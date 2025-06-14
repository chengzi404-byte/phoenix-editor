from library.highlighter_factory import HighlighterFactory
from library.logger import setup_logger
from library.api import Settings
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

# Load language settings
with open(Settings.Editor.langfile(), "r", encoding="utf-8") as fp:
    lang_dict = json.load(fp)

try:
    for directory in Settings.Init.required_dirs():
        if not os.path.exists(directory):
            os.makedirs(directory)
            
    # Check and create the normal files
    if not os.path.exists("./asset/settings.json"):
        default_settings = {
            "file-encoding": "utf-8",
            "lang": "zh-cn",
            "font": "Consolas",
            "fontsize": 12,
            "code": "python",  # Use the python highlighter as normal
            "syntax-highlighting": {
                "theme": "vscode-dark",
                "enable-type-hints": True,
                "enable-docstrings": True
            }
        }
        with open("./asset/settings.json", "w", encoding="utf-8") as f:
            json.dump(default_settings, f, indent=4, ensure_ascii=False)

except Exception as e:
    logger.error(f"Initlaze failed: {str(e)}")

# -------------------- Settings Panel Functions --------------------
def open_settings_panel():
    """Open Settings Panel"""
    settings_window = Toplevel()
    settings_window.title(lang_dict["settings"]["title"])
    settings_window.geometry("400x300")

    def apply_settings():
        """Apply settings immediately"""
        theme_name = theme_var.get()
        # Load theme file
        theme_file = f"./asset/theme/{theme_name}.json"
        try:
            # Apply changes
            with open(theme_file, "r", encoding="utf-8") as f:
                theme_data = json.load(f)
            codehighlighter.set_theme(theme_data)
            codearea.configure(font=Font(settings_window, family=font_var.get(), size=fontsize_var.get()))
        except Exception as e:
            print(f"Use theme failed: {str(e)}")
    
    def apply_lang():
        lang_file = lang_var.get()
        Settings.Editor.change("lang", lang_file)
        messagebox.showinfo(lang_dict["info-window-title"], lang_dict["settings"]["restart"])

    # Theme
    theme_var = StringVar(value=Settings.Highlighter.syntax_highlighting()["theme"])
    Label(settings_window, text=lang_dict["settings"]["theme"]).pack(anchor=W)
    rawdata = os.listdir("./asset/theme/")
    themes = ["vscode-dark"]
    rawdata.remove("vscode-dark.json")
    for theme in rawdata:
        themes.append(theme.split('.')[0])

    OptionMenu(settings_window, theme_var, *themes).pack(anchor=W, fill=X)

    # Font
    font_var = StringVar(value=Settings.Editor.font())
    Label(settings_window, text=lang_dict["settings"]["font"]).pack(anchor=W)
    Entry(settings_window, textvariable=font_var).pack(anchor=W, fill=X)

    # Font size
    fontsize_var = IntVar(value=Settings.Editor.font_size())
    Label(settings_window, text=lang_dict["settings"]["font-size"]).pack(anchor=W)
    Spinbox(settings_window, from_=8, to=72, textvariable=fontsize_var).pack(anchor=W, fill=X)

    # Apply settings immediatly
    theme_var.trace_add('write', lambda *args: apply_settings())
    font_var.trace_add('write', lambda *args: apply_settings())
    fontsize_var.trace_add('write', lambda *args: apply_settings())

    # Multi-languange support
    lang_var = StringVar(value=Settings.Editor.lang)
    Label(settings_window, text=lang_dict["settings"]["languange"]).pack(anchor=W)
    OptionMenu(settings_window, lang_var, "Chinese", "English", "French", "German", "Japanese", "Russian").pack(anchor=W, fill=X)

    lang_var.trace_add('write', lambda *args: apply_lang())

    Button(settings_window, text=lang_dict["settings"]["close"], command=settings_window.destroy).pack(anchor=E)

