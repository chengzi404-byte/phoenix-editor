from library.highlighter_factory import HighlighterFactory
from library.logger import setup_logger
from tkinter import messagebox
from tkinter import filedialog 
from tkinter.font import Font
from tkinter import *
import os
import json
import subprocess
import sys
import zipfile
import tkinter as tk


# -------------------- Global Variables --------------------
global settings, highlighter_factory, file_path, logger
global codehighlighter2, codehighlighter
logger = setup_logger()
highlighter_factory = HighlighterFactory()

with open("./asset/settings.json", "r", encoding="utf-8") as fp:
    settings = json.load(fp)

class Settings:
    class Editor:
        def file_encoding():        return settings["editor.file-encoding"]
        def lang():                 return settings["editor.lang"]
        def langfile():             return f"./asset/lang/{settings["editor.lang"]}.json"
        def font():                 return settings["editor.font"]
        def font_size():            return settings["editor.fontsize"]
        def file_path():            return settings["editor.file-path"]
        def change(key, value):
            settings[f"editor.{key}"] = value

            with open("./asset/settings.json", "r", encoding="utf-8") as fp:
                json.dump(settings, fp)

    class Highlighter:
        def syntax_highlighting():  return settings["highlighter.syntax-highlighting"]

        def change(key, value):
            settings[f"highlighter.syntax-highlighting.{key}"] = value

            with open("./asset/settings.json", "r", encoding="utf-8") as fp:
                json.dump(settings, fp)
    
    class Init:
        def required_dirs():        return settings["init.required-dirs"]
        def required_packages():    return settings["init.required-packages"]

try:
    for directory in Settings.Init.required_dirs():
        if not os.path.exists(directory):
            os.makedirs(directory)
            
    # 检查并创建默认设置文件
    if not os.path.exists("./asset/settings.json"):
        default_settings = {
            "file-encoding": "utf-8",
            "lang": "zh-cn",
            "font": "Consolas",
            "fontsize": 12,
            "code": "python",  # 默认使用Python高亮
            "syntax-highlighting": {
                "theme": "vscode-dark",
                "enable-type-hints": True,
                "enable-docstrings": True
            }
        }
        with open("./asset/settings.json", "w", encoding="utf-8") as f:
            json.dump(default_settings, f, indent=4, ensure_ascii=False)

except Exception as e:
    logger.error(f"初始化失败: {str(e)}")



def load_language(lang):
    """加载语言文件"""
    lang_file = f"./asset/lang_{lang}.json"
    if os.path.exists(lang_file):
        with open(lang_file, "r", encoding="utf-8") as f:
            return json.load(f)
    update_ui_text()
    return {}

# -------------------- Settings Panel Functions --------------------
def open_settings_panel():
    """打开设置面板"""
    settings_window = Toplevel()
    settings_window.title("设置")
    settings_window.geometry("400x300")

    def apply_settings():
        """Apply settings immediately"""
        theme_name = theme_var.get()
        # 加载主题文件
        theme_file = f"./asset/theme/{theme_name}.json"
        try:
            with open(theme_file, "r", encoding="utf-8") as f:
                theme_data = json.load(f)
            codehighlighter.set_theme(theme_data)
            codearea.configure(font=Font(settings_window, family=font_var.get(), size=fontsize_var.get()))
        except Exception as e:
            print(f"应用主题失败: {str(e)}")

    # 主题设置
    theme_var = StringVar(value=Settings.Highlighter.syntax_highlighting()["theme"])
    Label(settings_window, text="主题:").pack(anchor=W)
    rawdata = os.listdir("./asset/theme/")
    themes = ["vscode-dark"]
    rawdata.remove("vscode-dark.json")
    for theme in rawdata:
        themes.append(theme.split('.')[0])

    OptionMenu(settings_window, theme_var, *themes).pack(anchor=W, fill=X)

    # 字体设置
    font_var = StringVar(value=Settings.Editor.font())
    Label(settings_window, text="字体:").pack(anchor=W)
    Entry(settings_window, textvariable=font_var).pack(anchor=W, fill=X)

    # 字体大小设置
    fontsize_var = IntVar(value=Settings.Editor.font_size())
    Label(settings_window, text="字体大小:").pack(anchor=W)
    Spinbox(settings_window, from_=8, to=72, textvariable=fontsize_var).pack(anchor=W, fill=X)

    # 主题设置
    theme_var.trace_add('write', lambda *args: apply_settings())
    font_var.trace_add('write', lambda *args: apply_settings())
    fontsize_var.trace_add('write', lambda *args: apply_settings())

    # 多语言支持
    lang_var = StringVar(value=Settings.Editor.lang)
    Label(settings_window, text="语言:").pack(anchor=W)
    OptionMenu(settings_window, lang_var, "Chinese", "English", "French", "German", "Japanese", "Russian").pack(anchor=W, fill=X)

    lang_var.trace_add('write', lambda *args: load_language(lang_var.get()))

    Button(settings_window, text="关闭", command=settings_window.destroy).pack(anchor=E)

