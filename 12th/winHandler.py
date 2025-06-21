import ctypes
import threading
import tkinter as tk
from backend.helper import *
from tkinter import filedialog
from PIL import Image, ImageTk
from backend.decompiler import Decompiler
from tkinterdnd2 import DND_FILES, TkinterDnD

class Window(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.vars = Vars()
        self.style = Style(self)
        self.decompiler = Decompiler()

        self.iconbitmap("Assets/icon.ico")
        self.iconphoto(False, ImageTk.PhotoImage(Image.open("Assets/icon.png")))
        
        self.title("Decompiler")

        self.overrideredirect(True)
        self.after(10, self._restore_window_styles)
        self.geometry("600x400")
        self.configure(bg=self.vars.BG)

        self._create_title_bar()

        self.container = tk.Frame(self, bg=self.vars.BG)
        self.container.pack(fill="both", expand=True)

        self.current_frame = None
        self.container.drop_target_register(DND_FILES)
        self.container.dnd_bind('<<Drop>>', self._onDrop)
        self.dragDrop()

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
        self.max_icon = ImageTk.PhotoImage(Image.open("Assets/maximize_icon.png").resize((16, 16)))
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
            command=self.toggleMaximize,
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

        self.title_bar.bind("<Button-1>", self.startWinMove)
        self.title_bar.bind("<B1-Motion>", self.doWinMove)
        self.title_label.bind("<Button-1>", self.startWinMove)
        self.title_label.bind("<B1-Motion>", self.doWinMove)

        self._isMaximised = False
        self._geom = self.geometry()

    def toggleMaximize(self):
        if not self._isMaximised:
            self._geom = self.geometry()
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
            self._isMaximised = True
        else:
            self.geometry(self._geom)
            self._isMaximised = False

    def startWinMove(self, event):
        self._x = event.x
        self._y = event.y

    def doWinMove(self, event):
        x = self.winfo_pointerx() - self._x
        y = self.winfo_pointery() - self._y
        self.geometry(f"+{x}+{y}")

    def dragDrop(self):
        self._switchFrame(tk.Frame(self.container, bg=self.vars.BG))

        label = tk.Label(self.current_frame, text="Drag and Drop Folder Here", bg=self.vars.BG, font=self.vars.FONT)
        label.pack(pady=100)

        button = tk.Button(self.current_frame, text="...or Click to Select Folder", command=self.select_folder)
        button.pack()

    def _onDrop(self, event):
        paths = self.tk.splitlist(event.data)
        folder = None
        for path in paths:
            import os
            if os.path.isdir(path):
                folder = path
                break
        if folder:
            self.scanning(folder)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.scanning(folder)

    def scanning(self, folder):
        self.container.drop_target_unregister()
        self._switchFrame(tk.Frame(self.container, bg=self.vars.BG))
        label = tk.Label(self.current_frame, text="Scanning, please wait...", font=self.vars.FONT, bg=self.vars.BG)
        label.pack(pady=150)
        threading.Thread(target=self._scanner, args=(folder,)).start()

    def _scanner(self, folder):
        self.decompiler.scan(folder)
        self.after(0, self.options)

    def options(self):
        self._switchFrame(tk.Frame(self.container, bg=self.vars.BG))
        label = tk.Label(self.current_frame, text="Scan complete. Choose options:", font=self.vars.FONT, bg=self.vars.BG)
        label.pack(pady=50)

    def _switchFrame(self, frame):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)
    
    def _restore_window_styles(self):
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        SWP_NOSIZE = 0x0001
        SWP_NOMOVE = 0x0002
        SWP_FRAMECHANGED = 0x0020

        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        ctypes.windll.user32.SetWindowPos(hwnd, None, 0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_FRAMECHANGED)
