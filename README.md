# Phoenix Editor

Phoenix Editor 是一个轻量级的代码编辑器，旨在提供简洁高效的编程体验。它支持多种编程语言的语法高亮，并具备基本的代码编辑功能。

## 特性

- 支持多语言语法高亮（Python、C/C++、Java、JavaScript、HTML、CSS 等）
- 多标签页管理
- 自动保存功能
- 基本的代码高亮与语法分析
- 可扩展的主题和语言包
- 支持文件图标显示

## 安装

1. 确保你已经安装了 Python 3.x。
2. 克隆本仓库到本地：
   
   ```bash
   git clone https://gitee.com/your-repo/phoenix-editor.git
   ```
3. 进入项目目录并运行主程序：
   
   ```bash
   cd phoenix-editor
   python main.py
   ```

## 使用方法

- **新建文件/窗口**：点击菜单栏 `File > New File / New Window`
- **打开文件**：点击菜单栏 `File > Open`
- **保存文件**：点击菜单栏 `File > Save`
- **运行代码**：点击菜单栏 `Run > Run`
- **设置**：点击菜单栏 `Settings > Open Settings Panel` 可调整字体、编码、语言等

## 配置

所有配置信息存储在 `asset/settings.json` 文件中，你可以手动修改该文件来调整以下设置：

- 字体与字号
- 默认编码格式
- 默认语言
- 主题样式（支持深色/浅色模式）
- 自动保存间隔

## 主要模块

- `library/highlighter/`: 各种语言的语法高亮实现
- `library/tab_manager.py`: 标签页管理逻辑
- `library/api.py`: 编辑器核心配置与初始化接口
- `main.py`: 主程序入口及基础功能实现
- `asset/settings.json`: 存储用户配置
- `asset/theme/`: 主题样式文件
- `asset/packages/lang/`: 多语言支持文件

## 贡献

欢迎贡献代码或提出建议！请遵循以下步骤：

1. Fork 本仓库
2. 创建新分支 (`git checkout -b feature/new-feature`)
3. 提交更改 (`git commit -m 'Add new feature'`)
4. 推送分支 (`git push origin feature/new-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT License，请参阅 [LICENSE](LICENSE) 文件了解详细信息。

## 版本历史

- **v0.3.0**：新增多语言支持与主题切换功能
- **v0.2.0**：实现多标签页与自动保存功能
- **v0.1.1**：优化语法高亮逻辑
- **v0.1.0**：初始版本，实现基础编辑与运行功能

## 下载

你可以从 [Releases](README.md#下载) 页面下载最新版本的 Phoenix Editor。

## 相关链接

- [Gitee 项目主页](https://gitee.com/creative-and-dream/phoenix-editor)
- [Issue 跟踪](https://gitee.com/creative-and-dream/phoenix-editor/issues)
- [Pull Request 提交指南](.gitee/PULL_REQUEST_TEMPLATE.zh-CN.md)


