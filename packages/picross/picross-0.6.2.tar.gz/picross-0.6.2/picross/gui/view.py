import logging
import sys
import re
from tkinter import (
    Tk,
    PanedWindow,
    Text,
    Listbox,
    ttk,
    font,
    StringVar,
)

from .. import conf
from ..document import (
    GeminiNode,
    H1Node,
    H2Node,
    H3Node,
    LinkNode,
    ListItemNode,
    PreformattedNode,
    TextNode,
    is_title_node,
    get_toc,
)
from .model import Tab
from .widgets import AltButton, McEntry, ReadOnlyText

# OS-specific values
if sys.platform == "win32":
    TTK_THEME = "vista"
    POINTER_CURSOR = "center_ptr"
    WAITING_CURSOR = "wait"
elif sys.platform == "darwin":
    TTK_THEME = "aqua"
    POINTER_CURSOR = "pointinghand"
    WAITING_CURSOR = "wait"
else:
    TTK_THEME = "clam"
    POINTER_CURSOR = "hand1"
    WAITING_CURSOR = "watch"


def pick_font(names):
    available = font.families()
    picked = None
    for name in names:
        if name in available:
            picked = name
            break

    if not picked:
        picked = names[-1]

    return picked


def register_status_bar_log_handler(status_bar: ttk.Label):
    class StatusBarHandler(logging.Handler):
        def emit(self, record):
            status_bar.config(text=self.format(record))

    logger = logging.getLogger("statusbar")
    logger.setLevel(logging.INFO)
    logger.addHandler(StatusBarHandler())


