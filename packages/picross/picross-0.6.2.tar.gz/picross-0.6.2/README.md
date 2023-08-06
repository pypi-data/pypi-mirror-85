Picross is a minimal and usable [gemini://](https://gemini.circumlunar.space/)
browser written in Python and tkinter.

![](https://fkfd.me/static/picross-0.6.2.png)

# Installation

Install from PyPI for releases:

```sh
# do user install or grant privilege
pip install picross --user
```

or install from source:

```sh
git clone https://git.sr.ht/~fkfd/picross
cd picross
pip install -r requirements.txt --user
python setup.py install --user
```

# Usage

Run `picross` to open browser, and `picross -h` to get a full list of CLI
arguments which modify appearance or behavior.

The priority is CLI arg > config file > default.

## Keyboard shortcuts:

- Hold `Alt` to see possible button shortcuts underlined. This is what Qt calls
  [Accelerator Keys](https://doc.qt.io/qt-5/accelerators.html).
- `Ctrl-r` / `F5`: refresh page.
- `Ctrl-l`: jump to address bar.
- `Ctrl-t`: open new tab.
- `Ctrl-w`: close current tab.
- `Ctrl-PgUp/PgDown`: switch to tab above/below.

# Development

To get started:

```sh
git clone https://git.sr.ht/~fkfd/picross
cd picross
# you can set up virtualenv here if you want
# install dependencies
# escalate/limit privilege if necessary
pip install -r requirements.txt
python -m picross
```

Mailing list for sending patches and anything related to Picross:
[~fkfd/picross@lists.sr.ht](https://lists.sr.ht/~fkfd/picross)

If you're not familiar with the mailing list workflow, check out
[git-send-email.io][1] and [mailing list etiquette][2]. [useplaintext.email][3]
also has useful plaintext setup tips for various email clients.

[1]: https://git-send-email.io/
[2]: https://man.sr.ht/lists.sr.ht/etiquette.md
[3]: https://useplaintext.email/
