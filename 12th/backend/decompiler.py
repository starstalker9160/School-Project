import ctypes
import os, sys
from backend.helper import DLLFile, EXEFile

class Decompiler:
    def __init__(self):
        self.result = {}
        self.files = []
        # self.decoderDll = ctypes.CDLL('bin/decoder.dll')

    def scan(self, files: list):
        print('[ Decompiler ]', *files, sep='\n')
        for i in files:
            if i.lower().endswith(".dll"):
                self.files.append(DLLFile(i))
            elif i.lower().endswith(".exe"):
                self.files.append(EXEFile(i))

    def decompile_exe(self):
        print("[Decompiler] Decompiling EXE...")

    def list_dlls(self):
        return self.result.get("dlls", [])

    def generate_options(self):
        return ["Option 1", "Option 2"]