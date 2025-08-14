from subprocess import Popen, PIPE
import os

def runFile(path:str) -> list:
    os.system(f"gcc {path} -o {path.split('.')[0]}.exe -O2 -Wall -std=c99")

    runtool = Popen(
        [path.split('.')[0] + '.exe'],
        stdout=PIPE,
        stderr=PIPE
    )

    stdout, stderr = runtool.communicate()
    returncode = runtool.returncode

    return [stdout, stderr, returncode]

__ver__ = "0.1.0"
__author__ = "Creative and dream"
