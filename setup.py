# set up file
# setting up the editor
# version: 0.1

from shutil import copyfile
from os import listdir, path, environ, name
import ctypes

# 检查是否在Windows环境下运行
if not name == 'nt':
    raise EnvironmentError("This setup script is intended to run on Windows only.")

# 获取Windows字体目录
fonts_dir = path.join(environ['WINDIR'], 'Fonts')

# 复制字体文件
for dir in listdir("./asset/font/"):
    src = path.join("./asset/font/", dir)
    dst = path.join(fonts_dir, dir)
    print(f"[INFO] Copying font {dir}")
    copyfile(src, dst)

# 刷新字体缓存
ctypes.windll.gdi32.AddFontResourceW.restype = ctypes.c_int
for dir in listdir("./asset/font/"):
    font_path = path.join(fonts_dir, dir)
    ctypes.windll.gdi32.AddFontResourceW(font_path)

print("Setup Successfully")