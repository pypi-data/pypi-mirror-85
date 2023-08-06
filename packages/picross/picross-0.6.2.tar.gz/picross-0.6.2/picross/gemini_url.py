import re
from urllib.parse import urlparse
from .about_pages import AboutUrl


class GeminiUrl:
    PROTOCOL = "gemini"
    __slots__ = ("host", "port", "path", "query", "fragment")
    host: str
    port: int
    path: str
    query: str
    fragment: str

    def __init__(self, host, port, path, query, fragment):
        """
        You probably don't want to use this constructor directly.
        Use one of the parse methods instead.
        """
        self.host = host
        self.port = port
        self.path = path
        self.query = query
        self.fragment = fragment

    def __repr__(self):
        return (
            f"{self.PROTOCOL}://{self.host}:{self.port}{self.path}"
            f"{('?' + self.query) if self.query else ''}"
            f"{('#' + self.fragment) if self.fragment else ''}"
        )

    def without_protocol(self):
        return (
            f"{self.host}{(':'+self.port) if self.port != 1965 else ''}{self.path}"
            f"{('?' + self.query) if self.query else ''}"
            f"{('#' + self.fragment) if self.fragment else ''}"
        )

    @classmethod
    def parse(cls, text, current_url):
        assert not re.search(r"\s", text), "Url should not contain any whitespace!"
        if text.startswith("about:"):
            return self.parse_absolute_url(text)

        parsed = urlparse(text)
        protocol = parsed.scheme
        if protocol == cls.PROTOCOL:
            return cls.parse_absolute_url(text)

        if protocol:
            raise UnsupportedProtocolError(protocol)

        # absolute url with scheme omitted
        # for example, "//example.com/foo"
        if text.startswith("//"):
            return cls.parse_absolute_url("gemini:" + text)

        if current_url is None:
            raise NonAbsoluteUrlWithoutContextError(text)

        # relative url starting from top level
        if text.startswith("/"):
            return GeminiUrl(
                current_url.host,
                current_url.port,
                parsed.path,
                parsed.query,
                parsed.fragment,
            )

        # just query:
        if text.startswith("?"):
            return GeminiUrl(
                current_url.host,
                current_url.port,
                current_url.path,
                parsed.query,
                parsed.fragment,
            )

        # just relative url:
        # trim stuff after the last `/` - for example:
        #   current url: gemini://example.com/foo/bar
        #   raw url text: yikes
        #   => parsed url: gemini://example.com/foo/yikes
        current_path = current_url.path[: current_url.path.rfind("/") + 1]
        if current_path == "":
            current_path = "/"

        current_path += parsed.path
        return GeminiUrl(
            current_url.host,
            current_url.port,
            current_path,
            parsed.query,
            parsed.fragment,
        )

    @staticmethod
    def parse_absolute_url(text):
        # TODO: urlparse doesn't seem that foolproof. Revisit later.
        no_protocol = text.lstrip("gemini://")
        if no_protocol.startswith("about:"):
            return AboutUrl(no_protocol[6:])

        parsed = urlparse(text)
        return GeminiUrl(
            parsed.hostname,
            parsed.port or 1965,
            parsed.path,
            parsed.query,
            parsed.fragment,
        )

