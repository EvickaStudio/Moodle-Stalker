# Information

This is a POC/ translation of the Turndown library. The original library is written in JavaScript and can be found [here](https://github.com/mixmark-io/turndown). Its main purpose is to convert html to markdown, and as its one of the best libraries for this purpose, I decided to translate it to Python for less dependencys and overhead.

This version has been translated to Python (with a lot of help from my friend chatty) and is not as feature complete as the original library. I do not plan to add any more features or fix anything that is not necessary for my use case. If you want to use this library or want to further develop it, feel free to fork it or just to copy the code.

The repository for the python version is [here](https://github.com/EvickaStudio/turndown-python), as the version used here is refactored and renamed.

## Usage

Here is a simple example of how to use the library:

```python
from src.turndown import TurndownService

td = TurndownService({"headingStyle": "atx", "codeBlockStyle": "fenced"})

html = "<h1>Hello, World!</h1>"
markdown = td.turndown(html)
print(markdown)
```
