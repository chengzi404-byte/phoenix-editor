from .base import BaseHighlighter
import ast

class CodeHighlighter(BaseHighlighter):
    def __init__(self, text_widget):
        super().__init__(text_widget)
        # Rust特定的关键字
        self.keywords = {
            "as", "async", "await", "break", "const", "continue", "crate", 
            "dyn", "else", "enum", "extern", "false", "fn", "for", "if", 
            "impl", "in", "let", "loop", "match", "mod", "move", "mut", 
            "pub", "ref", "return", "self", "Self", "static", "struct", 
            "super", "trait", "true", "type", "unsafe", "use", "where", "while"
        }
        
        # Rust特定的语法高亮规则
        self.syntax_colors.update({
            "macro": self.syntax_colors["function"],      # 宏
            "lifetime": self.syntax_colors["decorator"],  # 生命周期标注
            "attribute": self.syntax_colors["decorator"], # 属性
            "trait": self.syntax_colors["interface"],    # trait
            "enum": self.syntax_colors["type"],          # 枚举
            "struct": self.syntax_colors["type"],        # 结构体
        })
        self.setup_tags()
        
    def _highlight_node(self, node: ast.AST):
        """Extend base highlighter's node processing"""
        super()._highlight_node(node)
        
        if not hasattr(node, 'lineno'):
            return
            
        start, end = self.get_position(node)
        
        # Rust特定的节点处理
        if isinstance(node, ast.Name):
            self._highlight_rust_name(node, start, end)
        elif isinstance(node, ast.Call):
            self._highlight_rust_macro(node, start, end)
            
    def _highlight_rust_name(self, node: ast.Name, start: str, end: str):
        """Highlight Rust-specific names"""
        name = node.id
        if name in self.keywords:
            self._add_tag("keyword", start, end)
        elif name.startswith("'"):  # 生命周期标注
            self._add_tag("lifetime", start, end)
        elif name.isupper():  # 常量
            self._add_tag("constant", start, end)
            
    def _highlight_rust_macro(self, node: ast.Call, start: str, end: str):
        """Highlight Rust macro calls"""
        if isinstance(node.func, ast.Name) and node.func.id.endswith("!"):
            self._add_tag("macro", start, end)
