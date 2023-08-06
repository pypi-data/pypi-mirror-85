from tkinter import (
    Toplevel,
    Text,
    ttk,
    filedialog,
    messagebox,
)
from .widgets import McEntry
import subprocess
import os


class Dialog:
    root: Toplevel
    inputbar: McEntry
    submit_btn: ttk.Button
    value: str
    canceled = False

    def __init__(self, question: str, sensitive=False):
        root = Toplevel()
        root.title = "Picross Browser input"
        self.root = root
        prompt = ttk.Label(root, text=question)
        inputbar = McEntry(root, show="*" if sensitive else "")
        inputbar.bind("<Return>", self.submit)
        inputbar.bind("<KP_Enter>", self.submit)
        inputbar.focus_set()
        self.inputbar = inputbar
        buttons_frame = ttk.Frame(root)
        submit_btn = ttk.Button(buttons_frame, text="OK", command=self.submit)
        cancel_btn = ttk.Button(buttons_frame, text="Cancel", command=self.cancel)
        file_btn = ttk.Button(
            buttons_frame, text="Upload File...", command=self.select_file
        )
        editor_btn = ttk.Button(
            buttons_frame, text="Editor...", command=self.open_editor
        )
        self.submit_btn = submit_btn
        prompt.pack(fill="x", padx=2, pady=3, ipadx=2, ipady=3)
        inputbar.pack(fill="x", padx=2, pady=3, ipadx=2, ipady=3, expand=True)
        editor_btn.pack(side="right", padx=2, pady=3)
        file_btn.pack(side="right", padx=2, pady=3)
        cancel_btn.pack(side="right", padx=2, pady=3)
        submit_btn.pack(side="right", padx=2, pady=3)
        buttons_frame.pack(fill="x")
        self.value = None
        style = ttk.Style()

    def cancel(self):
        self.canceled = True
        self.root.destroy()

    def submit(self, ev=None):
        self.value = self.inputbar.get()
        self.root.destroy()

    def select_file(self):
        fp = filedialog.askopenfilename(initialdir="~/", title="Select File to Upload")
        try:
            with open(fp) as f:
                content = f.read()
                f.close()
                length = len(content)
                # HACK query after shortest URL imaginable:
                # gemini://x.xx/?[query_text_here]
                # |<--- 15 ---->||<--- 1009 ---->|
                # Let's hope the server handles the rest
                if length > 1009:
                    # file apparently too large to fit in URL
                    messagebox.showerror(
                        "Upload Error", "File too large (maximum: 1009 characters)"
                    )
                else:
                    self.value = content
                    self.root.destroy()
        except:
            messagebox.showerror("Upload Error", "Cannot read file")

    def open_editor(self):
        fp = "/tmp/picross_query"
        try:
            open(fp, "x")
        except FileExistsError:
            pass
        f = open(fp, "r")

        try:
            # blocking operation
            proc = subprocess.run(["xdg-open", fp], capture_output=True)
            if proc.returncode == 0:
                content = f.read()
                f.close()
                os.remove(fp)
                self.value = content
                self.root.destroy()
            else:
                messagebox.showerror(
                    "Cannot open editor", "stderr:\n" + proc.stderr.decode("utf-8")
                )
        except FileNotFoundError:
            messagebox.showerror(
                "Cannot open editor", "xdg-open is not found on your device"
            )

    def get(self):
        # blocking method
        # returns value when it is submitted and None when canceled
        while self.value is None and not self.canceled:
            try:
                self.root.state()
            except:  # if window no longer exists, break loop
                break
            pass
        return self.value
