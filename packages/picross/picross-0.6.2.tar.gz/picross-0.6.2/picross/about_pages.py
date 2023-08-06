import re
from pathlib import Path
from appdirs import user_config_dir

GEMINI_TYPE = "text/gemini"

"""
A set of methods that interface with Picross internally,
but not with the Gemini protocol.
Accessed with "about:xxx" in the URL bar.
Each method returns a 2-tuple: (text, mimetype)
"""


class AboutUrl:
    __slots__ = ("page",)
    page: str

    def __init__(self, page):
        self.page = page

    def __repr__(self):
        return f"about:{self.page}"

    def without_protocol(self):
        return repr(self)


def about_blank():
    return ("", "text/plain")


def about_home():
    homepage_fp = Path(user_config_dir("picross")) / "home.gmi"
    DEMO_TEXT = "\n".join(
        [
            "# Welcome to Picross Browser",
            "## Links",
            "=> gemini://gemini.circumlunar.space/   Gemini homepage",
            "=> gemini://gus.guru/   Gemini Universal Search engine",
            "=> gemini://gemini.conman.org/test/torture/    Gemini client torture test",
            "=> gemini://git.fkfd.me/cgi/picross/    Source code",
            "",
            "## Tips",
            f"* Set a .gmi file as your home page by moving it to {homepage_fp}",
            "* Use Ctrl+PgUp/PgDn to flip through tabs",
        ]
    )

    try:
        with open(homepage_fp) as homepage:
            page = (homepage.read(), GEMINI_TYPE)
            homepage.close()
        return page
    except:
        return (DEMO_TEXT, GEMINI_TYPE)


about_pages = {
    "about:blank": about_blank,
    "about:home": about_home,
}
