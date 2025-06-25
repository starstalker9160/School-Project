import os, pefile

class Vars:
    @property
    def BG(self): return "#C0C0C0"
    @property
    def BTN(self): return "#C0C0C0"
    @property
    def BTN_DARK(self): return "#808080"
    @property
    def BTN_LIGHT(self): return "#FFFFFF"
    @property
    def TEXT(self): return "#000000"
    @property
    def TITLE_BG(self): return "#000080"
    @property
    def TITLE_FG(self): return "#FFFFFF"
    @property
    def FONT(self): return ("MS Sans Serif", 10)
    @property
    def FONT_BOLD(self): return ("MS Sans Serif", 10, "bold")

class Style:
    def __init__(self, root):
        root.option_add("*Button.Background", Vars().BTN)
        root.option_add("*Button.Relief", "raised")
        root.option_add("*Button.Font", Vars().FONT)
        root.option_add("*Label.Font", Vars().FONT)
        root.option_add("*Label.Background", Vars().BG)

class DLLFile:
    def __init__(self, absPath):
        self.path = absPath
        self.fileName = os.path.basename(absPath)
        self.fileSize = os.path.getsize(absPath)
        self.isDotnet = False

        self.scanResult = None

    def doScan(self) -> bool:
        try:
            # do scan and update self.scanResult accordingly
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

class EXEFile:
    def __init__(self, absPath):
        self.path = absPath
        self.fileName = os.path.basename(absPath)
        self.fileSize = os.path.getsize(absPath)
        self.isDotnet = False

        self.scanResult = None

    def doScan(self) -> bool:
        try:
            # do scan and update self.scanResult accordingly
            return True
        except Exception as e:
            return e

class ScanResult:
    def __init__(self, stream):
        self.data = stream