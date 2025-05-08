from .base import BaseHighlighter
import ast
import builtins
import keyword

class CodeHighlighter(BaseHighlighter):
    def __init__(self, text_widget):
        super().__init__(text_widget)
        # Python特定的内置函数和关键字
        self.builtins = set(dir(builtins))
        self.keywords = set(keyword.kwlist)
        
        # Python特定的语法高亮规则
        self.syntax_colors.update({
            "f_string": self.syntax_colors["string"],     # f-string使用字符串颜色
            "bytes": self.syntax_colors["string"],        # 字节字符串
            "exception": self.syntax_colors["class"],     # 异常类使用类的颜色
            "magic_method": self.syntax_colors["function"], # 魔术方法
        })
        self.setup_tags()
        
    def _highlight_node(self, node: ast.AST):
        """扩展基础高亮器的节点处理"""
        super()._highlight_node(node)
        
        if not hasattr(node, 'lineno'):
            return
            
        start, end = self.get_position(node)
        
        # Python特定的节点处理
        if isinstance(node, ast.JoinedStr):  # f-string
            self._highlight_f_string(node, start, end)
        elif isinstance(node, ast.Bytes):     # 字节字符串
            self._add_tag("bytes", start, end)
        elif isinstance(node, ast.Try):       # try-except 块
            self._highlight_try_except(node)
        elif isinstance(node, ast.AsyncFunctionDef):  # 异步函数
            self._highlight_async_function(node)
            
    def _highlight_f_string(self, node: ast.JoinedStr, start: str, end: str):
        """高亮f-string"""
        self._add_tag("f_string", start, end)
        # 处理f-string中的表达式
        for value in node.values:
            if isinstance(value, ast.FormattedValue):
                expr_start, expr_end = self.get_position(value)
                self._add_tag("variable", expr_start, expr_end)
                
    def _highlight_try_except(self, node: ast.Try):
        """高亮try-except块"""
        # 高亮异常类
        for handler in node.handlers:
            if handler.type:
                start, end = self.get_position(handler.type)
                self._add_tag("exception", start, end)
                
    def _highlight_async_function(self, node: ast.AsyncFunctionDef):
        """高亮异步函数"""
        start, end = self.get_position(node)
        # 高亮async关键字
        async_end = f"{node.lineno}.{node.col_offset + 5}"
        self._add_tag("keyword", start, async_end)
        
        # 高亮函数名
        name_start = f"{node.lineno}.{node.col_offset + 9}"  # async def 后的位置
        name_end = f"{node.lineno}.{node.col_offset + 9 + len(node.name)}"
        self._add_tag("function", name_start, name_end)
