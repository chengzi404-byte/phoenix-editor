from . import highlighter
import importlib
import pathlib
import json

class HighlighterFactory:
    """Code highlighter factory class"""
    
    def __init__(self):
        # 文件扩展名到高亮器的映射
        self.highlighter_map = {
            ".py": "python",
            ".js": "javascript",
            ".html": "html",
            ".css": "css",
            ".json": "json",
            ".rb": "ruby",
            ".c": "c",
            ".cpp": "cpp",
            ".h": "cpp",
            ".m": "objc",
            ".java": "java",
            ".rs": "rust",
            ".sh": "bash",
            ".txt": "text"
        }
        
    def create_highlighter(self, file_extension, text_widget):
        """Create appropriate highlighter based on file extension"""
        # 获取高亮器类型
        highlighter_type = self.highlighter_map.get(file_extension.lower(), "python")
        
        # 动态导入高亮器模块
        module_name = f"library.highlighter.{highlighter_type}"
        module = importlib.import_module(module_name)

        print(module_name)
        
        # 创建高亮器实例
        highlighter_class = getattr(module, 'CodeHighlighter')
        return highlighter_class(text_widget)

"""
from . import highlighter

class HighlighterFactory:
        
    def create_highlighter(self, file_extension, text_widget):

        if file_extension in [".py", ".pyi", ".pyw"]:
            return highlighter.python.CodeHighlighter
        elif file_extension in [".js"]:
            return highlighter.javascript.CodeHighlighter
        elif file_extension in [".cpp", ".hxx", ".cxx", ".c++"]:
            return highlighter.cpp.CodeHighlighter
        elif file_extension in [".rb"]:
            return highlighter.ruby.CodeHighlighter
        elif file_extension in [".c", ".h"]:
            return highlighter.c.CodeHighlighter
        elif file_extension in [".m"]:
            return highlighter.objc.CodeHighlighter
        elif file_extension in [".sh", ".bat", ".ps1"]:
            return highlighter.bash.CodeHighlighter
        elif file_extension in [".rs"]:
            return highlighter.rust.CodeHighlighter
        elif file_extension in [".java"]:
            return highlighter.java.CodeHighlighter
        elif file_extension in [".html", ".htm"]:
            return highlighter.html.CodeHighlighter
        else:
            return highlighter.json.CodeHighlighter
"""