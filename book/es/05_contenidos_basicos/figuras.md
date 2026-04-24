(figuras)=
# Figuras e imágenes

Las figuras son esenciales en cualquier material docente. MyST ofrece dos directivas principales: `{image}` (imagen simple) y `{figure}` (imagen con número y pie de foto).

## Imagen centrada con texto alternativo

La directiva `{image}` inserta una imagen sin numeración:

```md
```{image} _static/logo.png
:alt: Logo del proyecto TeachBook
:width: 60%
:align: center
```
```

Resultado:

```{image} _static/logo.png
:alt: Logo del proyecto TeachBook
:width: 60%
:align: center
```

## Figura numerada con pie de foto

La directiva `{figure}` añade numeración automática (`Figura 1`, `Figura 2`…):

````md
```{figure} _static/logo.png
:name: fig-logo
:width: 50%
:align: center

Logo oficial del proyecto TeachBook.
```
````

Resultado:

```{figure} _static/logo.png
:name: fig-logo
:width: 50%
:align: center

Logo oficial del proyecto TeachBook.
```

## Referencia cruzada a una figura

Usa `{numref}` para referenciar figuras por su número:

```md
En la {numref}`fig-logo` se muestra el logo del proyecto.
```

Resultado: En la {numref}`fig-logo` se muestra el logo del proyecto.

## Figura en el margen

Añade `:figclass: margin` para colocar una imagen en el margen (solo HTML):

````md
```{figure} _static/logo.png
:figclass: margin
:width: 100%

Logo en el margen.
```
````

Resultado:

```{figure} _static/logo.png
:figclass: margin
:width: 100%

Logo en el margen.
```

## Parámetros útiles

| Parámetro | Qué hace | Ejemplo |
|-----------|----------|---------|
| `:width:` | Ancho (`50%`, `200px`) | `:width: 80%` |
| `:align:` | Alineación (`left`, `center`, `right`) | `:align: center` |
| `:alt:` | Texto alternativo (accesibilidad) | `:alt: Diagrama` |
| `:name:` | Etiqueta para `{numref}` | `:name: fig-mapa` |
| `:figclass:` | Clase CSS (`margin`) | `:figclass: margin` |

```{tip}
Siempre añade `:alt:` para accesibilidad. Es el texto que ven los lectores de pantalla y se muestra si la imagen no carga.
```
