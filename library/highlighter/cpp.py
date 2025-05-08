from .base import BaseHighlighter
import ast
import keyword

class CodeHighlighter(BaseHighlighter):
    def __init__(self, text_widget):
        super().__init__(text_widget)
        # C++特定的关键字
        self.keywords = {
            'if', 'else', 'while', 'signed', 'throw', 'union', 'this', 'int',
            'char', 'double', 'unsigned', 'const', 'goto', 'virtual', 'for',
            'float', 'break', 'auto', 'class', 'operator', 'case', 'do',
            'long', 'typedef', 'static', 'friend', 'template', 'default',
            'new', 'void', 'register', 'extern', 'return', 'enum', 'inline',
            'try', 'short', 'continue', 'sizeof', 'switch', 'private',
            'protected', 'public', 'volatile', 'struct', 'using', 'namespace'
        }
        
        # C++特定的语法高亮规则
        self.syntax_colors.update({
            "preprocessor": self.syntax_colors["control"],  # 预处理指令使用控制流颜色
            "namespace": self.syntax_colors["namespace"],   # 命名空间
            "template": self.syntax_colors["type"],         # 模板
            "operator": self.syntax_colors["operator"],     # 运算符重载
            "pointer": self.syntax_colors["variable"],      # 指针
        })
        self.setup_tags()
        
    def _highlight_node(self, node: ast.AST):
        """扩展基础高亮器的节点处理"""
        super()._highlight_node(node)
        
        if not hasattr(node, 'lineno'):
            return
            
        start, end = self.get_position(node)
        
        # C++特定的节点处理
        if isinstance(node, ast.Name):
            self._highlight_cpp_name(node, start, end)
        elif isinstance(node, ast.ClassDef):
            self._highlight_cpp_class(node, start, end)
            
    def _highlight_cpp_name(self, node: ast.Name, start: str, end: str):
        """高亮C++特定的名称"""
        name = node.id
        if name in self.keywords:
            self._add_tag("keyword", start, end)
        elif name.startswith("#"):  # 预处理指令
            self._add_tag("preprocessor", start, end)
        elif "::" in name:  # 命名空间
            self._add_tag("namespace", start, end)
            
    def _highlight_cpp_class(self, node: ast.ClassDef, start: str, end: str):
        """高亮C++类定义"""
        # 处理模板
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and decorator.func.id == "template":
                dec_start, dec_end = self.get_position(decorator)
                self._add_tag("template", dec_start, dec_end)
