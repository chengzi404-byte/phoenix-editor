Phoenix Editor
==============

Phoenix Editor is a lightweight code editor designed to provide a simple and efficient programming experience. It supports syntax highlighting for multiple programming languages and offers basic code editing functions.

## Features



* Supports syntax highlighting for multiple languages (Python, C/C++, Java, JavaScript, HTML, CSS, etc.)
* Multi-tab management
* Auto-save function
* Basic code highlighting and syntax analysis
* Extensible themes and language packs
* Supports file icon display

Installation
------------

1. Ensure you have Python 3.x installed.

2. Clone this repository to your local machine:
   
   ```bash
   git clone https://gitee.com/creative-and-dream/phoenix-editor.git
   ```

3. Navigate to the project directory and run the main program:

```bash
cd phoenix-editor
python main.py
```




## Usage

* **New File/Window**: Click `File > New File / New Window` in the menu bar.
* **Open File**: Click `File > Open` in the menu bar.
* **Save File**: Click `File > Save` in the menu bar.
* **Run Code**: Click `Run > Run` in the menu bar.
* **Settings**: Click `Settings > Open Settings Panel` in the menu bar to adjust fonts, encoding, language, etc.

Configuration
-------------

All configuration information is stored in the `asset/settings.json` file. You can manually modify this file to adjust the following settings:



* Font and font size
* Default encoding format
* Default language
* Theme styles (support for dark/light modes)
* Auto-save interval

Main Modules
------------

* `library/highlighter/`: Syntax highlighting implementations for various languages
* `library/tab_manager.py`: Tab management logic
* `library/api.py`: Core configuration and initialization interface for the editor
* `main.py`: Main program entry and basic function implementation
* `asset/settings.json`: Stores user configurations
* `asset/theme/`: Theme style files
* `asset/packages/lang/`: Multilingual support files

Contribution
------------

Welcome to contribute code or suggest improvements! Please follow these steps:



1. Fork this repository.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push the branch (`git push origin feature/new-feature`).
5. Create a Pull Request.

License
-------

This project is licensed under the MIT License. Please refer to the LICENSE file for details.
Version History

* **v0.3.0**: Added multilingual support and theme switching functionality.
* **v0.2.0**: Implemented multi-tab and auto-save functions.
* **v0.1.1**: Optimized syntax highlighting logic.
* **v0.1.0**: Initial release, implemented basic editing and running functions.

Download
--------

You can download the latest version of Phoenix Editor from the Releases page.
Related Links

* [Gitee Project Homepage](https://gitee.com/creative-and-dream/phoenix-editor)
* [Issue Tracking](https://gitee.com/creative-and-dream/phoenix-editor/issues)
* Pull Request Submission Guidelines


