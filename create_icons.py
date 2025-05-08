import requests
import os
from pathlib import Path
# import cairosvg

# 创建图标目录
icons_dir = Path("./asset/icons")
icons_dir.mkdir(parents=True, exist_ok=True)

# Seti Icons 的下载链接 (使用 jsDelivr CDN)
ICON_URLS = {
    "python.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/python.svg",
    "javascript.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/javascript.svg",
    "html.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/html.svg",
    "css.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/css.svg",
    "json.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/json.svg",
    "ruby.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/ruby.svg",
    "c.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/c.svg",
    "cpp.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/cpp.svg",
    "h.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/h.svg",
    "objc.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/objc.svg",
    "java.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/java.svg",
    "rust.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/rust.svg",
    "bash.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/shell.svg",
    "text.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/text.svg",
    "file.png": "https://cdn.jsdelivr.net/gh/jesseweed/seti-ui/icons/default.svg"
}

# def svg_to_png(svg_data, size=(64, 64)):
#     """将SVG数据转换为PNG格式，并调整大小"""
#     try:
#         # 先将SVG转换为PNG
#         png_data = cairosvg.svg2png(
#             bytestring=svg_data,
#             output_width=size[0],
#             output_height=size[1]
#         )
#         return png_data
#     except Exception as e:
#         print(f"SVG转换错误: {str(e)}")
#         return None

def download_and_convert_icon(url, filename, size=(64, 64)):
    """下载SVG图标并转换为PNG"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 转换SVG为PNG
            png_data = response.content
            # if png_data:
            with open(icons_dir / filename, 'wb') as f:
                f.write(png_data)
                # print(f"成功下载并转换: {filename}")
            # else:
            #     print(f"转换失败: {filename}")
        else:
            print(f"下载失败 {filename}: HTTP {response.status_code}")
    except Exception as e:
        print(f"处理 {filename} 时出错: {str(e)}")

# 下载并转换所有图标
for filename, url in ICON_URLS.items():
    download_and_convert_icon(url, filename, (64, 64))

print("图标下载和转换完成！") 