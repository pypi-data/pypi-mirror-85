import curio
from appdirs import user_config_dir
from pathlib import Path
import os
import ssl
from cryptography import x509
import hashlib
import csv
from typing import NamedTuple
from datetime import datetime
from dateutil.parser import parse

"""
TOFU stands for Tofu On First Use
just kidding, it stands for Trust On First Use
This library will store the domain and port of the URL
and the SHA256 hash and expiry date ("not valid after") of a certificate
when the user visits a Gemini server for the first time.
When the user visits it again, the hash of its cert will be compared with the one stored.
It will be accepted if they match, or the original cert has expired, in which case
the updated cert will replace it.
If accepted, the connection shall proceed.
"""

TofuEntry = NamedTuple(
    "TofuEntry", [("domain", str), ("port", int), ("hash", str), ("expiry", datetime)]
)


class TofuDatabase:
    untrusted_cert_callback = None

    def __init__(self):
        self.db_file = Path(user_config_dir("picross")) / "tofu.csv"

    def read(self) -> list:
        """Reads all TOFU entries from DB
        """
        with open(self.db_file) as f:
            reader = csv.reader(f)
            tofu_entries = [
                TofuEntry(domain=l[0], port=int(l[1]), hash=l[2], expiry=parse(l[3]))
                for l in reader
            ]
            f.close()
        return tofu_entries

    def append(self, entry: TofuEntry):
        """Writes one TOFU entry to DB
        """
        with open(self.db_file, "a") as f:
            writer = csv.writer(f)
            writer.writerow(
                (entry.domain, entry.port, entry.hash, entry.expiry.isoformat())
            )
            f.close()

    def revoke(self, idx: int):
        """Remove entry #idx from DB
        """
        entries = self.read()
        with open(self.db_file, "w") as f:
            writer = csv.writer(f)
            writer.writerows(entries[:idx] + entries[idx + 1 :])
            f.close()

    async def handle_url(self, url):
        """Method called each time a connection is made to a server 
        Takes a GeminiUrl, checks against DB,
        returns boolean whether to proceed visiting the page
        """
        pem_str = await curio.ssl.get_server_certificate((url.host, url.port))
        cert = x509.load_pem_x509_certificate(pem_str.encode("utf-8"))
        sha256 = hashlib.sha256(pem_str.encode("utf-8")).hexdigest()
        not_valid_after = cert.not_valid_after

        for idx, entry in enumerate(self.read()):
            # compare domain and port
            if entry.domain == url.host and entry.port == url.port:
                if entry.hash == sha256:
                    return True  # everything matches
                elif entry.expiry < datetime.now():
                    # original cert expired
                    self.revoke(idx)
                    self.trust_cert(url.host, url.port, sha256, not_valid_after)
                    return True
                # no match, untrusted cert
                if callable(self.untrusted_cert_callback):
                    trust = self.untrusted_cert_callback(
                        url,
                        entry,
                        TofuEntry(url.host, url.port, sha256, not_valid_after),
                    )
                    if trust:
                        self.revoke(idx)
                        self.trust_cert(url.host, url.port, sha256, not_valid_after)
                        return True
                    return False

        # first visit, trust on first use
        self.trust_cert(url.host, url.port, sha256, not_valid_after)
        return True

    def trust_cert(self, domain, port, hash, expiry):
        self.append(TofuEntry(domain, port, hash, expiry))


def system_certs() -> str:
    """Currently unused. System-trusted certs have no privilege in picross.
    """
    ca_file = "/etc/ssl/cert.pem"
    with open(ca_file) as f:
        certs = f.read()
        f.close()
    return certs


class UntrustedCertificateError(Exception):
    pass
