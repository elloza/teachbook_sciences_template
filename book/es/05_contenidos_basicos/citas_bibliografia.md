(citas_bibliografia)=
# Citas y bibliografía

Esta plantilla incluye `sphinxcontrib-bibtex`, que permite gestionar referencias bibliográficas con archivos BibTeX.

## Archivo de referencias

Las referencias se guardan en `book/_static/references.bib`. Cada entrada tiene este formato:

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

## Cita textual: `{cite:t}`

Inserta el nombre del autor seguido del año:

```md
{cite:t}`einstein1920` formuló la teoría de la relatividad.
```

Resultado: {cite:t}`einstein1920` formuló la teoría de la relatividad.

## Cita entre paréntesis: `{cite:p}`

Inserta autor y año entre paréntesis:

```md
La mecánica cuántica revolucionó la física {cite:p}`dirac1930`.
```

Resultado: La mecánica cuántica revolucionó la física {cite:p}`dirac1930`.

## Múltiples citas

Separa varias claves con comas:

```md
Varios autores contribuyeron {cite:p}`einstein1920,dirac1930`.
```

Resultado: Varios autores contribuyeron {cite:p}`einstein1920,dirac1930`.

## Imprimir la bibliografía

Añade la directiva `{bibliography}` al final de tu página o capítulo:

````md
```{bibliography}
:filter: docname in docnames
```
````

Resultado:

```{bibliography}
:filter: docname in docnames
```

## Flujo de trabajo

1. Añade las entradas BibTeX a `_static/references.bib`.
2. Cita con `{cite:t}` o `{cite:p}` en cualquier página.
3. Añade `{bibliography}` donde quieras que aparezca la lista de referencias.

```{warning}
Cada clave de cita (ej: `einstein1920`) debe ser única en todo el archivo `.bib`. Si se duplica, la compilación fallará.
```
