from pathlib import Path
import tkinter as tk
from PIL import Image, ImageTk

class FileIcons:
    def __init__(self):
        self.icons = {}
        self.load_icons()
        
    def load_icons(self):
        """Load all file type icons"""
        icon_dir = Path("./asset/icons")
        
        # 文件类型到图标的映射
        self.file_types = {
            ".py": "python.png",
            ".js": "javascript.png",
            ".html": "html.png",
            ".css": "css.png",
            ".json": "json.png",
            ".rb": "ruby.png",
            ".c": "c.png",
            ".cpp": "cpp.png",
            ".h": "h.png",
            ".m": "objc.png",
            ".java": "java.png",
            ".rs": "rust.png",
            ".sh": "bash.png",
            ".txt": "text.png",
            "default": "file.png"
        }
        
        # 加载所有图标
        for icon_file in self.file_types.values():
            try:
                icon_path = icon_dir / icon_file
                if not icon_path.exists():
                    print(f"警告: 图标文件不存在 {icon_file}")
                    continue
                    
                # 打开并调整图标大小
                img = Image.open(icon_path)
                # 保持宽高比
                if img.size[0] != img.size[1]:
                    size = min(img.size)
                    img = img.crop((0, 0, size, size))
                img = img.resize((16, 16), Image.Resampling.LANCZOS)
                
                # 创建Tkinter图像
                self.icons[icon_file] = ImageTk.PhotoImage(img)
                
            except Exception as e:
                print(f"无法加载图标 {icon_file}: {str(e)}")
                # 如果加载失败，尝试使用默认图标
                if icon_file != "file.png":  # 防止递归
                    self.icons[icon_file] = self.get_default_icon()
                
    def get_icon(self, file_path):
        """Get icon based on file extension"""
        try:
            ext = Path(file_path).suffix.lower()
            icon_file = self.file_types.get(ext, self.file_types["default"])
            return self.icons.get(icon_file, self.get_default_icon())
        except Exception as e:
            print(f"获取图标错误 {file_path}: {str(e)}")
            return self.get_default_icon()
            
    def get_default_icon(self):
        """Get default icon"""
        return self.icons.get("file.png") 
