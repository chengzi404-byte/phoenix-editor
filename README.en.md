# Phoenix Editor
> A simple and easy-to-use lightweight multi-language development IDE

## Download Method
Select the release version in the Gitee repository and choose the version you need. The explanations for all versions are as follows:

- `.release` Official version
- `.dev` Development version
- `.fix` Fix for the previous version
Please note: We only provide the source code; the specific program needs to be compiled into an exe file by yourself.

## Usage
### 1. Explanation of the ./asset/settings.json file
Open the `./asset/settings.json file`; the default format is as follows:

```json5
{
    "file-encoding": "utf-8",
    "lang": "zh-cn",
    "font": "Consolas",
    "fontsize": 12,
    "code": "python",
    "syntax-highlighting": {
        "theme": "github-light",
        "enable-type-hints": true,
        "enable-docstrings": true
    }
}
```
- code(str) Development language, determines the code highlighting. It can be one of the programming languages listed below or one from the `./library/highlighter/` directory:
    ```
      base
      bash
      html
      cpp
      html
      java
      objc
      python
      ruby 
      rust
      javascript
    ```
<font color=yellow>Note: The above content will be continuously updated according to the latest version; for detailed information, please refer to the Wiki.</font>
- file-encoding(str) File encoding, determines the format for opening and saving files, default is utf-8.
- font(str) Global font setting; please ensure the font is located in the C:\Windows\Font directory. You can add suffixes like Regular.
- fontsize(int) Global font size setting.
- syntax-highlighting(dict) Code highlighting rules.
  - theme(str) Can be one of the themes listed below or any custom theme you add. The default themes are:
  ```
  vscode-dark
  github-light
  one-dark-pro
  solarized-dark
  monokai
  ```
  - enable-type-hints (deprecated)
  - enable-docstrings (deprecated)
### 2. Adding Themes
If you want to add a theme, please use the following template as a reference:

``` json5
{
    "base": {
        "background": "#282C34",
        "foreground": "#ABB2BF",
        "insertbackground": "#ABB2BF",
        "selectbackground": "#3E4451",
        "selectforeground": "#ABB2BF"
    },
    "keyword": "#C678DD",
    "control": "#C678DD",
    "operator": "#56B6C2",
    "punctuation": "#ABB2BF",
    
    "class": "#E5C07B",
    "function": "#61AFEF",
    "method": "#61AFEF",
    "variable": "#E06C75",
    "parameter": "#ABB2BF",
    "property": "#E06C75",
    
    "string": "#98C379",
    "number": "#D19A66",
    "boolean": "#D19A66",
    "null": "#D19A66",
    "constant": "#D19A66",
    
    "comment": "#7F848E",
    "docstring": "#7F848E",
    "todo": "#FF8C00",
    
    "decorator": "#61AFEF",
    "builtin": "#56B6C2",
    "self": "#E06C75",
    "namespace": "#E5C07B",
    
    "type": "#E5C07B",
    "type_annotation": "#E5C07B",
    "interface": "#E5C07B"
} 
```
After writing, save the entire file with a .json extension and place it in the ./asset/theme/ directory so that the software can use this file.

To use this theme, adjust the settings in ./asset/settings.json.

### 3. Code Execution
Currently, code execution only supports Python, so detailed code highlighting is only available for Python.

If you need multi-language development, you can modify the source code to implement this feature.

### 4. Multi-file Support
This feature will be worked on in the upcoming versions.

## Support
If you are interested in this project, please give our project a star. The project is completely open-source, allowing you to use it in your own projects.