from ttkbootstrap import *
from tkinter import messagebox
from subprocess import run

def install():
    run(f"pip install {lib_entry.get()} -i {mirrors[mirror_list.get()]}")
    messagebox.showinfo("pipUI", "下载完成！")

def uninstall():
    run(f"pip uninstall {lib_entry2.get()}")
    messagebox.showinfo("pipUI", "卸载完成！")

def main():
    global lib_entry, lib_entry2, lib_install, lib_text, lib_text2, lib_uninstall, mirror_list, mirrors

    mirrors = {
        "清华源": "https://pypi.tuna.tsinghua.edu.cn/simple",
        "阿里源": "https://mirrors.aliyun.com/pypi/simple",
        "中科大源": "https://pypi.mirrors.ustc.edu.cn/simple",
        "官方源": "https://pypi.org/simple"
    }

    root = Window("pipUI")

    lib_text = Label(root, text="安装库：")
    lib_text.grid(column=0, row=0)

    lib_entry = Entry(root)
    lib_entry.grid(column=1, row=0)

    lib_install = Button(root, text="安装", command=install)
    lib_install.grid(column=2, row=0)

    lib_text2 = Label(root, text="卸载库：")
    lib_text2.grid(column=0, row=1)

    lib_entry2 = Entry(root)
    lib_entry2.grid(column=1, row=1)

    lib_uninstall = Button(root, text="卸载", command=uninstall)
    lib_uninstall.grid(column=2, row=1)

    mirror_list_text = Label(root, text="使用镜像：")
    mirror_list_text.grid(column=0, row=2)

    mirror_list = Combobox(root, values=["清华源", "阿里源", "中科大源"])
    mirror_list.grid(column=1, row=2)

    root.mainloop()