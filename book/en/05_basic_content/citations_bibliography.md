(citations_bibliography)=
# Citations and Bibliography

This template includes `sphinxcontrib-bibtex`, which manages bibliographic references using BibTeX files.

## References file

References are stored in `book/_static/references.bib`. Each entry follows this format:

```bibtex
@book{einstein1920,
  author    = {Albert Einstein},
  title     = {Relativity: The Special and General Theory},
  year      = {1920},
  publisher = {Henry Holt and Company}
}

@article{dirac1930,
  author  = {Paul A. M. Dirac},
  title   = {A Theory of Electrons and Protons},
  journal = {Proceedings of the Royal Society A},
  year    = {1930},
  volume  = {126},
  pages   = {360--365}
}
```

## Textual citation: `{cite:t}`

Inserts the author name followed by the year:

```md
{cite:t}`einstein1920` formulated the theory of relativity.
```

Result: {cite:t}`einstein1920` formulated the theory of relativity.

## Parenthetical citation: `{cite:p}`

Inserts author and year in parentheses:

```md
Quantum mechanics revolutionized physics {cite:p}`dirac1930`.
```

Result: Quantum mechanics revolutionized physics {cite:p}`dirac1930`.

## Multiple citations

Separate multiple keys with commas:

```md
Several authors contributed {cite:p}`einstein1920,dirac1930`.
```

Result: Several authors contributed {cite:p}`einstein1920,dirac1930`.

## Printing the bibliography

Add the `{bibliography}` directive at the end of your page or chapter:

````md
```{bibliography}
:filter: docname in docnames
```
````

Result:

```{bibliography}
:filter: docname in docnames
```

## Workflow

1. Add BibTeX entries to `_static/references.bib`.
2. Cite with `{cite:t}` or `{cite:p}` on any page.
3. If you want a local bibliography, add `{bibliography}` at the end of that page.
4. If you want a global bibliography for the whole book, use the `References` page included at the end of the table of contents.

```{warning}
Each citation key (e.g., `einstein1920`) must be unique across the entire `.bib` file. Duplicates will cause a build failure.
```
