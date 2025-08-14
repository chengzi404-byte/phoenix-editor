debug = True # Debug

from library.highlighter_factory import HighlighterFactory
from library.logger import setup_logger
from library.api import Settings
from tkinter import messagebox
from tkinter import filedialog 
from tkinter.font import Font
from tkinter import (
    Tk, Toplevel, 
    StringVar, IntVar, 
    Menu, Text,
    W, X, E, BOTH, VERTICAL, HORIZONTAL, END,
    Frame, Label, Button, Scrollbar, DISABLED, NORMAL
)
from tkinter.ttk import *
from pathlib import Path
from library.thridPartyLicense import show as tplshow
import os
import json
import subprocess
import sys
import shutil
import requests
import threading
import time
import easygui
import zipfile
import shlex
from queue import Queue
import locale
import importlib

if debug:
    import traceback

# -------------------- Global Variables --------------------
global settings, highlighter_factory, file_path, logger
global codehighlighter2, codehighlighter, APIKEY
global ai_sidebar, ai_display, ai_input, ai_queue, ai_loading
logger = setup_logger()
highlighter_factory = HighlighterFactory()
file_path = "temp_script.txt"
ai_queue = Queue()  # AI QUEUE
ai_loading = False  # AI LOAD

with open(f"{Path.cwd() / "asset" / "settings.json"}", "r", encoding="utf-8") as fp:
    settings = json.load(fp)

# Load language settings
lang = locale.getdefaultlocale()[0]
if lang == "zh_CN":
    lang = "Chinese"
elif lang == "en_US":
    lang = "English"
elif lang == "fr_FR":
    lang = "French"
elif lang == "de_DE":
    lang = "German"
elif lang == "ja_JP":
    lang = "Japanese"
elif lang == "ru_RU":
    lang = "Russian"
else: # Default setting
    lang = "English"
Settings.Editor.change("lang", lang)
with open(Settings.Editor.langfile(), "r", encoding="utf-8") as fp:
    lang_dict = json.load(fp)

if not debug:
    try:
        APIKEY = Settings.AI.get_api_key()
    except KeyError:
        APIKEY = easygui.enterbox("API KEY: ", "API KEY:")

with open(f"{Path.cwd() / "asset" / "packages" / "themes.dark.json"}", "r", encoding="utf-8") as fp:
    dark_themes = json.load(fp)

with open(f"{Path.cwd() / "asset" / "theme" / "terminalTheme" / "dark.json"}", "r", encoding="utf-8") as fp:
    dark_terminal_theme = json.load(fp)

with open(f"{Path.cwd() / "asset" / "theme" / "terminalTheme" / "light.json"}", "r", encoding="utf-8") as fp:
    light_terminal_theme = json.load(fp)

