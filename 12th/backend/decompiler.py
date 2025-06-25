import ctypes
import os, sys
from backend.errors import *
from backend.helper import DLLFile, EXEFile

class Decompiler:
    def __init__(self):
        self.files = []
        # self.decoderDll = ctypes.CDLL('bin/decoder.dll')

    def scan(self, files: list):
        for i in files:
            if i.lower().endswith(".dll"):
                self.files.append(DLLFile(i))
            elif i.lower().endswith(".exe"):
                self.files.append(EXEFile(i))
        print('[ Decompiler ] Files found: ', *[i.path for i in self.files], sep='\n    - ')
        for i in self.files:
            if i.doScan() == True:
                print(f"[ Decompiler ] Successfully scanned {i.path}")
            else:
                raise ScanError(f"[ Decompiler ] Error while scanning file {i.path}")

    def decompileEXE(self, file:EXEFile):
        print("[ Decompiler ] Decompiling EXE...")

    def decompileDLL(self, file:DLLFile):
        print("[ Decompiler ] Decompiling DLL...")

    def generate_options(self):
        return ["Option 1", "Option 2"]