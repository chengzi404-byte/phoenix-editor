from .validator import validate_settings
import json
import os
class EditorAPI:
    """编辑器公共API"""
    def __init__(self):
        self.file_path = "./temp_script.py"
        self.copy_msg = ""
        self.settings = {}
        self.lang_dict = {}
        self.codehighlighter = None
        self.file_encoding = "utf-8"
        
    def load_settings(self):
        """加载设置"""
        try:
            with open("./asset/settings.json", "r", encoding="utf-8") as fp:
                self.settings = json.load(fp)
            if not validate_settings(self.settings):
                raise ValueError("无效的设置文件")
            self.file_encoding = self.settings.get("file-encoding", "utf-8")
            return True
        except Exception as e:
            print(f"加载设置失败: {str(e)}")
            return False
            
    def save_settings(self):
        """保存设置"""
        try:
            with open("./asset/settings.json", "w", encoding="utf-8") as fp:
                json.dump(self.settings, fp, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存设置失败: {str(e)}")
            return False
            
    def load_language(self, lang):
        """加载语言包"""
        try:
            lang_file = f"./asset/lang_{lang}.json"
            if os.path.exists(lang_file):
                with open(lang_file, "r", encoding="utf-8") as f:
                    self.lang_dict = json.load(f)
            return True
        except Exception as e:
            print(f"加载语言包失败: {str(e)}")
            return False 