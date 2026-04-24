# Thebe + Pyodide: Código en Vivo

**Thebe** permite ejecutar código Python directamente en el navegador del lector, sin necesidad de instalar nada. Funciona gracias a **Pyodide**, una versión de Python compilada a WebAssembly.

```{warning}
Thebe es una funcionalidad **solo HTML**. No está disponible en la exportación PDF.
```

## ¿Cómo funciona?

1. Pulsa el botón **"Live Code"** que aparece debajo.
2. Se carga Pyodide en el navegador (puede tardar unos segundos la primera vez).
3. Las celdas de código se vuelven editables y ejecutables — ¡pruébalo!

---

## Prueba: código ejecutable

Pulsa el botón para activar el modo interactivo. Luego puedes editar y ejecutar las celdas.

```{thebe-button}
```

````{div} full-width
```{code-block} python
:class: thebe

import numpy as np

# Crea un array de 0 a 2π
x = np.linspace(0, 2 * np.pi, 100)

# Calcula seno y coseno
y_sin = np.sin(x)
y_cos = np.cos(x)

print(f"Media del seno: {np.mean(y_sin):.4f}")
print(f"Media del coseno: {np.mean(y_cos):.4f}")
print(f"Valor máximo del seno: {np.max(y_sin):.4f}")
print("¡Funciona! Prueba a cambiar np.sin por otra función.")
```
````

````{div} full-width
```{code-block} python
:class: thebe

import matplotlib.pyplot as plt
import numpy as np

# Parámetros modificables
frecuencia = 2   # Hz
amplitud = 1.0   # Escala
fase = 0         # Radiantes

t = np.linspace(0, 2*np.pi, 200)
señal = amplitud * np.sin(frecuencia * t + fase)

plt.figure(figsize=(8, 3))
plt.plot(t, señal, 'b-', linewidth=2, label=f'{amplitud}·sin({frecuencia}t + {fase})')
plt.title('Señal Senoidal Interactiva')
plt.xlabel('Tiempo (rad)')
plt.ylabel('Amplitud')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()
```
````

---

## ¿Cómo añadir esto a tus páginas?

### 1. Botón de activación

Añade esta directiva donde quieras que aparezca el botón "Live Code":

````md
```{thebe-button}
```
````

### 2. Celda ejecutable

Usa `code-block` con la clase `thebe`:

````md
```{code-block} python
:class: thebe

import numpy as np
print("¡Hola desde el navegador!")
```
````

### 3. Configuración del `_config.yml`

Tu `_config.yml` debe incluir la extensión `sphinx-thebe`:

```yaml
sphinx:
  extra_extensions:
    - sphinx_thebe
  config:
    thebe_config:
      use_thebe_lite: true
      always_load: false
```

Esta configuración usa **Thebe Lite** con Pyodide, que carga Python directamente en el navegador sin necesidad de Binder.

```{admonition} Alternativa más sencilla
:class: tip
Si no quieres configurar Thebe, puedes usar **Google Colab**. Sube tu notebook a Colab y comparte el enlace en tu TeachBook. Los estudiantes podrán ejecutar el código en la nube sin instalación.
```
