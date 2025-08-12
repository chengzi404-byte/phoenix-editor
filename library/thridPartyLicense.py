from tkinter import Tk, Label

def show():
    root = Tk("第三方协议 - Thrid party license")
    Label(root, text="[MIT]Phoenix Highlighter - https://gitee.com/phoenix-editor/phoenix-highlighter").pack()
    Label(root, text="[MIT]Phoenix Debugging Tool - https://gitee.com/phoenix-editor/phoenix-editor-debugging-tool").pack()
    root.mainloop()