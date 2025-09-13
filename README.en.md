# Phoenix Editor

Phoenix Editor is a lightweight code editor designed to provide a clean and efficient programming experience. It supports syntax highlighting for multiple programming languages and includes essential code editing features.

## Features

- Syntax highlighting for multiple languages (Python, C/C++, Java, JavaScript, HTML, CSS, etc.)
- Multi-tab management
- Auto-save functionality
- Basic code highlighting and syntax analysis
- Extensible themes and language packages
- Support for file icon display

## Installation

1. Ensure you have Python 3.x installed.
2. Clone this repository to your local machine:

   ```bash
   git clone https://gitee.com/your-repo/phoenix-editor.git
   ```
3. Navigate to the project directory and run the main program:

   ```bash
   cd phoenix-editor
   python main.py
   ```

## Usage

- **New File/Window**: Click `File > New File / New Window` in the menu bar.
- **Open File**: Click `File > Open` in the menu bar.
- **Save File**: Click `File > Save` in the menu bar.
- **Run Code**: Click `Run > Run` in the menu bar.
- **Settings**: Click `Settings > Open Settings Panel` to adjust font, encoding, language, etc.

## Configuration

All configuration information is stored in the `asset/settings.json` file. You can manually modify this file to adjust the following settings:

- Font and font size
- Default encoding format
- Default language
- Theme style (supports dark/light mode)
- Auto-save interval

## Main Modules

- `library/highlighter/`: Syntax highlighting implementations for various languages
- `library/tab_manager.py`: Tab management logic
- `library/api.py`: Core editor configuration and initialization interface
- `main.py`: Main program entry and basic functionality implementation
- `asset/settings.json`: Stores user configurations
- `asset/theme/`: Theme style files
- `asset/packages/lang/`: Multi-language support files
- `asset/packages/runner`: Code execution module

## Q&A Section

**Q1: What is this project built with?**

> It is built using Python and integrates the **Deepseek-r1** large model to quickly respond to all requests.
> 
> It also uses the AST (Abstract Syntax Tree) for syntax highlighting, enabling code highlighting for programming languages and supporting various data types across all languages.

**Q2: What are the features of this project?**

> ### ✨ Advantages
> 
> * Lightweight — Occupies only about 10MB of disk space and requires only 50MB of memory to run.
>   
> * Cross-platform — Supports Windows, Linux/Unix, and other operating systems, adapting to various environments.
>   
> * Open-source and free — All source code is available on [Gitee](https://gitee.com/creative-and-dream/phoenix-editor/) under the MIT License, allowing anyone to modify and redistribute the project with high customizability.
>   
> 
> ### ⭕ Limitations
> 
> * No cloud saving functionality.
>   
> * No mobile version available.
>   

**Q3: Who is the target audience for this project?**

> The education sector. Compared to most IDEs in the education industry, this IDE offers more advantages. Please refer to *Q2*.

**Q4: What are the strengths and weaknesses of this project compared to other IDEs in the education sector?**

> | Feature | Turtle Editor | This IDE |
> | --- | --- | --- |
> | Auto-save | √ | √ |
> | Basic code highlighting (keywords, numbers) | √ | √ |
> | Advanced code highlighting (variables, function names, package names) | X | √ |
> | AI functionality | X | √ |
> | Multi-language syntax highlighting | X | √ |
> | Code execution | O | √ |
> | Cloud saving | √ | X |
> 
> *Turtle Editor is used as an example here.*

## Contribution

Contributions and suggestions are welcome! Please follow these steps:

1. Fork this repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push the branch (`git push origin feature/new-feature`).
5. Create a Pull Request.

## License

This project is licensed under the MIT License. For more details, please refer to the [LICENSE](LICENSE) file.

## Version History

- **v1.0.0**: Official release
- **v0.4.0**: Added AI dialogue functionality
- **v0.3.0**: Added multi-language support and theme switching
- **v0.2.0**: Implemented multi-tab and auto-save features
- **v0.1.1**: Optimized syntax highlighting logic
- **v0.1.0**: Initial version with basic editing and execution functionality

## Download

You can download the latest version of Phoenix Editor from the [Releases](README.md#download) page.

## Related Links

- [Gitee Project Homepage](https://gitee.com/creative-and-dream/phoenix-editor)
- [Issue Tracking](https://gitee.com/creative-and-dream/phoenix-editor/issues)
- [Pull Request Submission Guidelines](.gitee/PULL_REQUEST_TEMPLATE.zh-CN.md) 