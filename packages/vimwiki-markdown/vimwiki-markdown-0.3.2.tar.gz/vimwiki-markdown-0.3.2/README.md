# vimwiki-markdown

[vimwiki](https://github.com/vimwiki/vimwiki) markdown file to html with syntax
highlighting.

## Install

```
pip install vimwiki-markdown
```

## Usage

Add the following to your `~/.vimrc`:

```vim
let g:vimwiki_list = [{
	\ 'path': '~/vimwiki',
	\ 'template_path': '~/vimwiki/templates/',
	\ 'template_default': 'default',
	\ 'syntax': 'markdown',
	\ 'ext': '.md',
	\ 'path_html': '~/vimwiki/site_html/',
	\ 'custom_wiki2html': 'vimwiki_markdown',
	\ 'template_ext': '.tpl'}]
```

## Markdown extensions

The following [markdown extensions](https://python-markdown.github.io/extensions/)
are activated by default:

- [fenced_code](https://python-markdown.github.io/extensions/fenced_code_blocks/)
- [tables](https://python-markdown.github.io/extensions/tables/)
- [CodeHilite](https://python-markdown.github.io/extensions/code_hilite/)

But you can add more extensions using `VIMWIKI_MARKDOWN_EXTENSIONS` environment
variable, which is a coma separated list of extensions.

## Syntax highlighting

Syntax highlighting is provided by [Pygments](http://pygments.org/), which will
try to guess language by default.

You can use regular markdown indented code blocks:

```
	:::python
	for value range(42):
		print(value)
```

Or Fenced Code Blocks

	```python
	for value range(42):
		print(value)
	```

You can also highlight line using `hl_lines` argument:

	```python hl_lines="1 3"
	for value range(42):
		print(value)
	```

Pygments can generate CSS rules for you. Just run the following command from
the command line:

```
pygmentize -S default -f html -a .codehilite > styles.css
```

If you would like to use a different theme, swap out `default` for the desired
theme. For a list of themes installed on your system, run the following
command:

```
pygmentize -L style
```

If you are lazy you can juste use the one in this repository inside `css`
directory which provide the `monokai` theme.
