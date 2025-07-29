from .base import *


class PythonExecuter(Executer):
    def __init__(self, commandarea, printarea):
        super().__init__(commandarea, printarea)
        self.command = "python {}"