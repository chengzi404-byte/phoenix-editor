from library.highlighter_factory import HighlighterFactory
from library.logger import setup_logger
from library.api import EditorAPI
from tkinter import messagebox
from tkinter import filedialog 
from tkinter.font import Font
from ttkbootstrap import (Window, Button, Text, 
                          Menu, Toplevel, StringVar, 
                          Label, OptionMenu, Entry, 
                          IntVar, Spinbox,PanedWindow,
                          END, VERTICAL, BOTH, E, W, X)
import os
import json
import subprocess
import sys
import zipfile
import traceback
import tkinter as tk


# -------------------- 全局变量 --------------------
global api, settings, highlighter_factory, file_path, logger
api = EditorAPI()
logger = setup_logger()
settings = api.settings
file_path = api.file_path  # 设置默认值
highlighter_factory = HighlighterFactory()

# -------------------- 初始化函数 --------------------
def initialize_application():
    """初始化应用程序"""
    try:
        # 检查目录
        check_required_directories()
        
        # 加载设置
        if not api.load_settings():
            logger.warning("无法加载设置，使用默认值")
            
        # 加载语言
        if not api.load_language(api.settings.get("lang", "zh-cn")):
            logger.warning("无法加载语言包，使用默认值")
            
        return True
    except Exception as e:
        logger.error(f"初始化失败: {str(e)}")
        return False

# -------------------- 初始化和设置 --------------------
def check_required_directories():
    """检查并创建必要的目录和文件"""
    required_dirs = [
        "./asset",
        "./asset/plugins",
        "./library/highlighter"
    ]
    for directory in required_dirs:
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

