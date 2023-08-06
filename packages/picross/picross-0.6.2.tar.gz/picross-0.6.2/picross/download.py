from . import conf
from pathlib import Path


def download(url, body):
    filename = str(url).split("/")[-1]
    with open(Path(conf.get("download-dest")).expanduser() / filename, "xb") as f:
        f.write(body)
        f.close()
