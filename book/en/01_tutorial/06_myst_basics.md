# 6. MyST Markdown: The Basics

**MyST** (Mark up Your Scientific Text) is a Markdown extension designed for scientific and technical documents. It is the format used by Jupyter Book. If you know basic Markdown, you already know 80 % of MyST.

## Essential syntax

### Headings

```md
# Main title (H1)
## Section (H2)
### Subsection (H3)
```

### Text formatting

```md
**Bold** for strong emphasis.
*Italic* for terms or titles of works.
`inline code` for file names or commands.
```

### Lists

```md
- Unordered list item
- Another item
  - Sub-item with indentation

1. First step
2. Second step
3. Third step
```

### Links and images

```md
[Link text](https://example.com)
```

```md
![Alt text](path/to/image.png)
```

## Directives (special blocks)

MyST adds **directives** that don't exist in standard Markdown:

```{note}
This is a note. It appears highlighted in blue.
```

```{warning}
This is a warning. It appears highlighted in red/orange.
```

```{tip}
This is a tip. It appears highlighted in green.
```

You can create custom blocks with `admonition`:

```md
```{admonition} My custom title
Block content goes here.
```
```

## Math

Inline: the equation $E = mc^2$ is written as `$E = mc^2$`.

Display:

$$
\int_0^\infty e^{-x^2} \, dx = \frac{\sqrt{\pi}}{2}
$$

Written as `$$ ... $$` on its own line.

## Tables

```md

The following table summarizes the main elements of this section.

**Table. Tables.**

| Column A | Column B | Column C |
|----------|----------|----------|
| data 1   | data 2   | data 3   |
| data 4   | data 5   | data 6   |
```

Result:


The following table summarizes the main elements of this section.

**Table. Tables.**

| Column A | Column B | Column C |
|----------|----------|----------|
| data 1   | data 2   | data 3   |
| data 4   | data 5   | data 6   |

## Code blocks

````md
```python
def greet(name):
    return f"Hello, {name}!"
```
````

```{admonition} Tip
:class: tip
Don't try to memorize all the syntax. Use an AI assistant to generate the MyST you need and learn as you go.
```