def load_language(lang):
    """加载语言文件"""
    lang_file = f"./asset/lang_{lang}.json"
    if os.path.exists(lang_file):
        with open(lang_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# -------------------- 设置面板相关函数 --------------------
def open_settings_panel():
    """打开设置面板"""
    settings_window = Toplevel()
    settings_window.title("设置")
    settings_window.geometry("400x300")

    def apply_settings():
        """立即应用设置"""
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
    theme_var = StringVar(value=api.settings.get("theme", "vscode-dark"))
    Label(settings_window, text="主题:").pack(anchor=W)
    rawdata = os.listdir("./asset/theme/")
    themes = ["vscode-dark"]
    rawdata.remove("vscode-dark.json")
    for theme in rawdata:
        themes.append(theme.split('.')[0])

    OptionMenu(settings_window, theme_var, *themes).pack(anchor=W, fill=X)

    # 字体设置
    font_var = StringVar(value=settings.get("font", "Fira Code"))
    Label(settings_window, text="字体:").pack(anchor=W)
    Entry(settings_window, textvariable=font_var).pack(anchor=W, fill=X)

    # 字体大小设置
    fontsize_var = IntVar(value=settings.get("fontsize", 18))
    Label(settings_window, text="字体大小:").pack(anchor=W)
    Spinbox(settings_window, from_=8, to=72, textvariable=fontsize_var).pack(anchor=W, fill=X)

    # 主题设置
    theme_var.trace_add('write', lambda *args: apply_settings())
    font_var.trace_add('write', lambda *args: apply_settings())
    fontsize_var.trace_add('write', lambda *args: apply_settings())

    # 多语言支持
    lang_var = StringVar(value=settings.get("lang", "zh-cn"))
    Label(settings_window, text="语言:").pack(anchor=W)
    OptionMenu(settings_window, lang_var, "zh-cn", "en", "es", "fr").pack(anchor=W, fill=X)

    lang_var.trace_add('write', lambda *args: load_language(lang_var.get()))

    # 编程语言设置
    code_var = StringVar(value=settings.get("code", "python"))
    Label(settings_window, text="编程语言：").pack(anchor=W)
    OptionMenu(settings_window, code_var, "python", "python", "c", "cpp", "bash", "java", "html", "javascript", "json", "ruby", "rust", "css", "objc")

    code_var.trace_add('write', lambda *args: apply_settings())

    Button(settings_window, text="关闭", command=settings_window.destroy).pack(anchor=E)

# -------------------- UI 更新 --------------------
def update_ui_text():
    """更新UI文本"""
    # 菜单项配置字典
    menu_config = {
        'filemenu': {
            0: "new_file",
            1: "new_window",
            3: "open_file",
            4: "save_file",
            5: "save_as_file",
            7: "exit"
        },
        'editmenu': {
            0: "undo",
            1: "redo",
            3: "copy",
            4: "paste",
            5: "delete"
        },
        'runmenu': {
            0: "run",
            1: "clear_output",
            2: "terminal"
        },
        'settingsmenu': {
            0: "open_settings"
        }
    }

    # 循环更新菜单项
    for menu_name, items in menu_config.items():
        menu = globals()[menu_name]
        for index, key in items.items():
            menu.entryconfig(index, label=lang_dict.get(key, key))

# -------------------- 文件操作相关函数 --------------------
def open_file():
    """文件>打开文件"""
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
    with open(file_path, encoding=api.file_encoding) as f:
        content = f.read()
    codearea.insert(0.0, content)

def save_file():
    """文件>保存文件"""
    global file_path
    msg = codearea.get(0.0, END)
    if file_path == "./temp_script.py":
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
    else:
        print(file_path)

    with open(file_path, "w", encoding="utf-8") as fp:
        fp.write(msg)
    

def save_as_file():
    """文件>另存为文件"""
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
    """文件>新建文件"""
    codearea.delete(0.0, END)

def new_window():
    """文件>新建窗口"""
    subprocess.run([sys.executable, "main.py"])

# -------------------- 编辑相关函数 --------------------
def copy():
    """编辑>复制"""
    global copy_msg
    try:
        copy_msg = codearea.selection_get()
    except:
        try:
            copy_msg = printarea.selection_get()
        except:
            pass

def paste():
    """编辑>粘贴"""
    try:
        codearea.insert("insert", copy_msg)
    except:
        pass

def delete():
    """编辑>删除所选内容"""
    try:
        codearea.delete("sel.first", "sel.last")
    except:
        pass

def undo():
    """编辑>撤销"""
    codearea.edit_undo()

def redo():
    """编辑>重做"""
    codearea.edit_redo()

# -------------------- 运行相关函数 --------------------
def run():
    """运行>运行Python文件"""
    runtool = subprocess.Popen([sys.executable, api.file_path], stdin=subprocess.PIPE, 
                           stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    
    # 获取printarea的内容并转换为字节
    input_data = printarea.get(0.0, END).encode('utf-8')  # 转换为字节
    stdout, stderr = runtool.communicate(input=input_data)

    printarea.insert(END, f"%Run {file_path}\n")
    printarea.insert(END, f"------------------Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}------------------\n")
    printarea.insert(END, stdout.decode())  # 解码为字符串
    # printarea.insert(END, stderr.decode())  # 解码为字符串

    printarea.insert(END, "\n>>> ")

def autosave():
    """文件>自动保存"""
    try:
        content = codearea.get("1.0", END)
        if api.file_path != "./temp_script.py":
            with open(api.file_path, "w", encoding=file_encoding) as f:
                f.write(content)
        
        with open("./temp_script.py", "w", encoding=file_encoding) as f:
            f.write(content)
    except Exception as e:
        print(f"自动保存失败：{str(e)}")

def clear_printarea():
    """运行>清空输出"""
    printarea.delete(0.0, END)

def terminal():
    """运行>打开终端"""
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
root = Window()
root.title("火凤文本编辑器 Phoenix Notepad")
root.geometry("800x600+100+100")
root.configure(bg='black')
root.iconbitmap(default="./asset/icon.ico")
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
        """处理回车事件"""
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
printarea = Terminal(paned, font=Font(root, family="Fira Code", size=12))
paned.add(printarea)

# 显示上一次编辑的内容
try:
    with open("./temp_script.py", "r", encoding="utf-8") as fp:
        codearea.insert("1.0", fp.read())
except FileNotFoundError:
    # 如果临时文件不存在，创建一个空文件
    with open("./temp_script.py", "w", encoding="utf-8") as fp:
        fp.write("")

# 加载插件
pluginlist = os.listdir("./asset/plugins/")
print(pluginlist)
pluginlist.remove("__init__.py")
for plugin in pluginlist:
    # 加载插件
    try:
        with open(f"./asset/plugins/{plugin}/des.json", "r", encoding="utf-8") as fp:
            plugin_data = json.load(fp)
    except Exception as e:
        logger.warning("警告: 插件设置文件不存在")
        logger.error(f"返回错误: {str(e)}")
        print(e)
        continue
    
    try:
        subprocess.run(f"python ./asset/plugins/{plugin}/{plugin_data["py_file"]}")
    except Exception as e:
        logger.warning("警告: 无运行文件")
        logger.error(f"返回错误: {str(e)}")
        print(e)

    exec(f"""def run_plugin_{plugin_data["uid"]}(): subprocess.run(plugin_data["commands"]["0"][0]) """)
    
    if len(plugin_data["commands"]) != 1:
        subpluginmenu = Menu(tearoff=0)
        pluginmenu.add_cascade(menu=subpluginmenu, label=plugin)
        for command in len(plugin_data["commands"]):
            subpluginmenu.add_command(command=subprocess.run(plugin_data["commands"][str(command)][0]), label=plugin_data["commands"][str(command)][1])
    else:
        exec(f"""pluginmenu.add_command(command=run_plugin_{plugin_data["uid"]}, label=plugin_data["commands"]["0"][1]) """)

# 加载语言设置
api.load_language(api.settings.get("lang", "zh-cn"))
lang_dict = api.lang_dict

# 读取设置
if not api.load_settings():
    logger.info("无法加载设置，使用默认值。")

file_encoding = settings.get("file-encoding", "utf-8")

# 加载语言设置
if not api.load_language(settings.get("lang", "zh-cn")):
    print("无法加载语言包，使用默认值。")
lang_dict = api.lang_dict

# 修改所有使用file_path的地方
if api.file_path == "./temp_script.py":
    api.file_path = file_path

# 修改所有使用copy_msg的地方
if codearea.tag_ranges("sel"):  # 检查是否有选中的文本
    api.copy_msg = codearea.selection_get()
else:
    api.copy_msg = ""  # 如果没有选中内容，设置为一个空字符串

# 修改所有使用settings的地方
if not api.load_settings():  # 确保设置成功加载
    logger.info("无法加载设置，使用默认值。")
    api.settings = {}  # 如果加载失败，设置为一个空字典

# 确保settings不为None
if api.settings is None:
    api.settings = {}

# 修改所有使用lang_dict的地方
api.load_language(lang_dict)

try:
    # 加载代码高亮工具
    highlighter_module = __import__(f"library.highlighter.{api.settings.get('code', 'python')}", fromlist=['CodeHighlighter'])
    CodeHighlighter = getattr(highlighter_module, 'CodeHighlighter')
except (ImportError, KeyError):
    # 如果加载失败，使用Python高亮器作为默认
    from library.highlighter.python import CodeHighlighter
    logger.warning(f"警告: 无法加载{api.settings.get('code', 'unknown')}高亮器，使用Python高亮器作为默认")

# 初始化代码高亮器
try:
    codehighlighter = CodeHighlighter(codearea)
    
    # 检查主题文件是否存在
    theme_file = "./asset/theme/vscode-dark.json"
    if not os.path.exists(theme_file):
        logger.warning(f"警告: 主题文件 {theme_file} 不存在，使用默认主题")
        # 使用内置的默认主题
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
            logger.warning(f"警告: 加载主题文件失败: {str(e)}，使用默认主题")
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
    codehighlighter2 = CodeHighlighter(printarea)
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
    logger.warning(f"警告: 代码高亮器初始化失败: {str(e)}")
    traceback.print_exc()  # 打印完整的错误堆栈

# 设置自动保存的定时器
def schedule_autosave():
    autosave()
    root.after(5000, schedule_autosave)  # 每5秒自动保存一次

# 启动自动保存
schedule_autosave()

# 设置菜单
settingsmenu = Menu(tearoff=0)
menu.add_cascade(menu=settingsmenu, label="设置")
settingsmenu.add_command(command=open_settings_panel, label="打开设置面板")

# 现在所有菜单都已创建，可以安全地调用update_ui_text
# update_ui_text()

# 启动自动保存
schedule_autosave()

if __name__ == "__main__":
    n = 0
else:
    n = 1

# 启动主循环
root.mainloop(n)
