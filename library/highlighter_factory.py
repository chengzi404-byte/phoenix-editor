from . import highlighter
import importlib

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
        try:
            # 获取高亮器类型
            highlighter_type = self.highlighter_map.get(file_extension.lower(), "python")
            
            # 动态导入高亮器模块
            module_name = f"library.highlighter.{highlighter_type}"
            module = importlib.import_module(module_name)
            
            # 创建高亮器实例
            highlighter_class = getattr(module, 'CodeHighlighter')
            return highlighter_class(text_widget)
            
        except Exception as e:
            print(f"创建高亮器失败: {str(e)}，使用Python高亮器作为默认")
            return highlighter.python.CodeHighlighter(text_widget) 
