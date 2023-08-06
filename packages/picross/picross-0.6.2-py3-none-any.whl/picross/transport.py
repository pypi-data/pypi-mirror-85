import re
import ssl

from .gemini_url import GeminiUrl
from . import conf

import curio

MAX_RESP_HEADER_BYTES = 2 + 1 + 1024 + 2  # <STATUS><whitespace><META><CR><LF>
MAX_RESP_BODY_BYTES = 1024 * 1024 * 5
MAX_REDIRECTS = 3
MAX_REQUEST_SECONDS = 30


class Response:
    __slots__ = ("status", "meta", "body", "url", "mime_type", "charset")

    def __init__(
        self, status: str, meta: str, url, mime_type, charset, body: bytes = None
    ):
        self.status = status
        self.meta = meta
        self.body = body
        self.url = url
        self.mime_type = mime_type
        self.charset = charset

    def __repr__(self):
        return (
            f"Response(status={repr(self.status)}, "
            f"meta={repr(self.meta)}, "
            f"body={repr(self.body)}, "
            f"url='{repr(self.url)}', "
            f"mime_type={repr(self.mime_type)}, "
            f"charset={repr(self.charset)})"
        )


def _parse_resp_header(header, pattern=re.compile(r"^(\d\d)\s+(.{,1024})\r\n$")):
    match = pattern.match(header)
    assert match is not None, f"Malformed response header: {header}"
    status = match.group(1)
    meta = match.group(2).strip()
    return status, meta


def _parse_meta(meta, pattern=re.compile(r"^(\S+)\s*;\s*charset=(\S+)$")):
    match = pattern.match(meta)
    if not match:
        return None, None
    mime_type = match.group(1)
    charset = match.group(2)
    return mime_type, charset


# TODO: GeminiUrl's context-aware parse() method probably doesn't belong
# in a "transport" module.


class UnsupportedProtocolError(Exception):
    pass


class NonAbsoluteUrlWithoutContextError(Exception):
    pass


async def raw_get(url: GeminiUrl):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    sock = await curio.open_connection(
        url.host, url.port, ssl=context, server_hostname=url.host
    )

    async with sock:
        await sock.sendall((str(url) + "\r\n").encode())
        header = b""
        remainder = b""
        while True:
            header += await sock.recv(4096)
            if b"\r\n" in header:
                idx = header.find(b"\r\n")
                remainder = header[(idx + 2) :]
                header = header[: (idx + 2)]
                break
            elif len(header) > MAX_RESP_HEADER_BYTES:
                break

        status, meta = _parse_resp_header(header.decode())

        mime_type, charset = _parse_meta(meta)
        mime_type = mime_type or "text/gemini"
        charset = charset or "utf-8"

        resp = Response(
            status=status, meta=meta, url=url, mime_type=mime_type, charset=charset
        )

        if status.startswith("2"):
            body = remainder
            msg = await sock.recv(4096)
            body += msg
            while msg and len(body) <= MAX_RESP_BODY_BYTES:
                msg = await sock.recv(4096)
                body += msg
            resp.body = body

        return resp


async def get(url: GeminiUrl, redirect_count=0):
    resp = await curio.timeout_after(MAX_REQUEST_SECONDS, raw_get, url)
    if resp.status.startswith("3") and redirect_count < MAX_REDIRECTS:
        redirect_count += 1
        new_url = GeminiUrl.parse(resp.meta, url)
        print(f"Redirecting to {new_url}, count={redirect_count}")
        return await get(new_url, redirect_count)
    return resp