# -------------------- UI Updates --------------------
def update_ui_text():
    """Update UI text"""
    # 菜单项配置字典
    # 菜单项配置字典
    menu_config = {
        'filemenu': {
            "0": "new_file",
            "1": "new_window",
            "3": "open_file",
            "4": "save_file",
            "5": "save_as_file",
            "6": "exit"
        },
        'editmenu': {
            "0": "undo",
            "1": "redo",
            "3": "copy",
            "4": "paste",
            "5": "delete"
        },
        'runmenu': {
            "0": "run",
            "1": "clear_output",
            "2": "terminal"
        },
        'settingsmenu': {
            "0": "open_settings"
        }
    }

    # 循环更新菜单项
    for menu_name, items in menu_config.items():
        menu = globals()[menu_name]
        for index, key in items.items():
            menu.entryconfig(index, label=lang_dict.get(key, key))

# -------------------- File Operations --------------------
def open_file():
    """File > Open File"""
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Python文件", "*.py"),
            ("HTML文件", "*.html"),
            ("CSS文件", "*.css"),
            ("JavaScript文件", "*.js"),
            ("JSON文件", "*.json"),
            ("Ruby文件", "*.rb"),
            ("C/C++文件", "*.c;*.cpp;*.h"),
            ("Objective-C文件", "*.m"),
            ("所有文件", "*.*")
        ]
    )
    codearea.delete(0.0, END)
    with open(file_path, encoding=Settings.Editor.file_encoding()) as f:
        content = f.read()
    codearea.insert(0.0, content)

    try:
        codehighlighter = highlighter_factory.create_highlighter(Settings.Editor.file_path(), codearea)
        
        # 检查主题文件是否存在
        theme_file = "./asset/theme/vscode-dark.json"
        if not os.path.exists(theme_file):
            logger.warning(f"Warning: Theme file {theme_file} not found, using default theme")
            # Use built-in default theme
            theme_data = {
                "base": {
                    "background": "#1E1E1E",
                    "foreground": "#D4D4D4",
                    "insertbackground": "#D4D4D4",
                    "selectbackground": "#264F78",
                    "selectforeground": "#D4D4D4"
                }
            }
        else:
            # 加载主题
            try:
                with open(theme_file, "r", encoding="utf-8") as f:
                    theme_data = json.load(f)
            except Exception as e:
                logger.warning(f"Warning: Failed to load theme file: {str(e)}, using default theme")
                theme_data = {
                    "base": {
                        "background": "#1E1E1E",
                        "foreground": "#D4D4D4",
                        "insertbackground": "#D4D4D4",
                        "selectbackground": "#264F78",
                        "selectforeground": "#D4D4D4"
                    }
                }
        
        codehighlighter.set_theme(theme_data)
        codehighlighter.highlight()

        # 对printarea使用相同的设置
        codehighlighter2 = highlighter_factory.create_highlighter(Settings.Editor.file_path(), printarea)
        codehighlighter2.set_theme(theme_data)
        codehighlighter2.highlight()
        
        def on_key(event):
            # 处理自动保存
            autosave()
            return None
        
        # 移除所有原有的按键绑定
        for binding in root.bind_all():
            if binding.startswith('<Key'):
                root.unbind_all(binding)
        
        # 添加新的按键绑定
        root.bind("<Key>", on_key, add="+")
        
    except Exception as e:
        logger.warning(f"Warning: Code highlighter initialization failed: {str(e)}")

