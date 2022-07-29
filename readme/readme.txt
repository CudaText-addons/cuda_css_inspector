CSS Inspector plugin for CudaText.
In HTML documents (with lexer "HTML") it shows CSS properties of current tag under caret.
To call plugin, use menu item "Plugins / CSS Inspector", it will show side panel with "CSS" icon.
When you move caret in editor, this panel updates its info.

It calculates tag properties given by: 
- class
- id
- "style" tag
Properties can be set:
- straight in HTML by using "style" tag
- in the CSS file, and connected by the "link" tag

Libraries
---------
- Windows: plugin uses local libraries in its folder.
- Unix: plugin needs additional libs in OS Python, install them like this:
$ pip3 install lxml
$ pip3 install cssselect


Authors:
- @Medvosa at GitHub
- Alexey Torgashin (CudaText)
License: MIT
