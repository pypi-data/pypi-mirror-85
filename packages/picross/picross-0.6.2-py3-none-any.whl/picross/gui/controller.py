import logging
import threading
import time
import traceback
import urllib
import sys
import re
from ssl import SSLCertVerificationError
from tkinter import READABLE, Tk, messagebox

import curio

from .. import tofu, conf
from ..transport import (
    MAX_REQUEST_SECONDS,
    GeminiUrl,
    NonAbsoluteUrlWithoutContextError,
    UnsupportedProtocolError,
    get,
)
from ..download import download
from .model import Tab
from .view import WAITING_CURSOR, View
from .dialog import Dialog
from ..document import get_title
from ..about_pages import about_pages

statusbar_logger = logging.getLogger("statusbar")


class Controller:
    def __init__(self):
        self.root = Tk()
        self.root.alt_shortcuts = set()
        tab = Tab("about:home", "Home")
        tab.sync_view_tabs = self.sync_view_tabs
        self.tabs = [tab]  # init home tab
        self.tab_idx = 0  # tab index
        self.tab = self.tabs[0]
        self.view = View(self.root, self.tab)
        self.sync_view_tabs()
        self.view.activate_tab(0)
        self.root.title("Picross Browser")
        self.root.geometry(conf.get("window-geometry"))

        self.gui_ops = curio.UniversalQueue(withfd=True)
        self.coro_ops = curio.UniversalQueue()

        # Set up event handler for queued GUI updates
        self.root.createfilehandler(self.gui_ops, READABLE, self.process_gui_ops)

        # When in the middle of an action, this flag is set to False to prevent user
        # from clicking other random stuff:
        self.allow_user_interaction = True

        def put_coro_op(func):
            def inner(*args, **kwargs):
                if self.allow_user_interaction:
                    self.coro_ops.put(
                        self.show_waiting_cursor_during_task(func, *args, **kwargs)
                    )

            return inner

        self.view.go_callback = put_coro_op(self.go_callback)
        self.view.link_click_callback = put_coro_op(self.link_click_callback)
        self.view.back_callback = put_coro_op(self.back_callback)
        self.view.forward_callback = put_coro_op(self.forward_callback)
        self.view.refresh_callback = put_coro_op(self.refresh_callback)
        self.view.newtab_callback = self.new_tab
        self.view.closetab_callback = self.close_tab
        self.view.switchtab_callback = self.switch_to_tab
        self.view.movetabup_callback = lambda: self.move_tab("up")
        self.view.movetabdown_callback = lambda: self.move_tab("down")
        self.view.toc_click_callback = self.toc_navigate

        curio.run(self.visit_link(GeminiUrl.parse_absolute_url("about:home")))

    async def main(self):
        while True:
            coro = await self.coro_ops.get()
            await coro

    def run(self):
        threading.Thread(target=curio.run, args=(self.main,), daemon=True).start()
        self.root.mainloop()

    async def put_gui_op(self, func, *args, **kwargs):
        await self.gui_ops.put((func, args, kwargs))

    def process_gui_ops(self, file, mask):
        while not self.gui_ops.empty():
            func, args, kwargs = self.gui_ops.get()
            func(*args, **kwargs)

    async def show_waiting_cursor_during_task(self, func, *args, **kwargs):
        async def show():
            self.view.text.config(cursor=WAITING_CURSOR)
            self.root.config(cursor=WAITING_CURSOR)
            self.view.allow_changing_cursor = False

        async def hide():
            self.view.text.config(cursor="xterm")
            self.root.config(cursor="arrow")
            self.view.allow_changing_cursor = True

        await show()
        self.allow_user_interaction = False

        try:
            await func(*args, **kwargs)
        except Exception:
            # a catch-all here so that our show_waiting...() coroutine can be yielded
            traceback.print_exc()

        self.allow_user_interaction = True
        await hide()

    async def go_callback(self, url: str):
        url = GeminiUrl.parse_absolute_url(url)
        await self.visit_link(url)

    async def link_click_callback(self, raw_url, new_tab=False):
        try:
            url = GeminiUrl.parse(raw_url, self.tab.history.get_current_url())
            if new_tab:
                self.new_tab(url=url)  # Can't know the title yet
            await self.visit_link(url)
        except NonAbsoluteUrlWithoutContextError:
            await self.put_gui_op(
                messagebox.showwarning,
                "Ambiguous link",
                "Cannot visit relative urls without a current_url context",
            )
        except UnsupportedProtocolError as e:
            await self.put_gui_op(
                messagebox.showinfo,
                "Unsupported protocol",
                f"{e} links are unsupported (yet?)",
            )
        except SSLCertVerificationError:
            await self.put_gui_op(
                messagebox.showerror,
                "Invalid server certificate",
                "Server is NOT using a valid CA-approved TLS certificate.",
            )

    async def visit_link(self, url: GeminiUrl):
        if repr(url) in about_pages:
            self.tab.update_content(*about_pages[repr(url)]())
            await self.put_gui_op(self.view.render_page)
            return

        try:
            resp = await self.load_page(url)
            self.tab.history.visit(resp.url)
            await self.put_gui_op(self.view.render_page, fragment=url.fragment)

        except tofu.UntrustedCertificateError:
            return

        except curio.errors.TaskTimeout:
            await self.put_gui_op(
                statusbar_logger.info, f"Request timed out: {MAX_REQUEST_SECONDS}s",
            )
            await self.put_gui_op(
                messagebox.showwarning,
                "Request timed out",
                f"Request to {url.without_protocol()} took longer than {MAX_REQUEST_SECONDS}s",
            )

        except (ConnectionError, OSError) as e:
            await self.put_gui_op(statusbar_logger.info, str(e))
            raise

    async def back_callback(self):
        self.tab.history.go_back()
        await self.load_page(self.tab.history.get_current_url())
        await self.put_gui_op(self.view.render_page)

    async def forward_callback(self):
        self.tab.history.go_forward()
        await self.load_page(self.tab.history.get_current_url())
        await self.put_gui_op(self.view.render_page)

    async def refresh_callback(self):
        await self.load_page(self.tab.history.get_current_url())
        self.view.render_page()

    async def submit_query(self, query: str, base_url: GeminiUrl):
        escaped_query = urllib.parse.quote(query)
        url = GeminiUrl.parse("?" + escaped_query, base_url)
        await self.visit_link(url)

    def untrusted_cert_callback(
        self, url: GeminiUrl, old_cert: tofu.TofuEntry, new_cert: tofu.TofuEntry
    ):
        # not async because the result has to be awaited
        trust = messagebox.askyesno(
            "Untrusted certificate",
            "\n".join(
                [
                    f"The certificate received from {url.host}:{url.port} does not match the one previously stored.",
                    "",
                    f"Old certificate: SHA-256 {old_cert.hash}, not valid after {old_cert.expiry}",
                    f"New certificate: SHA-256 {new_cert.hash}, not valid after {new_cert.expiry}",
                    "",
                    "Do you wish to trust the new certificate?",
                ]
            ),
            icon="warning",
        )
        return trust

    async def load_page(self, url: GeminiUrl):
        await self.put_gui_op(statusbar_logger.info, f"Requesting {url}...")
        start = time.time()
        tofu_db = tofu.TofuDatabase()
        tofu_db.untrusted_cert_callback = self.untrusted_cert_callback
        proceed = await tofu_db.handle_url(url)
        if not proceed:
            raise tofu.UntrustedCertificateError
        resp = await get(url)
        request_time = time.time() - start
        await self.put_gui_op(
            statusbar_logger.info,
            f"{resp.status} {resp.meta} (took {request_time:.2f}s)",
        )

        # Support whatever encoding that python supports
        body_string = ""
        if resp.body and resp.charset:
            try:
                body_string = resp.body.decode(resp.charset)
            except LookupError:
                await self.put_gui_op(
                    self.tab.update_content,
                    "\n".join(
                        [
                            "Error:",
                            f"{resp.status} {resp.meta}",
                            f"Unsupported charset: {resp.charset}",
                        ]
                    ),
                    "text/x-picrosserror",
                )
                return resp
            except UnicodeDecodeError:
                # try downloading as file instead
                download(url, resp.body)
                return resp

        # Sucessfully decoded body string!
        if resp.status.startswith("2"):
            await self.put_gui_op(self.tab.update_content, body_string, resp.mime_type)
        elif resp.status.startswith("1"):
            dialog = Dialog(
                repr(resp.url) + " requests the following input: \n\n" + resp.meta,
                sensitive=resp.status == "11",
            )

            query = dialog.get()

            if query:
                await self.submit_query(query, resp.url)
        else:
            await self.put_gui_op(
                self.tab.update_content,
                f"Error:\n{resp.status} {resp.meta}\n{body_string}",
                "text/x-picrosserror",
            )
        return resp

    def new_tab(self, url=None, title=None):
        if url is None and title is None:
            tab = Tab("about:home", "Home")
        else:
            tab = Tab(url, title)
        tab.sync_view_tabs = self.sync_view_tabs
        self.tabs.append(tab)
        self.switch_to_tab(len(self.tabs) - 1)
        if url is None and title is None:
            curio.run(self.visit_link(GeminiUrl.parse_absolute_url("about:home")))

    def switch_to_tab(self, idx: int = None, rel: int = None):
        if idx is None:
            # invocation is from user input, i.e. clicking on a tab
            # tabs_list.curselection() -> (int,)
            try:
                idx = self.view.tabs_list.curselection()[0]
            except IndexError:
                return  # focus moved away from listbox
        tabcount = len(self.tabs)
        if rel is not None:
            # relative tab movement
            # typically +1 or -1
            # loops over all tabs
            idx = self.tab_idx + rel
            while not 0 <= idx < tabcount:
                if idx >= tabcount:
                    idx -= tabcount
                elif idx < 0:
                    idx += tabcount
        self.tab_idx = idx
        self.tab = self.tabs[idx]
        self.sync_view_tabs()
        self.view.activate_tab(idx)
        self.view.render_page()

    def close_tab(self, idx=None):
        if len(self.tabs) == 1:
            # close only tab: exit
            sys.exit()

        if not idx:
            # action invoked when closetab_btn is pressed,
            # or ^W
            # close current tab
            try:
                idx = self.view.tabs_list.curselection()[0]
            except IndexError:
                # nothing is selected for some reason
                idx = 0

        self.tabs = self.tabs[:idx] + self.tabs[idx + 1 :]
        self.sync_view_tabs()
        if idx < len(self.tabs):
            switch_to_idx = idx
        else:
            switch_to_idx = idx - 1

        self.switch_to_tab(switch_to_idx)

    def move_tab(self, direction: str):
        tabs = self.tabs
        try:
            idx = self.view.tabs_list.curselection()[0]
        except IndexError:
            return

        if direction == "up" and not idx == 0:
            self.tabs = tabs[: idx - 1] + [tabs[idx], tabs[idx - 1]] + tabs[idx + 1 :]
            idx -= 1
        elif direction == "down" and not idx == len(tabs) - 1:
            self.tabs = tabs[:idx] + [tabs[idx + 1], tabs[idx]] + tabs[idx + 2 :]
            idx += 1

        self.sync_view_tabs()
        self.switch_to_tab(idx)

    def sync_view_tabs(self):
        # callback that's passed to Tab.
        # internal use is accepted.
        self.view.tabs = self.tabs

    def toc_navigate(self):
        try:
            selected = self.view.toc_list.curselection()[0]
        except IndexError:
            return
        toc = [i.strip("' ") for i in self.view.toc.get().strip("()").split(",")]
        fragment = toc[selected]
        match = re.match(r"^(#{1,3})\s+(.+)$", fragment)
        heading = match.group(2)
        self.view.scroll_to_fragment(re.sub("\s", "_", heading))
