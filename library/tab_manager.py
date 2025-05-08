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
        
        # 创建标签页控件
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # 保存所有打开的标签页
        self.tabs = {}  # {tab_id: {"widget": widget, "file": file_path, "modified": bool}}
        
        # 绑定事件
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        
    def add_tab(self, file_path=None, content=""):
        """添加新标签页"""
        # 创建编辑器组件
        editor = ScrolledText(self.notebook, font=Font(family="Consolas", size=12))
        editor.insert("1.0", content)
        
        # 如果没有指定文件路径，创建一个新文件
        if not file_path:
            file_path = f"未命名-{len(self.tabs) + 1}.txt"
            
        # 获取文件图标
        icon = self.file_icons.get_icon(file_path)
        
        # 添加标签页
        self.notebook.add(editor, text=os.path.basename(file_path), image=icon, compound='left')
        
        # 创建语法高亮器
        ext = os.path.splitext(file_path)[1].lower()
        highlighter = self.highlighter_factory.create_highlighter(ext, editor)
        
        # 保存标签页信息
        tab_id = len(self.tabs)
        self.tabs[tab_id] = {
            "widget": editor,
            "file": file_path,
            "modified": False,
            "highlighter": highlighter
        }
        
        # 绑定修改事件
        editor.bind("<<Modified>>", lambda e: self._on_text_modified(tab_id))
        
        # 切换到新标签页
        self.notebook.select(len(self.tabs) - 1)
        
        return tab_id
        
    def close_tab(self, tab_id):
        """关闭标签页"""
        if tab_id in self.tabs:
            self.notebook.forget(tab_id)
            del self.tabs[tab_id]
            
    def get_current_tab(self):
        """获取当前标签页"""
        current = self.notebook.select()
        if current:
            tab_id = self.notebook.index(current)
            return self.tabs.get(tab_id)
        return None
        
    def _on_tab_changed(self, event):
        """标签页切换事件处理"""
        current_tab = self.get_current_tab()
        if current_tab and current_tab["highlighter"]:
            current_tab["highlighter"].highlight()
            
    def _on_text_modified(self, tab_id):
        """文本修改事件处理"""
        if tab_id in self.tabs:
            tab = self.tabs[tab_id]
            if not tab["modified"]:
                tab["modified"] = True
                # 在文件名后添加星号表示未保存
                self.notebook.tab(tab_id, text=os.path.basename(tab["file"]) + "*") 