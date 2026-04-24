(figures)=
# Figures and Images

Figures are essential in any teaching material. MyST offers two main directives: `{image}` (simple image) and `{figure}` (image with number and caption).

## Centered image with alt text

The `{image}` directive inserts an image without numbering:

```md
```{image} _static/logo.png
:alt: TeachBook project logo
:width: 60%
:align: center
```
```

Result:

```{image} _static/logo.png
:alt: TeachBook project logo
:width: 60%
:align: center
```

## Numbered figure with caption

The `{figure}` directive adds automatic numbering (`Figure 1`, `Figure 2`…):

````md
```{figure} _static/logo.png
:name: fig-logo-en
:width: 50%
:align: center

Official TeachBook project logo.
```
````

Result:

```{figure} _static/logo.png
:name: fig-logo-en
:width: 50%
:align: center

Official TeachBook project logo.
```

## Cross-reference to a figure

Use `{numref}` to reference figures by their number:

```md
The {numref}`fig-logo-en` shows the project logo.
```

Result: The {numref}`fig-logo-en` shows the project logo.

## Margin figure

Add `:figclass: margin` to place an image in the margin (HTML only):

````md
```{figure} _static/logo.png
:figclass: margin
:width: 100%

Logo in the margin.
```
````

Result:

```{figure} _static/logo.png
:figclass: margin
:width: 100%

Logo in the margin.
```

## Useful parameters

| Parameter | What it does | Example |
|-----------|--------------|---------|
| `:width:` | Width (`50%`, `200px`) | `:width: 80%` |
| `:align:` | Alignment (`left`, `center`, `right`) | `:align: center` |
| `:alt:` | Alt text (accessibility) | `:alt: Diagram` |
| `:name:` | Label for `{numref}` | `:name: fig-map` |
| `:figclass:` | CSS class (`margin`) | `:figclass: margin` |

```{tip}
Always add `:alt:` for accessibility. It is the text that screen readers see and displays if the image fails to load.
```
