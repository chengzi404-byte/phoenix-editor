from . import api
import importlib

class HighlighterFactory:
    """Code highlighter factory class"""
    def __init__(self, logger):
        self.logger = logger

    def create_highlighter(self, text_widget, type=None):
        """Create appropriate highlighter based on file extension"""
        # Get highlighter type
        if type == None: type = api.Settings.Highlighter.syntax_highlighting()["code"]

        # Log info
        self.logger.info(f"Setup highlighter {type}")
        
        # Import module
        module_name = f"library.highlighter.{type}"
        module = importlib.import_module(module_name)
        
        # Create highlighter
        highlighter_class = getattr(module, 'CodeHighlighter')
        return highlighter_class(text_widget)