class View:
    model: Tab
    tab_titles: StringVar
    tabs_list: Listbox
    toc: StringVar
    toc_list: Listbox
    address_bar: ttk.Entry
    go_btn: AltButton
    back_btn: AltButton
    forward_btn: AltButton
    text: Text
    status_bar: ttk.Label

    allow_changing_cursor = True

    go_callback = None
    link_click_callback = None
    back_callback = None
    forward_callback = None
    refresh_callback = None
    toc_click_callback = None

    newtab_callback = None
    closetab_callback = None
    switchtab_callback = None
    movetabup_callback = None
    movetabdown_callback = None

    def __init__(self, root: Tk, tab):
        self.model = tab
        self._tabs = []  # list of Tab instances
        self.tab_titles = StringVar(value=[])
        self.toc = StringVar(value=[])

        text_font = pick_font([conf.get("text-font"), "Noto Sans", "TkTextFont"])

        mono_font = pick_font(
            [conf.get("mono-font"), "Noto Sans Mono", "Noto Mono", "TkFixedFont"]
        )

        # address bar + buttons
        navigation_bar = ttk.Frame(root)
        navigation_bar.pack(fill="x")

        paned_window = PanedWindow(root)
        paned_window.pack(fill="both", expand=True)
        paned_window.config(showhandle=True)

        # tabs pane
        tabs_pane = ttk.Frame(paned_window)
        tabs_pane.pack(side="left", fill="y")
        root.bind("<Control-t>", lambda _: self.newtab_callback())
        root.bind("<Control-w>", lambda _: self.closetab_callback())
        # Tk uses Prior/Next for PgUp/PgDown
        root.bind("<Control-Prior>", lambda _: self.switchtab_callback(rel=-1))
        root.bind("<Control-Next>", lambda _: self.switchtab_callback(rel=1))

        # tabs control
        tabs_ctrl_btns_frame = ttk.Frame(tabs_pane)
        tabs_ctrl_btns_frame.pack(side="top", padx=2, pady=3)
        newtab_btn = ttk.Button(
            tabs_ctrl_btns_frame,
            text="+",
            width=5,
            command=lambda: self.newtab_callback(),
        )
        closetab_btn = ttk.Button(
            tabs_ctrl_btns_frame,
            text="🛇",
            width=5,
            command=lambda: self.closetab_callback(),
        )
        movetabup_btn = ttk.Button(
            tabs_ctrl_btns_frame,
            text="↑",
            width=5,
            command=lambda: self.movetabup_callback(),
        )
        movetabdown_btn = ttk.Button(
            tabs_ctrl_btns_frame,
            text="↓",
            width=5,
            command=lambda: self.movetabdown_callback(),
        )
        newtab_btn.pack(side="left", padx=2)
        closetab_btn.pack(side="left", padx=2)
        movetabup_btn.pack(side="left", padx=2)
        movetabdown_btn.pack(side="left", padx=2)

        # tabs listbox
        tabs_list = Listbox(tabs_pane, listvariable=self.tab_titles)
        tabs_list.config(
            font=(text_font, 12),
            bg=conf.get("background-color"),
            fg=conf.get("text-color"),
            selectbackground=conf.get("select-background"),
            selectforeground=conf.get("select-foreground"),
        )
        tabs_list.pack(side="top", fill="both", expand=True)
        tabs_list.bind("<<ListboxSelect>>", lambda _: self.switchtab_callback())
        self.tabs_list = tabs_list

        # TOC pane
        toc_pane = ttk.Frame(paned_window)
        toc_pane.pack(side="right", fill="y")

        # TOC list
        toc_list = Listbox(toc_pane, listvariable=self.toc, width=24)
        toc_list.config(
            font=(text_font, 12),
            bg=conf.get("background-color"),
            fg=conf.get("text-color"),
            selectbackground=conf.get("select-background"),
            selectforeground=conf.get("select-foreground"),
        )
        toc_list.pack(side="top", fill="both", expand=True)
        toc_list.bind("<<ListboxSelect>>", lambda _: self.toc_click_callback())
        self.toc_list = toc_list

        # gmi viewport
        viewport = ttk.Frame(paned_window)
        viewport.pack(side="left", fill="both", expand=True)

        # status bar
        status_bar = ttk.Label(root)
        self.status_bar = status_bar
        status_bar.config(justify="right")
        status_bar.pack(fill="x")
        register_status_bar_log_handler(status_bar)

        # Back/Forward buttons
        back_btn = AltButton(
            navigation_bar,
            text="◀",
            width=3,
            command=lambda: self.back_callback(),
            root=root,
            alt_char_index=0,
            alt_key="Left",
        )
        forward_btn = AltButton(
            navigation_bar,
            text="▶",
            width=3,
            command=lambda: self.forward_callback(),
            root=root,
            alt_char_index=0,
            alt_key="Right",
        )
        back_btn.pack(side="left", padx=2)
        forward_btn.pack(side="left", padx=2)
        self.back_btn = back_btn
        self.forward_btn = forward_btn

        # Address bar prefix
        address_prefix = ttk.Label(navigation_bar, text="gemini://")
        address_prefix.pack(side="left")

        # Address bar
        address_bar = McEntry(navigation_bar)
        self.address_bar = address_bar
        address_bar.pack(side="left", fill="both", expand=True, pady=3)
        address_bar.bind("<Return>", self._on_go)
        address_bar.bind("<KP_Enter>", self._on_go)
        address_bar.focus_set()

        def on_ctrl_l(ev):
            address_bar.focus()
            address_bar.select_all()

        root.bind("<Control-l>", on_ctrl_l)
        root.bind("<Control-r>", lambda _: self.refresh_callback())
        root.bind("<F5>", lambda _: self.refresh_callback())

        # Go button
        go_btn = AltButton(
            navigation_bar,
            text="Go",
            root=root,
            alt_char_index=0,
            command=self._on_go,
            width=5,
        )
        self.go_btn = go_btn
        go_btn.pack(side="left", padx=2, pady=3)

        # Main viewport implemented as a Text widget.
        text = ReadOnlyText(viewport, wrap="word")
        self.text = text
        self.render_page()

        text.config(
            font=(text_font, 13),
            bg=conf.get("background-color"),
            fg=conf.get("text-color"),
            padx=5,
            pady=5,
            # hide blinking insertion cursor:
            insertontime=0,
            # prevent text widget from pushing scrollbar/status bar out of the window:
            width=1,
            height=1,
            selectbackground=conf.get("select-background"),
            selectforeground=conf.get("select-foreground"),
        )
        text.pack(side="left", fill="both", expand=True)
        text.tag_config("link", foreground=conf.get("link-color"))
        text.tag_bind("link", "<Enter>", self._on_link_enter)
        text.tag_bind("link", "<Leave>", self._on_link_leave)
        text.tag_bind("link", "<Button-1>", self._on_link_click)
        text.tag_bind("link", "<Button-2>", self._on_link_middle_click)
        text.tag_config("pre", font=(mono_font, 13))
        text.tag_config("plaintext", font=(mono_font, 13))
        text.tag_config("listitem", foreground=conf.get("list-item-color"))

        base_heading_font = font.Font(font=text["font"])
        base_heading_font.config(weight="bold")
        h1_font = font.Font(font=base_heading_font)
        h1_font.config(size=h1_font["size"] + 8)
        text.tag_config("h1", font=h1_font)
        h2_font = font.Font(font=base_heading_font)
        h2_font.config(size=h2_font["size"] + 4)
        text.tag_config("h2", font=h2_font)
        h3_font = font.Font(font=base_heading_font)
        text.tag_config("h3", font=h3_font)

        text_scrollbar = ttk.Scrollbar(viewport, command=text.yview)
        text["yscrollcommand"] = text_scrollbar.set
        text_scrollbar.pack(side="left", fill="y")

        style = ttk.Style()
        style.theme_use(TTK_THEME)

    @property
    def tabs(self):
        return self._tabs

    @tabs.setter
    def tabs(self, new: list):
        self._tabs = new
        self.tab_titles.set([tab.title for tab in new])

    def activate_tab(self, idx: int):
        # multi-duty method
        # updates self.model and updates highlighted tab in tablist
        # synchronize tabs before calling this
        self.model = self.tabs[idx]
        self.tabs_list.selection_clear(0, "end")
        self.tabs_list.selection_set(idx)

    def _on_go(self, ev=None):
        orig_url = self.address_bar.get()
        url = orig_url.strip()

        if url.startswith("gemini://"):
            url = url[9:]

        if not url:
            return

        if url != orig_url:
            self.address_bar.delete(0, "end")
            self.address_bar.insert(0, url)

        if self.go_callback is not None:
            self.go_callback("gemini://" + url)

    def _on_link_enter(self, ev):
        if self.allow_changing_cursor:
            self.text.config(cursor=POINTER_CURSOR)

    def _on_link_leave(self, ev):
        if self.allow_changing_cursor:
            self.text.config(cursor="xterm")

    def _on_link_click(self, ev):
        raw_url = get_content_from_tag_click_event(ev)
        self.link_click_callback(raw_url)

    def _on_link_middle_click(self, ev):
        raw_url = get_content_from_tag_click_event(ev)
        self.link_click_callback(raw_url, new_tab=True)

    def render_page(self, fragment=""):
        # Enable/Disable forward/back buttons according to history
        self.back_btn.config(
            state="normal" if self.model.history.can_go_back() else "disabled"
        )
        self.forward_btn.config(
            state="normal" if self.model.history.can_go_forward() else "disabled"
        )

        # Update url in address bar
        current_url = self.model.history.get_current_url()
        if current_url is not None:
            self.address_bar.delete(0, "end")
            self.address_bar.insert(0, current_url.without_protocol())

        self.render_viewport(fragment)

    def render_viewport(self, fragment=""):
        self.text.delete("1.0", "end")
        if self.model.mime_type.startswith("text/gemini"):
            for node in self.model.gemini_nodes:
                render_node(node, self.text)
            # delete final trailing newline:
            self.text.delete("insert-1c", "insert")
            # generate TOC:
            self.toc.set(get_toc(self.model))
            if fragment:
                self.scroll_to_fragment(fragment)
        elif self.model.mime_type.startswith("text/"):
            self.toc.set([])
            self.text.insert("end", self.model.plaintext, ("plaintext",))
        else:
            self.toc.set([])
            self.text.insert("end", self.model.plaintext, ("plaintext",))
            self.text.insert(
                "end", f"Unsupported MIME type: {self.model.mime_type}", ("plaintext",)
            )

    def scroll_to_fragment(self, fragment: str):
        if not self.model.mime_type.startswith("text/gemini"):
            return  # NYI

        self.text.see("heading_" + fragment + ".first")


