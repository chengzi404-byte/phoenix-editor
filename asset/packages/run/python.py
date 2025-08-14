def runFile(path:str) -> list:
    """ Execute the Python file located at {path} """
    import subprocess
    import os

    if not os.path.isfile(path):
        raise FileNotFoundError(f"The file {path} does not exist.")

    runtool = subprocess.Popen(
        ["python", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    stdout, stderr = runtool.communicate()
    returncode = runtool.returncode

    return [stdout, stderr, returncode]
    
__ver__ = "0.1.0"
__author__ = "Creative and dream"
