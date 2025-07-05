from subprocess import run
from tkinter import messagebox
from pathlib import Path
import shutil


messagebox.showinfo("", "要求使用管理员权限运行")

build_spec = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[
                 ('asset', 'asset'),
                 ('library', 'library'),
                 ('logs', 'logs'),
                 ('LICENSE', '.'),
                 ('README.en.md', '.'),
                 ('README.md', '.'),
                 ('temp_script.txt', '.'),
             ],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
"""


print("[INFO] Generating build.spec")
with open("./cache/build_file.spec", "w", encoding="utf-8") as fp:
    fp.write(build_spec)

print("[INFO] Copying required files")
shutil.copytree("asset", f"{Path.cwd() / "asset"}")
shutil.copytree("library", f"{Path.cwd() / "library"}")

try:
    print("[JUMP] Compling main.py...")
    run("pyinstaller cache/build_file.spec")
except Exception as e:
    print(f"ERROR: {e}")
    run("pip install pyinstaller")
    try:
        run("pyinstaller cache/build_file.spec")
    except:
        messagebox.showerror("ERR", "PLEASE RESTART THE SOFTWARE")

