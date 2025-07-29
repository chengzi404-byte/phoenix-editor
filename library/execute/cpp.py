from .base import *


class CppExecuter(Executer):
    def __init__(self, commandarea, printarea):
        super().__init__(commandarea, printarea)
        self.command = "g++ {} -o cache/cpp.exe -O2"