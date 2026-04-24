---
name: teachbook-generate-thebe-pyodide-page
description: >
  Crea páginas o notebooks con código Python ejecutable en el navegador usando Thebe Lite / Pyodide.
  El estudiante puede modificar y ejecutar código sin instalar nada.
  Trigger phrases: "thebe", "pyodide", "código live", "live code", "ejecutar en navegador",
  "código interactivo", "jupyterlite".
---

# Skill: Generar página con Thebe + Pyodide

## Objetivo

Crear una página o notebook donde el estudiante pueda ejecutar Python directamente en el navegador. No se instala nada en su ordenador: el kernel se lanza usando Pyodide/JupyterLite.

## Requisitos

- `sphinx-thebe` instalado (ya en `requirements.txt`)
- Config `_config_*.yml` con `sphinx_thebe` en `extra_extensions` y `thebe_config` con `use_thebe_lite: true`
- NO usar Binder como backend. Solo Pyodide/JupyterLite.

## Estructura de una página Thebe

```md
# Título de la página

Breve introducción.

```{admonition} Activar código interactivo
:class: tip

Pulsa el botón "Live Code" que aparece abajo para activar las celdas interactivas.
Podrás modificar el código y ejecutarlo directamente en tu navegador.
```

```{thebe-button} Activar código interactivo
```

```{code-cell} python
:tags: [thebe]

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.title("Función seno")
plt.grid(True)
plt.show()
```

Ahora modifica los parámetros y ejecuta de nuevo:

```{code-cell} python
:tags: [thebe]

# Modifica estos valores
amplitud = 2.0
frecuencia = 3

x = np.linspace(0, 2*np.pi, 200)
y = amplitud * np.sin(frecuencia * x)

plt.plot(x, y)
plt.title(f"Amplitud={amplitud}, Frecuencia={frecuencia}")
plt.grid(True)
plt.show()
```
```

## Reglas

1. Siempre incluir `{thebe-button}` al inicio de la sección interactiva.
2. Usar `:tags: [thebe]` en cada celda que deba ser interactiva.
3. Priorizar paquetes compatibles con Pyodide: numpy, matplotlib, pandas básico, math, random.
4. Evitar paquetes con binarios C (scipy puede fallar en Pyodide — si se usa, probar primero).
5. Cada celda debe ser autocontenida (no depender de celdas anteriores para importar).
6. Añadir comentarios en el código explicando qué puede modificar el estudiante.
7. Añadir siempre una alternativa estática para PDF (el código se ve como texto, sin ejecución).

## Paquetes compatibles con Pyodide

| Paquete | Estado | Notas |
|---|---|---|
| numpy | ✅ Completo | Funciona perfecto |
| matplotlib | ✅ Completo | Gráficos inline |
| pandas | ✅ Básico | I/O limitado |
| math | ✅ Nativo | Python estándar |
| random | ✅ Nativo | Python estándar |
| scipy | ⚠️ Parcial | Puede fallar — probar primero |
| scikit-learn | ⚠️ Parcial | Subconjunto disponible |
| schemdraw | ❌ No | Requiere binarios |

## Compatibilidad PDF

Thebe es SOLO HTML. En PDF:
- El botón no aparece.
- Las celdas se muestran como bloques de código estático.
- Añadir siempre texto explicativo alrededor del código para que tenga sentido en PDF.

## Template mínimo

```
1. Introducción (1 párrafo)
2. {thebe-button}
3. Celda de ejemplo (con thebe tag)
4. Texto: "Modifica los parámetros y ejecuta"
5. Celda modificable (con thebe tag)
6. Pregunta o actividad final
7. Nota: "Esta página es interactiva en la versión web. En PDF se muestra el código sin ejecución."
```
