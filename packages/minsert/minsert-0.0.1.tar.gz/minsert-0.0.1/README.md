# minsert

Insert dynamic content in markdown, without using a separate template file.

## Motivation

Inspired by jinja. 😂

Your actual markdown file is the template file itself.
Just make a block of content just by using comments, which indicate the start and end of the block.

This is really great for GitHub repo README. No hassle of creating a separate template file.

## Installation

```shell
pip install minsert
```

## Syntax

Start a block : `<!-- ➡️ thing1 ⬅️ -->`

End of a block: `<!-- 🛑 -->`

Emoji Tip:

- use :emojisense: in VS Code
- ➡️ `:arrow_right:`
- ⬅️ `:arrow_left:`
- 🛑 `:stop_sign:`

## Usage

```python
from minsert import MarkdownFile
file = MarkdownFile('test.md')
things = {'thing1': 'hi hello',
          'thing2': 'ping pong',
          }
file.insert(things)

```

## Example

Take a long hard look at this gif!

![minsert](https://user-images.githubusercontent.com/66209958/99037312-7bb39700-25a9-11eb-9d1e-2a15d76a8d10.gif)