# -------------------- File Operations --------------------
def open_file():
    """File > Open File"""
    global file_path
    file_path = filedialog.askopenfilename(
        filetypes=[
            (lang_dict["file-types"][0], "*.py"),
            (lang_dict["file-types"][1], "*.html"),
            (lang_dict["file-types"][2], "*.css"),
            (lang_dict["file-types"][3], "*.js"),
            (lang_dict["file-types"][4], "*.json"),
            (lang_dict["file-types"][5], "*.rb"),
            (lang_dict["file-types"][6], "*.c;*.cpp;*.h"),
            (lang_dict["file-types"][7], "*.m"),
            (lang_dict["file-types"][8], "*.*")
        ]
    )
    codearea.delete(0.0, END)
    with open(file_path, encoding=Settings.Editor.file_encoding()) as f:
        content = f.read()
    codearea.insert(0.0, content)

    try:
        codehighlighter = highlighter_factory.create_highlighter(Settings.Editor.file_path(), codearea)
        
        # Check theme file
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
            # Load theme
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

        # Use the same settings for printarea
        codehighlighter2 = highlighter_factory.create_highlighter(Settings.Editor.file_path(), printarea)
        codehighlighter2.set_theme(theme_data)
        codehighlighter2.highlight()
        
        def on_key(event):
            # Handle auto-saving
            autosave()
            return None
        
        # Remove all existing key bindings
        for binding in root.bind_all():
            if binding.startswith('<Key'):
                root.unbind_all(binding)
        
        # Add new key bindings
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
                        (lang_dict["file-types"][0], "*.py"),
                        (lang_dict["file-types"][1], "*.html"),
                        (lang_dict["file-types"][2], "*.css"),
                        (lang_dict["file-types"][3], "*.js"),
                        (lang_dict["file-types"][4], "*.json"),
                        (lang_dict["file-types"][5], "*.rb"),
                        (lang_dict["file-types"][6], "*.c;*.cpp;*.h"),
                        (lang_dict["file-types"][7], "*.m"),
                        (lang_dict["file-types"][8], "*.*")
                    ]
                )
        try:
            codehighlighter = highlighter_factory.create_highlighter(Settings.Editor.file_path(), codearea)
            
            # Check if the theme file exists
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
                # Load theme
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

            # Use the same settings for printarea
            codehighlighter2 = highlighter_factory.create_highlighter(Settings.Editor.file_path(), printarea)
            codehighlighter2.set_theme(theme_data)
            codehighlighter2.highlight()
            
            def on_key(event):
                # Handle auto-saving
                autosave()
                return None
            
            # Remove all existing key bindings
            for binding in root.bind_all():
                if binding.startswith('<Key'):
                    root.unbind_all(binding)
            
            # Add new key bindings
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
                (lang_dict["file-types"][0], "*.py"),
                (lang_dict["file-types"][1], "*.html"),
                (lang_dict["file-types"][2], "*.css"),
                (lang_dict["file-types"][3], "*.js"),
                (lang_dict["file-types"][4], "*.json"),
                (lang_dict["file-types"][5], "*.rb"),
                (lang_dict["file-types"][6], "*.c;*.cpp;*.h"),
                (lang_dict["file-types"][7], "*.m"),
                (lang_dict["file-types"][8], "*.*")
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
    
    # Get the content of printarea and convert it to bytes
    input_data = inputarea.get(0.0, END).encode('utf-8')  # 转换为字节
    stdout, stderr = runtool.communicate(input=input_data)

    printarea.delete(0.0, END)
    printarea.insert(END, f"%Run {Settings.Editor.file_path()}\n")
    printarea.insert(END, f"------------------Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}------------------\n")
    printarea.insert(END, stdout.decode(errors="replace"))  # Decode as a string
    printarea.insert(END, stderr.decode(errors="replace"))  # Decode as a string

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
        print(f"Auto-saving failed: {str(e)}")

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
                terminal.insert("end", "ERR: " + str(e))
        terminal.insert("end", "\n$ ")
        return "break"  # Prevent the default enter behavior

    window = Toplevel()  # Use Toplevel instead of Tk
    window.title("终端")
    window.geometry("600x400+100+100")
    terminal = Text(window)
    terminal.pack(fill=BOTH, expand=True)
    terminal.insert("end", "$ ")
    terminal.bind("<Return>", execute)

def download_plugin():
    """Plugin > Download plugin"""
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
            messagebox.showinfo("Plugin", "Plugin installation successful, please restart the software")
    except Exception as e:
        messagebox.showerror("Error", f"Plugin installation failed: {str(e)}")

def exit_editor():
    """Exit"""
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()
        sys.exit(0)

# -------------------- Create the window and menus --------------------

# Create the main window
root = Tk()
root.title(lang_dict["title"])
root.geometry("800x600+100+100")
root.configure(bg='black')
# root.iconbitmap(default="./asset/icon.ico")
root.resizable(width=True, height=True)

# Binding
root.bind("<Control-c>", lambda event: copy())
root.bind("<Control-v>", lambda event: paste())
root.bind("<Control-x>", lambda event: delete())
root.bind("<Control-z>", lambda event: undo())
root.bind("<Control-y>", lambda event: redo())
root.bind("<F5>", lambda event: run())
root.bind("<Key>", lambda event: autosave())

