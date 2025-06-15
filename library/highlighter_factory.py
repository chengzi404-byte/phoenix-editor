from . import api
import importlib

class HighlighterFactory:
    """Code highlighter factory class"""
    
    def __init__(self):
        # File extenision map
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
        # Get highlighter type
        highlighter_type = api.Settings.Highlighter.syntax_highlighting()["code"]
        
        # Import module
        module_name = f"library.highlighter.{highlighter_type}"
        module = importlib.import_module(module_name)

        print(f"Current module: {module_name}")
        
        # Create highlighter
        highlighter_class = getattr(module, 'CodeHighlighter')
        return highlighter_class(text_widget)
