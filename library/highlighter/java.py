from .base import BaseHighlighter
import ast

class CodeHighlighter(BaseHighlighter):
    def __init__(self, text_widget):
        super().__init__(text_widget)
        # Java特定的关键字
        self.keywords = {
            'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch',
            'char', 'class', 'const', 'continue', 'default', 'do', 'double',
            'else', 'enum', 'extends', 'final', 'finally', 'float', 'for',
            'if', 'implements', 'import', 'instanceof', 'int', 'interface',
            'long', 'native', 'new', 'package', 'private', 'protected',
            'public', 'return', 'short', 'static', 'strictfp', 'super',
            'switch', 'synchronized', 'this', 'throw', 'throws', 'transient',
            'try', 'void', 'volatile', 'while'
        }
        
        # Java特定的语法高亮规则
        self.syntax_colors.update({
            "annotation": self.syntax_colors["decorator"],  # 注解
            "generic": self.syntax_colors["type"],         # 泛型
            "interface": self.syntax_colors["interface"],  # 接口
            "enum": self.syntax_colors["type"],           # 枚举
            "package": self.syntax_colors["namespace"],    # 包名
        })
        self.setup_tags()
        
    def _highlight_node(self, node: ast.AST):
        """Extend base highlighter's node processing"""
        super()._highlight_node(node)
        
        if not hasattr(node, 'lineno'):
            return
            
        start, end = self.get_position(node)
        
        # Java特定的节点处理
        if isinstance(node, ast.Name):
            self._highlight_java_name(node, start, end)
        elif isinstance(node, ast.ClassDef):
            self._highlight_java_class(node, start, end)
            
    def _highlight_java_name(self, node: ast.Name, start: str, end: str):
        """Highlight Java-specific names"""
        name = node.id
        if name in self.keywords:
            self._add_tag("keyword", start, end)
        elif name.startswith("@"):  # 注解
            self._add_tag("annotation", start, end)
            
    def _highlight_java_class(self, node: ast.ClassDef, start: str, end: str):
        """Highlight Java class definitions"""
        # 处理泛型
        for base in node.bases:
            if isinstance(base, ast.Subscript):
                base_start, base_end = self.get_position(base)
                self._add_tag("generic", base_start, base_end)
