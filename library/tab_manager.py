from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.font import Font
import os
from .file_icons import FileIcons

class TabManager:
    def __init__(self, root, highlighter_factory):
        self.root = root
        self.highlighter_factory = highlighter_factory
        self.file_icons = FileIcons()
        
        # Create notebook widget
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Save opened tabs
        self.tabs = {}  # {tab_id: {"widget": widget, "file": file_path, "modified": bool}}
        
        # Bind events
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        
    def add_tab(self, file_path=None, content=""):
        """Add tab"""
        # Create editor widget
        editor = ScrolledText(self.notebook, font=Font(family="Consolas", size=12))
        editor.insert("1.0", content)
        
        if not file_path:
            file_path = f"未命名-{len(self.tabs) + 1}.txt"
            
        # Get file icon
        icon = self.file_icons.get_icon(file_path)
        
        # Add tab
        self.notebook.add(editor, text=os.path.basename(file_path), image=icon, compound='left')
        
        # Create highlighter
        ext = os.path.splitext(file_path)[1].lower()
        highlighter = self.highlighter_factory.create_highlighter(ext, editor)
        
        # Save tab infomation
        tab_id = len(self.tabs)
        self.tabs[tab_id] = {
            "widget": editor,
            "file": file_path,
            "modified": False,
            "highlighter": highlighter
        }
        
        # Bind event
        editor.bind("<<Modified>>", lambda e: self._on_text_modified(tab_id))
        
        # Switch new tab
        self.notebook.select(len(self.tabs) - 1)
        
        return tab_id
        
    def close_tab(self, tab_id):
        """Close tab"""
        if tab_id in self.tabs:
            self.notebook.forget(tab_id)
            del self.tabs[tab_id]
            
    def get_current_tab(self):
        """Get current tab"""
        current = self.notebook.select()
        if current:
            tab_id = self.notebook.index(current)
            return self.tabs.get(tab_id)
        return None
        
    def _on_tab_changed(self, event):
        """Tab changed event"""
        current_tab = self.get_current_tab()
        if current_tab and current_tab["highlighter"]:
            current_tab["highlighter"].highlight()
            
    def _on_text_modified(self, tab_id):
        """Text modified event"""
        if tab_id in self.tabs:
            tab = self.tabs[tab_id]
            if not tab["modified"]:
                tab["modified"] = True
                # Add '*' to mark the file
                self.notebook.tab(tab_id, text=os.path.basename(tab["file"]) + "*") 