def save_file():
    """File > Save File"""
    global file_path
    msg = codearea.get(0.0, END)
    if file_path == "./temp_script.txt":
        file_path = filedialog.asksaveasfilename(
                    filetypes=[
                        ("Python文件", "*.py"),
                        ("HTML文件", "*.html"),
                        ("CSS文件", "*.css"),
                        ("JavaScript文件", "*.js"),
                        ("JSON文件", "*.json"),
                        ("Ruby文件", "*.rb"),
                        ("C/C++文件", "*.c;*.cpp;*.h"),
                        ("Objective-C文件", "*.m"),
                        ("所有文件", "*.*")
                    ]
                )
        try:
            codehighlighter = highlighter_factory.create_highlighter(Settings.Editor.file_path(), codearea)
            
            # 检查主题文件是否存在
            theme_file = "./asset/theme/vscode-dark.json"
            if not os.path.exists(theme_file):
                logger.warning(f"Warning: Theme file {theme_file} not found, using default theme")
                # Use built-in default theme
                theme_data = {
                    "base": {
                        "background": "#1E1E1E",
                        "foreground": "#D4D4D4",
                        "insertbackground": "#D4D4D4",
                        "selectbackground": "#264F78",
                        "selectforeground": "#D4D4D4"
                    }
                }
            else:
                # 加载主题
                try:
                    with open(theme_file, "r", encoding="utf-8") as f:
                        theme_data = json.load(f)
                except Exception as e:
                    logger.warning(f"Warning: Failed to load theme file: {str(e)}, using default theme")
                    theme_data = {
                        "base": {
                            "background": "#1E1E1E",
                            "foreground": "#D4D4D4",
                            "insertbackground": "#D4D4D4",
                            "selectbackground": "#264F78",
                            "selectforeground": "#D4D4D4"
                        }
                    }
            
            codehighlighter.set_theme(theme_data)
            codehighlighter.highlight()

            # 对printarea使用相同的设置
            codehighlighter2 = highlighter_factory.create_highlighter(Settings.Editor.file_path(), printarea)
            codehighlighter2.set_theme(theme_data)
            codehighlighter2.highlight()
            
            def on_key(event):
                # 处理自动保存
                autosave()
                return None
            
            # 移除所有原有的按键绑定
            for binding in root.bind_all():
                if binding.startswith('<Key'):
                    root.unbind_all(binding)
            
            # 添加新的按键绑定
            root.bind("<Key>", on_key, add="+")
            
        except Exception as e:
            logger.warning(f"Warning: Code highlighter initialization failed: {str(e)}")
    else:
        print(file_path)

    with open(file_path, "w", encoding="utf-8") as fp:
        fp.write(msg)
    

def save_as_file():
    """File > Save As"""
    msg = codearea.get(0.0, END)
    file_path = filedialog.asksaveasfilename(
            filetypes=[
                ("Python文件", "*.py"),
                ("HTML文件", "*.html"),
                ("CSS文件", "*.css"),
                ("JavaScript文件", "*.js"),
                ("JSON文件", "*.json"),
                ("Ruby文件", "*.rb"),
                ("C/C++文件", "*.c;*.cpp;*.h"),
                ("Objective-C文件", "*.m"),
                ("所有文件", "*.*")
            ]
        )
    
    with open(file_path, "w", encoding="utf-8") as fp:
        fp.write(msg)

def new_file():
    """File > New File"""
    codearea.delete(0.0, END)

def new_window():
    """File > New Window"""
    subprocess.run([sys.executable, "main.py"])

# -------------------- Edit Operations --------------------
def copy():
    """Edit > Copy"""
    global copy_msg
    try:
        copy_msg = codearea.selection_get()
    except:
        try:
            copy_msg = printarea.selection_get()
        except:
            pass

def paste():
    """Edit > Paste"""
    try:
        codearea.insert("insert", copy_msg)
    except:
        pass

def delete():
    """Edit > Delete Selection"""
    try:
        codearea.delete("sel.first", "sel.last")
    except:
        pass

def undo():
    """Edit > Undo"""
    codearea.edit_undo()

def redo():
    """Edit > Redo"""
    codearea.edit_redo()