def render_node(node: GeminiNode, widget: Text):
    nodetype = type(node)
    if nodetype is TextNode:
        widget.insert("end", node.text)
    elif nodetype is LinkNode:
        widget.insert("end", "=> ")
        widget.insert("end", node.url, ("link",))
        if node.name:
            widget.insert("end", f" {node.name}")
    elif nodetype is PreformattedNode:
        widget.insert("end", f"```{node.alt}\n{node.text}\n```", ("pre",))
    elif nodetype is ListItemNode:
        widget.insert("end", node.text, ("listitem",))
    elif is_title_node(node):
        if nodetype is H1Node:
            level = "h1"
        elif nodetype is H2Node:
            level = "h2"
        elif nodetype is H3Node:
            level = "h3"
        widget.insert(
            "end", node.text, (level, "heading_" + re.sub("\s", "_", node.heading))
        )
    else:
        widget.insert("end", node.text)

    widget.insert("end", "\n")


def get_content_from_tag_click_event(event):
    # get the index of the mouse click
    index = event.widget.index("@%s,%s" % (event.x, event.y))

    # get the indices of all "link" tags
    tag_indices = list(event.widget.tag_ranges("link"))

    # iterate them pairwise (start and end index)
    for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
        # check if the tag matches the mouse click index
        if event.widget.compare(start, "<=", index) and event.widget.compare(
            index, "<", end
        ):
            # return string between tag start and end
            return event.widget.get(start, end)
