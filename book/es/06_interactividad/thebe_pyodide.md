# Thebe + Pyodide: Código en Vivo

**Thebe** permite ejecutar código Python directamente en el navegador del lector, sin necesidad de instalar nada. Funciona gracias a **Pyodide**, una versión de Python compilada a WebAssembly.

```{warning}
Thebe es una funcionalidad **solo HTML**. No está disponible en la exportación PDF. Además, requiere la extensión `sphinx-thebe` configurada en tu `_config.yml`.
```

## ¿Cómo funciona?

1. El lector pulsa el botón **"Live Code"** en la página.
2. Se carga Pyodide en el navegador (puede tardar unos segundos la primera vez).
3. Las celdas de código se vuelven editables y ejecutables.

## Botón de activación

Para mostrar el botón "Live Code" en una página, añade la directiva:

````md
```{thebe-button}
```
````

## Ejemplo: celda ejecutable

````md
```{code-cell} python
:tags: [thebe]

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y, label='sin(x)')
plt.title('Onda senoidal')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
```
````

El lector puede modificar los parámetros (por ejemplo, cambiar `np.sin` por `np.cos`) y volver a ejecutar la celda.

## Configuración necesaria

Para activar Thebe, tu `_config.yml` debe incluir:

```yaml
sphinx:
  extensions:
    - sphinx_thebe
  config:
    thebe_config:
      repository_url: "https://github.com/tu-usuario/tu-repo"
      repository_branch: "main"
```

```{admonition} Alternativa más sencilla
:class: tip
Si no quieres configurar Thebe, puedes usar **Google Colab**. Sube tu notebook a Colab y comparte el enlace en tu TeachBook. Los estudiantes podrán ejecutar el código en la nube sin instalación.
```