# Create all the menus
menu = Menu()
root.config(menu=menu)

# File menu
filemenu = Menu(tearoff=0)
menu.add_cascade(menu=filemenu, label=lang_dict["menus"]["file"])
filemenu.add_command(command=new_file, label=lang_dict["menus"]["new-file"])
filemenu.add_command(command=new_window, label=lang_dict["menus"]["new-window"])
filemenu.add_separator()
filemenu.add_command(command=open_file, label=lang_dict["menus"]["open-file"])
filemenu.add_command(command=save_file, label=lang_dict["menus"]["save-file"])
filemenu.add_command(command=save_as_file, label=lang_dict["menus"]["save-as-file"])
filemenu.add_separator()
filemenu.add_command(command=exit_editor, label=lang_dict["menus"]["exit"])

# Edit menu
editmenu = Menu(tearoff=0)
menu.add_cascade(menu=editmenu, label=lang_dict["menus"]["edit"])
editmenu.add_command(command=undo, label=lang_dict["menus"]["undo"])
editmenu.add_command(command=redo, label=lang_dict["menus"]["redo"])
editmenu.add_separator()
editmenu.add_command(command=copy, label=lang_dict["menus"]["copy"])
editmenu.add_command(command=paste, label=lang_dict["menus"]["paste"])
editmenu.add_command(command=delete, label=lang_dict["menus"]["delete"])

# Run menu
runmenu = Menu(tearoff=0)
menu.add_cascade(menu=runmenu, label=lang_dict["menus"]["run"])
runmenu.add_command(command=run, label=lang_dict["menus"]["run"])
runmenu.add_command(command=clear_printarea, label=lang_dict["menus"]["clear-output"])
runmenu.add_command(command=terminal, label=lang_dict["menus"]["terminal"])

# Plugin menu (comming soon)
pluginmenu = Menu(tearoff=0)
menu.add_cascade(menu=pluginmenu, label=lang_dict["menus"]["plugin"])

# Help menu
menu.add_command(label="帮助", command=lambda: messagebox.showinfo(lang_dict["info-window-title"], lang_dict["help"]))

# Create the paned window
paned = PanedWindow(root, orient=VERTICAL)
paned.pack(fill=BOTH, expand=True)

# Create the code area
codearea = Text(paned, font=Font(root, family="Consolas", size=12))
paned.add(codearea)

subpaned = PanedWindow(paned, orient=HORIZONTAL)
paned.add(subpaned)
inputarea = Text(subpaned, font=Font(root, family="Consolas", size=12))
subpaned.add(inputarea)
printarea = Text(subpaned, font=Font(root, family="Consolas", size=12))
subpaned.add(printarea)

# Show last edited content
try:
    with open("./temp_script.txt", "r", encoding="utf-8") as fp:
        codearea.insert("1.0", fp.read())
except FileNotFoundError:
    # If temp file doesn't exist, create an empty one
    with open("./temp_script.txt", "w", encoding="utf-8") as fp:
        fp.write("")

# Setup auto-save timer
def schedule_autosave():
    autosave()
    root.after(5000, schedule_autosave)  # Auto-save every 5 seconds

# Start auto-save
schedule_autosave()

# Configure menu
settingsmenu = Menu(tearoff=0)
menu.add_cascade(menu=settingsmenu, label=lang_dict["menus"]["configure"])
settingsmenu.add_command(command=open_settings_panel, label=lang_dict["menus"]["open-settings"])

# Enable autosave
schedule_autosave()

# Initialization
try:
    codehighlighter = highlighter_factory.create_highlighter(Settings.Editor.file_path(), codearea)
    
    # Check 
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
        # Load theme
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

    # Use the same configure to the terminal
    codehighlighter2 = highlighter_factory.create_highlighter(Settings.Editor.file_path(), printarea)
    codehighlighter2.set_theme(theme_data)
    codehighlighter2.highlight()

    codehighlighter3 = highlighter_factory.create_highlighter(Settings.Editor.file_path(), inputarea)
    codehighlighter3.set_theme(theme_data)
    codehighlighter3.highlight()
    
    def on_key(event):
        # Process auto-save
        autosave()
        return None
    
    # Remove all the key binds
    for binding in root.bind_all():
        if binding.startswith('<Key'):
            root.unbind_all(binding)
    
    # Add new key bind
    root.bind("<Key>", on_key, add="+")
    
except Exception as e:
    logger.warning(f"Warning: Code highlighter initialization failed: {str(e)}")


if __name__ == "__main__":
    n = 0
else:
    n = 1

# Start main loop
root.mainloop(n)
