[![](https://img.shields.io/pypi/v/foliantcontrib.utils.svg)](https://pypi.org/project/foliantcontrib.utils/) [![](https://img.shields.io/github/v/tag/foliant-docs/foliantcontrib.utils.svg?label=GitHub)](https://github.com/foliant-docs/foliantcontrib.utils)

# Generic utils

This module contains various utils for inner use in Foliant preprocessors, backends and other modules.

## Installation

To use functions from this module, install it with command

```bash
pip3 install foliantcontrib.utils
```

## Usage

Right now this module offers only one useful function, called `prepend_file`. This function properly prepends the markdown file with text string. If file starts with a YAML Front Matter or a heading, there are options to insert the content after them.

```python
>>> from foliant.contrib.utils import prepend_file

```

Let's assume we have a file which begins with YAML Front Matter:

```
---
author: John
---

Contents.
```

If we want to add some content to the beginning of this file for some reason, we will probably want to add this content *after* the YAML Front Matter, otherwise it will be broken by our insertion.

We can use the `prepend_file` function which will manage this case for us:

```python
>>> prepend_file('myfile.md', '\nInserted content\n', before_yfm=False)

```

Notice the `before_yfm` paramter. If it is `False` (which it is by default), the content will be added *after* YAML Front Matter. The result would be:

```
---
author: John
---

Inserted content

Contents.

```

There's also an option `before_heading`. If it is `False` (it's `True` by default), the content will be inserted after the first heading, if the document starts with a heading. Some backends treat these heading in a special way, that's why sometimes it makes sense to insert things after them.

Example:

```
# System description

Contents.
```

let's add some text:

```python
>>> prepend_file('myfile.md', '\nInserted content\n', before_heading=False)
```

Result:

```
# System description

Inserted content

Contents.
```