# -------------------- AI Functions --------------------
def send_ai_request_to_api(prompt):
    global ai_loading
    ai_loading = True
    update_ai_loading()
    
    try:
        headers = {
            "Authorization": f"Bearer {APIKEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        response = requests.post(
            "https://api.siliconflow.cn/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result["choices"][0]["message"]["content"]
            ai_queue.put(ai_response)
        else:
            error_msg = f"AI Error: {response.status_code}, {response.text}"
            logger.error(error_msg)
            ai_queue.put(error_msg)
            
    except Exception as e:
        error_msg = f"AI Responce Error: {str(e)}"
        logger.error(error_msg)
        ai_queue.put(error_msg)
    finally:
        ai_loading = False
        update_ai_loading()

def process_ai_responses():
    while not ai_queue.empty():
        response = ai_queue.get()
        display_ai_response(response)
        ai_queue.task_done()
    root.after(100, process_ai_responses)

def display_ai_response(response):
    current_time = time.strftime("%H:%M:%S")
    ai_display.config(state=NORMAL)
    ai_display.insert(END, f"AI [{current_time}]:\n{response}\n\n")
    ai_display.see(END)
    ai_display.config(state=DISABLED)

def update_ai_loading():
    if ai_loading:
        ai_send_button.config(text=lang_dict["ai"]["sending"], state=DISABLED)
    else:
        ai_send_button.config(text=lang_dict["ai"]["send"], state=NORMAL)

def on_ai_input_enter(event):
    send_ai_request()

def send_ai_request():
    prompt = ai_input.get()
    if not prompt:
        return
        
    current_time = time.strftime("%H:%M:%S")
    ai_display.config(state=NORMAL)
    ai_display.insert(END, f"用户 [{current_time}]:\n{prompt}\n\n")
    ai_display.see(END)
    ai_display.config(state=DISABLED)
    
    ai_input.delete(0, END)
    
    threading.Thread(target=send_ai_request_to_api, args=(prompt,), daemon=True).start()

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
        theme_file = f"{Path.cwd() / "asset" / "theme" / theme_name}.json"
        try:
            # Apply changes
            with open(theme_file, "r", encoding="utf-8") as f:
                theme_data = json.load(f)
            codehighlighter.set_theme(theme_data)
            codearea.configure(font=Font(settings_window, family=font_var.get(), size=fontsize_var.get()))

            with open(f"{Path.cwd() / "asset" / "packages" / "themes.dark.json"}", "r", encoding="utf-8") as fp:
                dark_themes = json.load(fp)
            
            with open(f"{Path.cwd() / "asset" / "theme" / "terminalTheme" / "dark.json"}", "r", encoding="utf-8") as fp:
                dark_terminal_theme = json.load(fp)
            
            with open(f"{Path.cwd() / "asset" / "theme" / "terminalTheme" / "light.json"}", "r", encoding="utf-8") as fp:
                light_terminal_theme = json.load(fp)

            if Settings.Highlighter.syntax_highlighting()["theme"] in dark_themes: codehighlighter2.set_theme(dark_terminal_theme)
            else: codehighlighter2.set_theme(light_terminal_theme)

            if Settings.Highlighter.syntax_highlighting()["theme"] in dark_themes: codehighlighter3.set_theme(dark_terminal_theme)
            else: codehighlighter3.set_theme(light_terminal_theme)

            # Write changes
            Settings.Highlighter.change("theme", theme_name)
            Settings.Editor.change("font", font_var.get())
            
            # Update
            update_ai_sidebar_theme()

        except Exception as e:
            logger.info(f"Use theme failed: {str(e)}")
    
    def apply_restart_settings():
        lang_file = lang_var.get()
        code_type = code_var.get()
        Settings.Editor.change("lang", lang_file)
        Settings.Highlighter.change("code", code_type)
        messagebox.showinfo(lang_dict["info-window-title"], lang_dict["settings"]["restart"])

    def clear_cache():
        shutil.rmtree(f"{Path.cwd() / "library/__pycache__/"}")

    # Theme
    theme_var = StringVar(value=Settings.Highlighter.syntax_highlighting()["theme"])
    Label(settings_window, text=lang_dict["settings"]["theme"]).pack(anchor=W)
    rawdata = os.listdir(f"{Path.cwd() / "asset" / "theme"}")
    themes = []
    rawdata.remove("terminalTheme")
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
    lang_var = StringVar(value=Settings.Editor.lang())
    Label(settings_window, text=lang_dict["settings"]["languange"]).pack(anchor=W)
    OptionMenu(settings_window, lang_var, "Chinese", "English", "French", "German", "Japanese", "Russian").pack(anchor=W, fill=X)

    lang_var.trace_add('write', lambda *args: apply_restart_settings())

    # Code settings
    code_var = StringVar(value=Settings.Highlighter.syntax_highlighting()["code"])
    with open(f"{Path.cwd() / "asset" / "packages" / "code_support.json"}", "r", encoding="utf-8") as fp:
        support_code_type = json.load(fp)
    Label(settings_window, text=lang_dict["settings"]["coding-languange"]).pack(anchor=W)
    OptionMenu(settings_window, code_var, *support_code_type).pack(anchor=W, fill=X)

    code_var.trace_add('write', lambda *args: apply_restart_settings())

    # Clear cache
    Button(settings_window, text=lang_dict["settings"]["clear-cache"], command=clear_cache).pack(anchor=E)

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

def save_file():
    """File > Save File"""
    global file_path
    msg = codearea.get(0.0, END)
    if file_path == "temp_script.txt":
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
    def execute_in_thread():
        try:
            # Dymanic import
            module = importlib.import_module(f"asset.packages.run.{Settings.Highlighter.syntax_highlighting()['code']}")
            stdout, stderr, returncode = module.runFile(file_path)
            update_printarea(stdout, stderr, returncode=returncode)
        except FileNotFoundError:
            root.after(0, lambda: printarea.insert(END, "Error: File not found.\n"))
            messagebox.showerror("Error", "File not found. Please check the file path.")
        except Exception as e:
            root.after(0, lambda: printarea.insert(END, f"Execution error: {str(e)}\n"))
            messagebox.showerror("Error", f"Execution error: {str(e)}")

    def update_printarea(stdout, stderr, returncode=0):
        printarea.delete(0.0, END)
        printarea.insert(END, stdout.decode(errors="replace")+'\n')
        printarea.insert(END, stderr.decode(errors="replace")+'\n')
        printarea.insert(END, f"\nReturn code: {returncode}\n")

    threading.Thread(target=execute_in_thread, daemon=True).start()

def autosave():
    """File > Auto Save"""
    try:
        content = codearea.get("1.0", END)
        if Settings.Editor.file_path() != "temp_script.txt":
            with open(Settings.Editor.file_path(), "w", encoding=Settings.Editor.file_encoding()) as f:
                f.write(content)
        
        with open("temp_script.txt", "w", encoding=Settings.Editor.file_encoding()) as f:
            f.write(content)
    except Exception as e:
        logger.info(f"Auto-saving failed: {str(e)}")

def clear():
    """Run > Clear Output"""
    printarea.delete(0.0, END)

def download_plugin():
    """Plugin > Download plugin"""
    try:
        plugin_path = filedialog.askopenfilename(
            title="Open",
            filetypes=[
                (lang_dict["plugin-types"][0], "*.zip"),
                (lang_dict["plugin-types"][1], "*.*")
            ]
        )
        if plugin_path:
            plugin_zip = zipfile.ZipFile(plugin_path, "r")
            plugin_zip.extractall(f"{Path.cwd() / "asset" / "plugins"}")
            plugin_zip.close()
            messagebox.showinfo("Plugin", "Plugin installation successful, please restart the software")
    except Exception as e:
        messagebox.showerror("Error", f"Plugin installation failed: {str(e)}")

def exit_editor():
    """Exit"""
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()
        sys.exit(0)

def execute_commands():
    """Excute commands in commandarea"""
    command = commandarea.get()
    try:
        args = shlex.split(command)
        runtool = subprocess.Popen(args, stdin=subprocess.PIPE, 
                                   stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                                   shell=True)
        
        stdout, stderr = runtool.communicate()

        printarea.delete(0.0, END)
        printarea.insert(END, stdout.decode(errors="replace"))  # Decode as a string
        printarea.insert(END, stderr.decode(errors="replace"))  # Decode as a string
    except Exception as e:
        printarea.insert(END, f"Execution error: {str(e)}\n")
        messagebox.showerror("Error", f"Execution error: {str(e)}")

def show_current_file_dir():
    """show current file dir(absoult)"""
    messagebox.showinfo(file_path, file_path)

def helpFunction():
    """Help"""
    from library.thridPartyLicense import show
    window = Toplevel()
    Label(window, text=lang_dict["help"]).grid(column=0, row=0)
    Button(window, text="LICENSE..", command=show).grid(column=0, row=1)

# -------------------- Create the window and menus --------------------

# Create the main window
root = Tk()
root.title(lang_dict["title"])
root.geometry("1920x980+0+0")
root.configure(bg='black')
root.resizable(width=True, height=True)

# Binding
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
filemenu.add_command(command=show_current_file_dir, label=lang_dict["menus"]["show-file-dir"])
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
runmenu.add_command(command=clear, label=lang_dict["menus"]["clear-output"])

# Pop menu
popmenu = Menu(root, tearoff=0)
popmenu.add_command(label=lang_dict["menus"]["copy"], command=copy)
popmenu.add_command(label=lang_dict["menus"]["paste"], command=paste)
popmenu.add_command(label=lang_dict["menus"]["undo"], command=undo)
popmenu.add_command(label=lang_dict["menus"]["redo"], command=redo)

# Plugin menu (comming soon)
pluginmenu = Menu(tearoff=0)
menu.add_cascade(menu=pluginmenu, label=lang_dict["menus"]["plugin"])

# AI menu
aimenu = Menu(tearoff=0)
menu.add_cascade(menu=aimenu, label="AI")
aimenu.add_command(command=lambda: ai_sidebar.pack(side="right", fill="y"), label=lang_dict["ai"]["show"])
aimenu.add_command(command=lambda: ai_sidebar.pack_forget(), label=lang_dict["ai"]["hide"])

# Settings menu
settingsmenu = Menu(tearoff=0)
menu.add_cascade(menu=settingsmenu, label=lang_dict["menus"]["help"])
settingsmenu.add_command(label=lang_dict["menus"]["help"], command=helpFunction)
settingsmenu.add_command(command=open_settings_panel, label=lang_dict["menus"]["open-settings"])
settingsmenu.add_command(command=tplshow, label="TPL")

# Create the main paned window
main_paned = PanedWindow(root, orient=HORIZONTAL)
main_paned.pack(fill=BOTH, expand=True)

# Create the code area paned window
code_paned = PanedWindow(main_paned, orient=VERTICAL)
main_paned.add(code_paned)

# Create the code area
codearea = Text(code_paned, font=Font(root, family=Settings.Editor.font(), size=Settings.Editor.font_size()))
code_paned.add(codearea)

subpaned = PanedWindow(code_paned, orient=HORIZONTAL)
code_paned.add(subpaned)
inputarea = Text(subpaned, font=Font(root, family=Settings.Editor.font(), size=Settings.Editor.font_size()))
subpaned.add(inputarea)
printarea = Text(subpaned, font=Font(root, family=Settings.Editor.font(), size=Settings.Editor.font_size()))
subpaned.add(printarea)

commandpaned = PanedWindow(code_paned, orient=HORIZONTAL)
code_paned.add(commandpaned, weight=2)
commandarea = Entry(commandpaned, font=Font(root, family=Settings.Editor.font(), size=Settings.Editor.font_size()))
commandpaned.add(commandarea,weight=18)
executebutton = Button(text=lang_dict["menus"]["run"], command=execute_commands)
commandpaned.add(executebutton, weight=1)

# Config commandpaned widgets background color
if Settings.Highlighter.syntax_highlighting()["theme"] in dark_themes:
    commandarea.config(background="#2F4F4F")
else:
    commandarea.config(background="#F8F8F8")

# Show last edited content
try:
    with open("temp_script.txt", "r", encoding="utf-8") as fp:
        codearea.insert("1.0", fp.read())
except FileNotFoundError:
    # If temp file doesn't exist, create an empty one
    with open("temp_script.txt", "w", encoding="utf-8") as fp:
        fp.write("")

# -------------------- AI Sidebar Implementation --------------------
def update_ai_sidebar_theme():
    if Settings.Highlighter.syntax_highlighting()["theme"] in dark_themes:
        ai_display.config(bg="#1E1E1E", fg="#D4D4D4", insertbackground="#D4D4D4")
    else:
        ai_display.config(bg="#F8F8F8", fg="#000000", insertbackground="#000000")

# Ai sidebar
ai_sidebar = Frame(main_paned, width=300)
main_paned.add(ai_sidebar)

# Set position
def set_sash_position():
    try:
        main_paned.sashpos(1, 1600)
    except Exception as e:
        logger.warning("Sash position loading failed!")

root.after(100, set_sash_position)  # Delay

# AI Title
ai_title = Label(ai_sidebar, text="AI助手", font=Font(ai_sidebar, size=14, weight="bold"))
ai_title.pack()

# AI Display area
ai_display_frame = Frame(ai_sidebar)
ai_display_frame.pack(fill=BOTH, expand=True)

ai_display_scroll = Scrollbar(ai_display_frame)
ai_display_scroll.pack(side="right", fill="y")

ai_display = Text(ai_display_frame, wrap="word", height=20, 
                  font=Font(ai_sidebar, family=Settings.Editor.font(), size=Settings.Editor.font_size()))
ai_display.pack(side="left", fill=BOTH, expand=True)
ai_display.config(state=DISABLED)

ai_display_scroll.config(command=ai_display.yview)
ai_display.config(yscrollcommand=ai_display_scroll.set)

# AI Input area
ai_input_frame = Frame(ai_sidebar)
ai_input_frame.pack(fill=X, padx=10, pady=(0, 10))

ai_input = Entry(ai_input_frame, font=Font(ai_sidebar, family=Settings.Editor.font(), size=Settings.Editor.font_size()))
ai_input.pack(side="left", fill=X, expand=True, padx=(0, 10))
ai_input.bind("<Return>", on_ai_input_enter)

ai_send_button = Button(ai_input_frame, text=lang_dict["ai"]["send"], command=send_ai_request)
ai_send_button.pack(side="right")

update_ai_sidebar_theme()

# -------------------- Initlaze Ai Module --------------------
# Start ai response processing
process_ai_responses()

# Setup auto-save timer
def schedule_autosave():
    """自动保存定时器"""
    autosave()
    root.after(5000, schedule_autosave)  # Auto-save every 5 seconds

# Start auto-save
schedule_autosave()

# Enable autosave
schedule_autosave()

# Bind popup event
def show_popup(event):
    """Show popup"""
    popmenu.post(event.x_root, event.y_root)

codearea.bind("<Button-3>", show_popup)

# Initialization
try:
    codehighlighter = highlighter_factory.create_highlighter(codearea)
    
    # Check 
    theme_file = f"{Path.cwd() / "asset" / "theme" / Settings.Highlighter.syntax_highlighting()["theme"]}.json"
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
    codehighlighter2 = highlighter_factory.create_highlighter(printarea)
    if Settings.Highlighter.syntax_highlighting()["theme"] in dark_themes: codehighlighter2.set_theme(dark_terminal_theme)
    else: codehighlighter2.set_theme(light_terminal_theme)
    codehighlighter2.highlight()

    codehighlighter3 = highlighter_factory.create_highlighter(inputarea)
    if Settings.Highlighter.syntax_highlighting()["theme"] in dark_themes: codehighlighter3.set_theme(dark_terminal_theme)
    else: codehighlighter3.set_theme(light_terminal_theme)
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


root.mainloop()

print("Traceback (most recent call last):") if debug else None
traceback.print_exc() if debug else None

print("Traceback (stack):") if debug else None
traceback.print_stack() if debug else None