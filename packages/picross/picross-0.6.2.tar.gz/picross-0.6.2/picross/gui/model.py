from typing import List

from .. import document
from ..transport import GeminiUrl
from appdirs import user_config_dir
from pathlib import Path


class History:
    h: List[GeminiUrl]
    current_index: int

    def __init__(self):
        self.h = []
        self.current_index = None

    def visit(self, url: GeminiUrl):
        # remove forward history first:
        if self.current_index is not None:
            self.h = self.h[: self.current_index + 1]
        self.h.append(url)
        self.current_index = len(self.h) - 1

    def go_back(self):
        if self.can_go_back():
            self.current_index -= 1

    def go_forward(self):
        if self.can_go_forward():
            self.current_index += 1

    def can_go_back(self):
        return self.current_index not in [None, 0]

    def can_go_forward(self):
        return self.current_index is not None and self.current_index < len(self.h) - 1

    def get_current_url(self):
        try:
            return self.h[self.current_index]
        except (IndexError, TypeError):
            return None


class Tab:
    plaintext = ""
    gemini_nodes = None
    history: History
    mime_type = ""
    url: GeminiUrl
    title: str
    sync_view_tabs = None

    def __init__(self, url, title=None):
        self.history = History()
        self.url = url
        self.title = title if title is not None else url

    def update_content(self, plaintext, mime_type):
        self.plaintext = plaintext
        self.mime_type = mime_type
        self.gemini_nodes = []
        if mime_type == "text/gemini":
            try:
                self.gemini_nodes = document.parse(plaintext)
            except Exception:
                print("Invalid gemini document!")

        page_title = document.get_title(self)
        if page_title:
            self.title = page_title
        if callable(self.sync_view_tabs):
            self.sync_view_tabs()
