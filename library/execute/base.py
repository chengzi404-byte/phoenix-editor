from tkinter import END
import subprocess
import shlex


class Executer:
    def __init__(self, commandarea, printarea):
        self.commandarea = commandarea
        self.printarea = printarea
        self.command = ""
        
    def run(self, filename):
        try:
            args = shlex.split(self.command.format(filename))
            runtool = subprocess.Popen(args, stdin=subprocess.PIPE, 
                                    stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                    shell=True)
            
            stdout, stderr = runtool.communicate()

            self.printarea.delete(0.0, END)
            self.printarea.insert(END, stdout.decode(errors="replace"))  # Decode as a string
            self.printarea.insert(END, stderr.decode(errors="replace"))  # Decode as a string
        except Exception as e:
            self.printarea.insert(END, f"执行命令时出错: {str(e)}\n")