import ast
from typing import Any, Dict, List, Tuple, Optional
import tokenize
import io
import keyword
import builtins
import re
import json
from tkinter import Toplevel, Listbox, BOTH, END
from pathlib import Path

class BaseHighlighter:
    def __init__(self, text_widget, syntax_colors= {
            "keyword": "#569CD6",
            "control": "#C586C0",
            "operator": "#D4D4D4",
            "punctuation": "#D4D4D4",
            "class": "#4EC9B0",
            "function": "#DCDCAA",
            "method": "#DCDCAA",
            "variable": "#9CDCFE",
            "parameter": "#9CDCFE",
            "property": "#9CDCFE",
            "string": "#CE9178",
            "number": "#B5CEA8",
            "boolean": "#569CD6",
            "null": "#569CD6",
            "constant": "#4FC1FF",
            "comment": "#6A9955",
            "docstring": "#6A9955",
            "todo": "#FF8C00",
            "decorator": "#C586C0",
            "builtin": "#4EC9B0",
            "self": "#569CD6",
            "namespace": "#4EC9B0",
            "type": "#4EC9B0",
            "type_annotation": "#4EC9B0",
            "interface": "#4EC9B0"
        }, theme_name="vscode-dark"):
        self.text_widget = text_widget
        # 初始化默认的语法高亮颜色
        self.syntax_colors = syntax_colors
        self.theme_name = theme_name
        
        self.setup_tags()
        self._setup_bindings()
        
        # 修改防抖动设置
        self._highlight_pending = False
        self._last_change_time = 0
        self._highlight_delay = 50  # 降低延迟时间
        self._last_content = ""     # 添加内容缓存
        
        # 添加自动补全配置
        self.auto_pairs = {
            '"': '"',
            "'": "'",
            '(': ')',
            '[': ']',
            '{': '}',
            '"""': '"""',
            "'''": "'''"
        }
        
        # 添加基础关键字列表
        self.keywords = set(keyword.kwlist)
        self.builtins = set(dir(builtins))
        
        # 添加语言特定的关键字
        self.language_keywords = {
            'control': {'if', 'else', 'elif', 'while', 'for', 'try', 'except', 'finally', 'with', 'break', 'continue', 'return'},
            'definition': {'def', 'class', 'lambda', 'async', 'await'},
            'module': {'import', 'from', 'as'},
            'value': {'True', 'False', 'None'},
            'context': {'global', 'nonlocal', 'pass', 'yield'}
        }
        
    def setup_tags(self):
        """Configure all syntax highlighting tags"""
        for tag, color in self.syntax_colors.items():
            self.text_widget.tag_configure(tag, foreground=color)
            
    def _setup_bindings(self):
        """Set up event bindings"""
        self.text_widget.bind('<<Modified>>', self._on_text_change)
        self.text_widget.bind('<KeyRelease>', self._on_key_release)
        self.text_widget.bind('(', self._handle_open_parenthesis)  # 绑定左括号
        self.text_widget.bind('<Return>', self._handle_return_key)  # 绑定回车键
        self.text_widget.bind('<Tab>', self._handle_tab_key)  # 绑定Tab键
        
    def _on_text_change(self, event=None):
        """Handle text modification events"""
        if self.text_widget.edit_modified():
            self.text_widget.edit_modified(False)
            self._queue_highlight()
            
    def _on_key_release(self, event=None):
        """Handle key release events"""
        if event.keysym in ('Return', 'BackSpace', 'Delete'):
            self._queue_highlight()
            
    def _queue_highlight(self):
        """Queue highlight task"""
        if not self._highlight_pending:
            self._highlight_pending = True
            self.text_widget.after(self._highlight_delay, self._delayed_highlight)
            
    def _delayed_highlight(self):
        """Execute highlighting with delay"""
        try:
            current_content = self.text_widget.get("1.0", "end-1c")
            # 只在内容真正改变时才执行高亮
            if current_content != self._last_content:
                self.highlight()
                self._last_content = current_content
        except Exception as e:
            print(f"高亮处理错误: {str(e)}")
        finally:
            self._highlight_pending = False
            
    def highlight(self):
        """Perform syntax highlighting"""
        try:
            # 保存当前状态
            current_insert = self.text_widget.index("insert")
            current_view = self.text_widget.yview()
            current_selection = None
            try:
                current_selection = (
                    self.text_widget.index("sel.first"),
                    self.text_widget.index("sel.last")
                )
            except:
                pass
                
            # 执行高亮
            self._clear_tags()
            text = self.text_widget.get("1.0", "end-1c")
            
            # 处理注释和字符串
            self._highlight_comments_and_strings(text)
            
            try:
                tree = ast.parse(text)
                self._process_ast(tree)
            except SyntaxError:
                self._basic_highlight(text)
                
            # 恢复状态
            self.text_widget.mark_set("insert", current_insert)
            self.text_widget.yview_moveto(current_view[0])
            if current_selection:
                self.text_widget.tag_add("sel", *current_selection)
                
        except Exception as e:
            print(f"高亮错误: {str(e)}")
            
    def _basic_highlight(self, text: str):
        """Basic highlighting when syntax errors occur"""
        try:
            import re
            
            # 将文本分割成行
            lines = text.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                # 高亮关键字
                for keyword in self.keywords:
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    for match in re.finditer(pattern, line):
                        start = f"{line_num}.{match.start()}"
                        end = f"{line_num}.{match.end()}"
                        self._add_tag("keyword", start, end)
                        
                # 高亮字符串
                string_pattern = r'("(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')'
                for match in re.finditer(string_pattern, line):
                    start = f"{line_num}.{match.start()}"
                    end = f"{line_num}.{match.end()}"
                    self._add_tag("string", start, end)
                    
                # 高亮数字
                number_pattern = r'\b\d+(\.\d+)?\b'
                for match in re.finditer(number_pattern, line):
                    start = f"{line_num}.{match.start()}"
                    end = f"{line_num}.{match.end()}"
                    self._add_tag("number", start, end)
                    
                # 高亮注释
                comment_pattern = r'#.*$'
                for match in re.finditer(comment_pattern, line):
                    start = f"{line_num}.{match.start()}"
                    end = f"{line_num}.{match.end()}"
                    self._add_tag("comment", start, end)
                    
        except Exception as e:
            print(f"基本高亮处理错误: {str(e)}")
            
    def _clear_tags(self):
        """Remove all syntax highlighting tags"""
        try:
            for tag in self.syntax_colors.keys():
                self.text_widget.tag_remove(tag, "1.0", "end")
        except Exception as e:
            print(f"清除标签错误: {str(e)}")
            
    def _add_tag(self, tag: str, start: str, end: str):
        """Add syntax highlighting tag"""
        try:
            self.text_widget.tag_add(tag, start, end)
        except Exception as e:
            print(f"添加标签错误 - 标签: {tag}, 开始: {start}, 结束: {end}, 错误: {str(e)}")

    def get_position(self, node: ast.AST) -> Tuple[str, str]:
        """Get start and end positions of AST node"""
        if hasattr(node, 'lineno'):
            start = f"{node.lineno}.{node.col_offset}"
            end = f"{node.end_lineno}.{node.end_col_offset}" if hasattr(node, 'end_lineno') else f"{node.lineno}.{node.col_offset + len(str(node))}"
            return start, end
        return "1.0", "1.0"

    def _highlight_comments_and_strings(self, text: str):
        """Highlight comments and strings"""
        try:
            # 将文本分割成行
            lines = text.split('\n')
            current_pos = 0
            
            for line_num, line in enumerate(lines, 1):
                # 处理多行字符串
                triple_quote_pattern = r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\')'
                for match in re.finditer(triple_quote_pattern, text[current_pos:]):
                    start_pos = current_pos + match.start()
                    end_pos = current_pos + match.end()
                    
                    # 计算起始行和列
                    start_line = text.count('\n', 0, start_pos) + 1
                    start_col = start_pos - text.rfind('\n', 0, start_pos) - 1
                    
                    # 计算结束行和列
                    end_line = text.count('\n', 0, end_pos) + 1
                    end_col = end_pos - text.rfind('\n', 0, end_pos) - 1
                    
                    start = f"{start_line}.{start_col}"
                    end = f"{end_line}.{end_col}"
                    self._add_tag("docstring", start, end)
                
                # 处理单行注释和字符串
                tokens = list(tokenize.generate_tokens(io.StringIO(line).readline))
                for token in tokens:
                    token_type = token.type
                    token_string = token.string
                    start_col = token.start[1]
                    end_col = token.end[1]
                    
                    if token_type == tokenize.COMMENT:
                        self._add_tag("comment", f"{line_num}.{start_col}", f"{line_num}.{end_col}")
                    elif token_type == tokenize.STRING:
                        if not (token_string.startswith('"""') or token_string.startswith("'''")):
                            self._add_tag("string", f"{line_num}.{start_col}", f"{line_num}.{end_col}")
                    elif token_type == tokenize.NUMBER:
                        self._add_tag("number", f"{line_num}.{start_col}", f"{line_num}.{end_col}")
                    elif token_type == tokenize.OP:
                        self._add_tag("operator", f"{line_num}.{start_col}", f"{line_num}.{end_col}")
                        
                current_pos += len(line) + 1  # +1 for the newline character
                
        except tokenize.TokenError:
            # 如果tokenize失败，尝试使用正则表达式
            self._basic_highlight(text)
        except Exception as e:
            print(f"注释和字符串高亮错误: {str(e)}")
            
    def _process_ast(self, tree: ast.AST):
        """Process AST tree"""
        for node in ast.walk(tree):
            self._highlight_node(node)
            
    def _highlight_node(self, node: ast.AST):
        """Highlight specific AST node"""
        if not hasattr(node, 'lineno'):
            return
        
        start, end = self.get_position(node)
        
        # 处理不同类型的节点
        if isinstance(node, ast.ClassDef):
            self._highlight_class_def(node, start, end)
        elif isinstance(node, ast.FunctionDef):
            self._highlight_function_def(node, start, end)
        elif isinstance(node, ast.Name):
            self._highlight_name(node, start, end)
        elif isinstance(node, ast.Call):
            self._highlight_call(node)
        elif isinstance(node, ast.Constant):
            self._highlight_constant(node, start, end)
        elif isinstance(node, ast.arg):
            self._highlight_arg(node, start, end)
        elif isinstance(node, ast.AnnAssign):
            self._highlight_annotation(node)
        elif isinstance(node, ast.Import):
            self._highlight_import(node)
        elif isinstance(node, ast.ImportFrom):
            self._highlight_import_from(node)
        elif isinstance(node, ast.Attribute):
            self._highlight_attribute(node)
        elif isinstance(node, ast.Assign):
            self._highlight_assignment(node)
        elif isinstance(node, ast.BinOp):
            self._highlight_operator(node, start, end)
        elif isinstance(node, ast.Compare):
            self._highlight_operator(node, start, end)
        elif isinstance(node, ast.BoolOp):
            self._highlight_operator(node, start, end)
        elif isinstance(node, ast.UnaryOp):
            self._highlight_operator(node, start, end)

    def _highlight_class_def(self, node: ast.ClassDef, start: str, end: str):
        """Highlight class definition"""
        # 高亮class关键字
        keyword_end = f"{node.lineno}.{node.col_offset + 5}"
        self._add_tag("keyword", start, keyword_end)
        
        # 高亮类名
        name_start = f"{node.lineno}.{node.col_offset + 6}"
        name_end = f"{node.lineno}.{node.col_offset + 6 + len(node.name)}"
        self._add_tag("class", name_start, name_end)
        
        # 高亮基类
        for base in node.bases:
            base_start, base_end = self.get_position(base)
            self._add_tag("class", base_start, base_end)

    def _highlight_function_def(self, node: ast.FunctionDef, start: str, end: str):
        """Highlight function definition"""
        # 高亮def关键字
        keyword_end = f"{node.lineno}.{node.col_offset + 3}"
        self._add_tag("keyword", start, keyword_end)
        
        # 高亮函数名
        name_start = f"{node.lineno}.{node.col_offset + 4}"
        name_end = f"{node.lineno}.{node.col_offset + 4 + len(node.name)}"
        # 检查是否为魔术方法
        if node.name.startswith('__') and node.name.endswith('__'):
            self._add_tag("method", name_start, name_end)
        else:
            self._add_tag("function", name_start, name_end)
        
        # 高亮装饰器
        for decorator in node.decorator_list:
            dec_start, dec_end = self.get_position(decorator)
            self._add_tag("decorator", dec_start, dec_end)
        
        # 高亮参数
        for arg in node.args.args:
            arg_start, arg_end = self.get_position(arg)
            self._add_tag("parameter", arg_start, arg_end)
            # 高亮参数类型注解
            if arg.annotation:
                ann_start, ann_end = self.get_position(arg.annotation)
                self._add_tag("type_annotation", ann_start, ann_end)

    def _highlight_import(self, node: ast.Import):
        """Highlight import statements"""
        for alias in node.names:
            if hasattr(alias, 'lineno'):
                start = f"{alias.lineno}.{alias.col_offset}"
                end = f"{alias.lineno}.{alias.col_offset + len(alias.name)}"
                self._add_tag("namespace", start, end)
                if alias.asname:
                    as_start = f"{alias.lineno}.{alias.col_offset + len(alias.name) + 4}"
                    as_end = f"{alias.lineno}.{alias.col_offset + len(alias.name) + 4 + len(alias.asname)}"
                    self._add_tag("variable", as_start, as_end)

    def _highlight_import_from(self, node: ast.ImportFrom):
        """Highlight from-import statements"""
        if node.module:
            start = f"{node.lineno}.{node.col_offset + 5}"  # 5 是 'from ' 的长度
            end = f"{node.lineno}.{node.col_offset + 5 + len(node.module)}"
            self._add_tag("namespace", start, end)
        
        for alias in node.names:
            if hasattr(alias, 'lineno'):
                start = f"{alias.lineno}.{alias.col_offset}"
                end = f"{alias.lineno}.{alias.col_offset + len(alias.name)}"
                self._add_tag("namespace", start, end)
                if alias.asname:
                    as_start = f"{alias.lineno}.{alias.col_offset + len(alias.name) + 4}"
                    as_end = f"{alias.lineno}.{alias.col_offset + len(alias.name) + 4 + len(alias.asname)}"
                    self._add_tag("variable", as_start, as_end)

    def _highlight_attribute(self, node: ast.Attribute):
        """Highlight attribute access"""
        if isinstance(node.value, ast.Name):
            # 高亮对象名
            start, _ = self.get_position(node.value)
            end = f"{node.value.lineno}.{node.value.col_offset + len(node.value.id)}"
            self._add_tag("variable", start, end)
        
        # 高亮属性名
        attr_start = f"{node.lineno}.{node.col_offset + len(str(node.value)) + 1}"
        attr_end = f"{node.lineno}.{node.col_offset + len(str(node.value)) + 1 + len(node.attr)}"
        self._add_tag("property", attr_start, attr_end)

    def _highlight_name(self, node: ast.Name, start: str, end: str):
        """Highlight name"""
        if node.id in keyword.kwlist:
            self._add_tag("keyword", start, end)
        elif node.id in dir(builtins):
            self._add_tag("builtin", start, end)
        elif node.id.isupper():
            self._add_tag("constant", start, end)
        elif node.id == 'self':
            self._add_tag("self", start, end)
        else:
            self._add_tag("variable", start, end)
            
    def _highlight_call(self, node: ast.Call):
        """Highlight function call"""
        if isinstance(node.func, ast.Name):
            start, end = self.get_position(node.func)
            if node.func.id in dir(builtins):
                self._add_tag("builtin", start, end)
            else:
                self._add_tag("function", start, end)
                
    def _highlight_constant(self, node: ast.Constant, start: str, end: str):
        """Highlight constant"""
        if isinstance(node.value, (int, float)):
            self._add_tag("number", start, end)
        elif isinstance(node.value, str):
            self._add_tag("string", start, end)
            
    def _highlight_arg(self, node: ast.arg, start: str, end: str):
        """Highlight function argument"""
        self._add_tag("parameter", start, end)
        
    def _highlight_annotation(self, node: ast.AnnAssign):
        """Highlight type annotation"""
        if node.annotation:
            start, end = self.get_position(node.annotation)
            self._add_tag("type_annotation", start, end)

    def _highlight_assignment(self, node: ast.Assign):
        """Highlight assignment statement"""
        for target in node.targets:
            start, end = self.get_position(target)
            self._add_tag("variable", start, end)
            
        if isinstance(node.value, ast.Name):
            start, end = self.get_position(node.value)
            self._add_tag("variable", start, end)

    def _handle_open_parenthesis(self, event):
        """Handle parenthesis auto-completion"""
        try:
            current_pos = self.text_widget.index("insert")
            self.text_widget.insert(current_pos, '(')  # 插入左括号
            self.text_widget.insert(f"{current_pos} + 1c", self.auto_pairs['('])  # 插入右括号
            self.text_widget.mark_set("insert", f"{current_pos} + 1c")  # 将光标移到括号之间
            return "break"  # 阻止默认的插入行为
        except Exception as e:
            print(f"左括号补全错误: {str(e)}")
        return None

    def _highlight_operator(self, node: ast.AST, start: str, end: str):
        """Highlight operator"""
        self._add_tag("operator", start, end)

    def _handle_return_key(self, event):
        """Handle return key for auto-indentation"""
        try:
            current_line = self.text_widget.get("insert linestart", "insert")
            indent = len(current_line) - len(current_line.lstrip())
            # 检查当前行是否以冒号结尾，表示需要增加缩进
            if current_line.rstrip().endswith(":"):
                indent += 4  # 增加一个缩进级别
            self.text_widget.insert("insert", "\n" + " " * indent)
            return "break"  # 阻止默认的回车行为
        except Exception as e:
            print(f"自动缩进错误: {str(e)}")
        return None

    def _handle_tab_key(self, event):
        """Handle tab key to insert 4 spaces"""
        self.text_widget.insert("insert", " " * 4)
        return "break"  # 阻止默认的Tab行为

    def set_theme(self, theme_data):
        """Set theme
        
        Args:
            theme_data: Can be theme name string or theme config dict
        """
        try:
            if isinstance(theme_data, str):
                # 如果传入的是主题名称，从主题文件加载
                theme_file = Path("./asset/theme") / f"{theme_data}.json"
                if not theme_file.exists():
                    print(f"警告: 主题文件 {theme_file} 不存在，使用默认主题")
                    return
                    
                with open(theme_file, "r", encoding="utf-8") as f:
                    theme_data = json.load(f)
                
                self.theme_name = theme_data
            
            # 配置文本部件的基础样式
            if "base" in theme_data:
                self.text_widget.configure(**theme_data["base"])
                
            # 更新语法高亮颜色
            for tag, color in theme_data.items():
                if tag != "base" and isinstance(color, str):
                    self.syntax_colors[tag] = color
                    
            # 重新设置所有标签
            self.setup_tags()
            
        except Exception as e:
            print(f"警告: 设置主题失败: {str(e)}")
            # 保持当前主题不变

    def get_theme(self):
        """
        Get theme type
        """
        return self.theme_name