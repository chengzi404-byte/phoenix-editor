from .base import BaseHighlighter
import ast

class CodeHighlighter(BaseHighlighter):
    def __init__(self, text_widget):
        super().__init__(text_widget)
        # JavaScript特定的语法高亮规则
        self.keywords = {
            # 控制流
            'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break',
            'continue', 'return', 'try', 'catch', 'finally', 'throw',
            # 声明
            'var', 'let', 'const', 'function', 'class', 'extends',
            'constructor', 'super', 'new', 'this',
            # 模块
            'import', 'export', 'default', 'from', 'as',
            # 其他
            'typeof', 'instanceof', 'in', 'of', 'void', 'delete',
            'async', 'await', 'yield'
        }
        
        self.syntax_colors.update({
            "regex": "#D16969",
            "template": "#CE9178",
            "arrow": "#569CD6",
            "object": "#4EC9B0",
            "array": "#4EC9B0"
        })
        
        self.setup_tags() 