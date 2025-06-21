import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from backend.helper import Vars, Style
from backend.decompiler import Decompiler

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.vars = Vars()
        self.style = Style(self)
        self.decompiler = Decompiler()

        self.iconphoto(False, ImageTk.PhotoImage(Image.open("Assets/icon.png")))

        self.overrideredirect(True)
        self.geometry("600x400")
        self.configure(bg=self.vars.BG)

        self._create_title_bar()

        self.container = tk.Frame(self, bg=self.vars.BG)
        self.container.pack(fill="both", expand=True)

        self.current_frame = None
        self.drag_drop()

    def _create_title_bar(self):
        self.title_bar = tk.Frame(self, bg=self.vars.TITLE_BG, relief="raised", bd=2, height=24)
        self.title_bar.pack(fill="x", side="top")

        self.title_label = tk.Label(
            self.title_bar,
            text="Decompiler",
            bg=self.vars.TITLE_BG,
            fg=self.vars.TITLE_FG,
            font=self.vars.FONT_BOLD,
            padx=6
        )
        self.title_label.pack(side="left", pady=2)

        # Load icons
        self.min_icon = ImageTk.PhotoImage(Image.open("Assets/minimise_icon.png").resize((16, 16)))
        self.max_icon = ImageTk.PhotoImage(Image.open("Assets/maximise_icon.png").resize((16, 16)))
        self.exit_icon = ImageTk.PhotoImage(Image.open("Assets/exit_icon.png").resize((16, 16)))

        closeButt = tk.Button(
            self.title_bar,
            image=self.exit_icon,
            command=self.destroy,
            bg=self.vars.TITLE_BG,
            relief="flat",
            bd=0
        )
        closeButt.pack(side="right", padx=2, pady=2)

        maxButt = tk.Button(
            self.title_bar,
            image=self.max_icon,
            command=self.toggle_maximize,
            bg=self.vars.TITLE_BG,
            relief="flat",
            bd=0
        )
        maxButt.pack(side="right", padx=0, pady=2)

        minButt = tk.Button(
            self.title_bar,
            image=self.min_icon,
            command=self.iconify,
            bg=self.vars.TITLE_BG,
            relief="flat",
            bd=0
        )
        minButt.pack(side="right", padx=0, pady=2)

        self.title_bar.bind("<Button-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)
        self.title_label.bind("<Button-1>", self.start_move)
        self.title_label.bind("<B1-Motion>", self.do_move)

        self._isMaximised = False
        self._geom = self.geometry()

    def toggle_maximize(self):
        if not self._isMaximised:
            self._geom = self.geometry()
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
            self._isMaximised = True
        else:
            self.geometry(self._geom)
            self._isMaximised = False

    def start_move(self, event):
        self._x = event.x
        self._y = event.y

    def do_move(self, event):
        x = self.winfo_pointerx() - self._x
        y = self.winfo_pointery() - self._y
        self.geometry(f"+{x}+{y}")

    def drag_drop(self):
        self._switch_frame(tk.Frame(self.container, bg=self.vars.BG))

        label = tk.Label(self.current_frame, text="Drag and Drop Folder Here", bg=self.vars.BG, font=self.vars.FONT)
        label.pack(pady=100)

        button = tk.Button(self.current_frame, text="...or Click to Select Folder", command=self.select_folder)
        button.pack()

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.scanning(folder)

    def scanning(self, folder):
        self._switch_frame(tk.Frame(self.container, bg=self.vars.BG))
        label = tk.Label(self.current_frame, text="Scanning, please wait...", font=self.vars.FONT, bg=self.vars.BG)
        label.pack(pady=150)
        threading.Thread(target=self._run_scan, args=(folder,)).start()

    def _run_scan(self, folder):
        self.decompiler.scan(folder)
        self.after(0, self.options)

    def options(self):
        self._switch_frame(tk.Frame(self.container, bg=self.vars.BG))
        label = tk.Label(self.current_frame, text="Scan complete. Choose options:", font=self.vars.FONT, bg=self.vars.BG)
        label.pack(pady=50)

    def _switch_frame(self, frame):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)
