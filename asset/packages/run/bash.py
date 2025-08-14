from subprocess import Popen, PIPE
import shlex

def runFile(path: str) -> list:
    """ Execute the Bash script located at {path} """
    import os

    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file {path} does not exist.")

    runtool = Popen(
        shlex.split(f"bash {path}"),
        stdout=PIPE,
        stderr=PIPE
    )

    stdout, stderr = runtool.communicate()
    returncode = runtool.returncode

    return [stdout, stderr, returncode]

__ver__ = "0.1.0"
__author__ = "Creative and dream"