# -------------------- Run Operations --------------------
def run():
    """Run > Run Python File"""
    runtool = subprocess.Popen([sys.executable, Settings.Editor.file_path()], stdin=subprocess.PIPE, 
                           stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    
    # 获取printarea的内容并转换为字节
    input_data = inputarea.get(0.0, END).encode('utf-8')  # 转换为字节
    stdout, stderr = runtool.communicate(input=input_data)

    printarea.insert(END, f"%Run {Settings.Editor.file_path()}\n")
    printarea.insert(END, f"------------------Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}------------------\n")
    printarea.insert(END, stdout.decode())  # 解码为字符串
    # printarea.insert(END, stderr.decode())  # 解码为字符串

    printarea.insert(END, "\n>>> ")

def autosave():
    """File > Auto Save"""
    try:
        content = codearea.get("1.0", END)
        if Settings.Editor.file_path() != "./temp_script.txt":
            with open(Settings.Editor.file_path(), "w", encoding=Settings.Editor.file_encoding()) as f:
                f.write(content)
        
        with open("./temp_script.txt", "w", encoding=Settings.Editor.file_encoding()) as f:
            f.write(content)
    except Exception as e:
        print(f"自动保存失败：{str(e)}")

def clear_printarea():
    """Run > Clear Output"""
    printarea.delete(0.0, END)

def terminal():
    """Run > Open Terminal"""
    def execute(event=None):
        cmd = terminal.get("2.0", "end-1c").strip()
        if cmd:
            try:
                result = subprocess.run(cmd.split(), 
                                     capture_output=True, 
                                     text=True)
                terminal.insert("end", "\n" + result.stdout + result.stderr)
            except Exception as e:
                terminal.insert("end", "\n错误: " + str(e))
        terminal.insert("end", "\n$ ")
        return "break"  # 防止默认的回车行为

    window = Toplevel()  # 使用Toplevel替代Tk
    window.title("终端")
    window.geometry("600x400+100+100")
    terminal = Text(window)
    terminal.pack(fill=BOTH, expand=True)
    terminal.insert("end", "$ ")
    terminal.bind("<Return>", execute)

def download_plugin():
    """插件>下载插件"""
    try:
        plugin_path = filedialog.askopenfilename(
            title="打开插件",
            filetypes=[
                ("插件执行文件", "*.zip"),
                ("插件安装文件", "*.json"),
                ("所有文件", "*.*")
            ]
        )
        if plugin_path:
            plugin_zip = zipfile.ZipFile(plugin_path, "r")
            plugin_zip.extractall("./asset/plugins/")
            plugin_zip.close()
            messagebox.showinfo("插件", "插件安装成功，请重启软件")
    except Exception as e:
        messagebox.showerror("错误", f"插件安装失败：{str(e)}")

def exit_editor():
    """退出编辑器"""
    if messagebox.askokcancel("退出", "确定要退出吗？"):
        root.destroy()
        sys.exit(0)

# -------------------- 创建窗口和菜单 --------------------

# 创建主窗口
root = Tk()
root.title("火凤文本编辑器 Phoenix Notepad")
root.geometry("800x600+100+100")
root.configure(bg='black')
# root.iconbitmap(default="./asset/icon.ico")
root.resizable(width=True, height=True)

# 绑定快捷键
root.bind("<Control-c>", lambda event: copy())
root.bind("<Control-v>", lambda event: paste())
root.bind("<Control-x>", lambda event: delete())
root.bind("<Control-z>", lambda event: undo())
root.bind("<Control-y>", lambda event: redo())
root.bind("<F5>", lambda event: run())
root.bind("<Key>", lambda event: autosave())

# 创建所有菜单
menu = Menu()
root.config(menu=menu)

# 文件菜单
filemenu = Menu(tearoff=0)
menu.add_cascade(menu=filemenu, label="文件")
filemenu.add_command(command=new_file, label="新建文件")
filemenu.add_command(command=new_window, label="新建窗口")
filemenu.add_separator()
filemenu.add_command(command=open_file, label="打开文件")
filemenu.add_command(command=save_file, label="保存文件")
filemenu.add_command(command=save_as_file, label="另存为文件")
filemenu.add_separator()
filemenu.add_command(command=exit_editor, label="退出")

# 编辑菜单
editmenu = Menu(tearoff=0)
menu.add_cascade(menu=editmenu, label="编辑")
editmenu.add_command(command=undo, label="撤销")
editmenu.add_command(command=redo, label="重做")
editmenu.add_separator()
editmenu.add_command(command=copy, label="复制")
editmenu.add_command(command=paste, label="粘贴")
editmenu.add_command(command=delete, label="删除所选内容")

# 运行菜单
runmenu = Menu(tearoff=0)
menu.add_cascade(menu=runmenu, label="运行")
runmenu.add_command(command=run, label="运行")
runmenu.add_command(command=clear_printarea, label="清空输出")
runmenu.add_command(command=terminal, label="终端")

# 插件菜单
pluginmenu = Menu(tearoff=0)
menu.add_cascade(menu=pluginmenu, label="插件")

# 创建分割器
paned = PanedWindow(root, orient=VERTICAL)
paned.pack(fill=BOTH, expand=True)

# 创建代码区
codearea = Text(paned, font=Font(root, family="Consolas", size=12))
paned.add(codearea)

# 创建输出区域为终端
class Terminal(tk.Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(
            background='#1E1E1E',
            foreground='#D4D4D4',
            insertbackground='#D4D4D4',
            selectbackground='#264F78',
            selectforeground='#D4D4D4'
        )
        self.bind('<Return>', self._handle_return)
        self.prompt = ">>> "
        self.insert("1.0", self.prompt)
        
    def _handle_return(self, event):
        """Handle Enter key event"""
        current_pos = self.index("insert")
        line_start = f"{current_pos} linestart"
        command = self.get(line_start, "insert").lstrip(self.prompt)
        
        if command.strip():
            try:
                # 执行命令
                result = subprocess.run(
                    [sys.executable, '-c', command],
                    capture_output=True,
                    text=True
                )
                self.insert("end", "\n" + result.stdout)
                if result.stderr:
                    self.insert("end", "\n" + result.stderr)
            except Exception as e:
                self.insert("end", f"\n错误: {str(e)}")
            
        self.insert("end", f"\n{self.prompt}")
        return "break"

# 将终端添加到分割器
subpaned = PanedWindow(paned, orient=HORIZONTAL)
paned.add(subpaned)
inputarea = Terminal(subpaned, font=Font(root, family="Consolas", size=12))
subpaned.add(inputarea)
printarea = Terminal(subpaned, font=Font(root, family="Consolas", size=12))
subpaned.add(printarea)

# Show last edited content
try:
    with open("./temp_script.txt", "r", encoding="utf-8") as fp:
        codearea.insert("1.0", fp.read())
except FileNotFoundError:
    # If temp file doesn't exist, create an empty one
    with open("./temp_script.txt", "w", encoding="utf-8") as fp:
        fp.write("")

# Load language settings
with open(Settings.Editor.langfile(), "r", encoding="utf-8") as fp:
    lang_dict = json.load(fp)

# Setup auto-save timer
def schedule_autosave():
    autosave()
    root.after(5000, schedule_autosave)  # Auto-save every 5 seconds

# Start auto-save
schedule_autosave()

# 设置菜单
settingsmenu = Menu(tearoff=0)
menu.add_cascade(menu=settingsmenu, label="设置")
settingsmenu.add_command(command=open_settings_panel, label="打开设置面板")

# Now all menus are created, safe to call update_ui_text
# update_ui_text()

# 启动自动保存
schedule_autosave()

# Initialization
try:
    codehighlighter = highlighter_factory.create_highlighter(Settings.Editor.file_path(), codearea)
    
    # 检查主题文件是否存在
    theme_file = "./asset/theme/vscode-dark.json"
    if not os.path.exists(theme_file):
        logger.warning(f"Warning: Theme file {theme_file} not found, using default theme")
        # Use built-in default theme
        theme_data = {
            "base": {
                "background": "#1E1E1E",
                "foreground": "#D4D4D4",
                "insertbackground": "#D4D4D4",
                "selectbackground": "#264F78",
                "selectforeground": "#D4D4D4"
            }
        }
    else:
        # 加载主题
        try:
            with open(theme_file, "r", encoding="utf-8") as f:
                theme_data = json.load(f)
        except Exception as e:
            logger.warning(f"Warning: Failed to load theme file: {str(e)}, using default theme")
            theme_data = {
                "base": {
                    "background": "#1E1E1E",
                    "foreground": "#D4D4D4",
                    "insertbackground": "#D4D4D4",
                    "selectbackground": "#264F78",
                    "selectforeground": "#D4D4D4"
                }
            }
    
    codehighlighter.set_theme(theme_data)
    codehighlighter.highlight()

    # 对printarea使用相同的设置
    codehighlighter2 = highlighter_factory.create_highlighter(Settings.Editor.file_path(), printarea)
    codehighlighter2.set_theme(theme_data)
    codehighlighter2.highlight()
    
    def on_key(event):
        # 处理自动保存
        autosave()
        return None
    
    # 移除所有原有的按键绑定
    for binding in root.bind_all():
        if binding.startswith('<Key'):
            root.unbind_all(binding)
    
    # 添加新的按键绑定
    root.bind("<Key>", on_key, add="+")
    
except Exception as e:
    logger.warning(f"Warning: Code highlighter initialization failed: {str(e)}")


if __name__ == "__main__":
    n = 0
else:
    n = 1

# Start main loop
root.mainloop(n)
