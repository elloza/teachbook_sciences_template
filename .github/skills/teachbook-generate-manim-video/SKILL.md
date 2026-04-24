---
name: teachbook-generate-manim-video
description: >
  Genera animaciones educativas con Manim Community Edition y las integra como vídeos locales HTML5 en el libro.
  Prioriza claridad visual, tipografía legible, ritmo didáctico y calidad final de render.
  SOLO usa Manim Community (no ManimGL). Trigger phrases: "manim", "animación matemática",
  "video animado", "animación física", "animación geometría", "video local", "mp4",
  "3b1b style", "explicación visual", "animación educativa".
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "2.0"
---

## Cuándo usar

- Cuando el usuario quiera una **animación educativa** de matemáticas, física o informática
- Cuando una explicación estática se quede corta y haga falta **mostrar un proceso**
- Cuando se necesite un **vídeo local** dentro del libro, no solo YouTube
- Cuando el objetivo sea explicar una idea visualmente, no solo “tener un vídeo”

## Regla principal

**La prioridad NO es “hacer un vídeo”. La prioridad es que el vídeo SE ENTIENDA y SE VEA BIEN.**

Si una animación queda recargada, pequeña, rápida o confusa, está mal aunque técnicamente funcione.

---

## Framework permitido

### SOLO Manim Community

Usar exclusivamente:

```python
from manim import *
```

NO usar:
- `from manimlib import *`
- `manimgl`
- APIs o ejemplos de 3Blue1Brown / ManimGL
- escenas o comandos incompatibles con Manim Community

Si hay duda entre dos APIs, elegir siempre la de **Manim Community Edition**.

---

## Objetivo visual del proyecto

Las animaciones deben sentirse:

- **claras**
- **legibles**
- **limpias**
- **docentes**
- **con ritmo pausado**

No buscamos fuegos artificiales. Buscamos que un estudiante o profesor vea el vídeo y diga:

> “Ahora lo entiendo.”

---

## Estándar de calidad visual

### 1. Fondo limpio

- Preferir fondo oscuro o neutro si mejora el contraste
- Evitar fondos con ruido visual
- El contenido importante debe destacar a primera vista

### 2. Tipografía grande y legible

- El texto debe poder leerse embebido dentro de una página del libro
- Evitar textos pequeños
- Para fórmulas, usar `MathTex` con tamaño suficiente

### 3. Poco contenido simultáneo

- Mostrar pocas cosas a la vez
- Introducir complejidad **progresivamente**
- Mejor 3 pasos claros que 12 elementos en pantalla al mismo tiempo

### 4. Color con significado

Usar colores de forma consistente:

- **entrada / dato inicial** → azul
- **resultado / salida** → verde
- **resaltado / foco** → amarillo
- **error / oposición / negativo** → rojo

No cambiar colores arbitrariamente.

### 5. Movimiento con propósito

- Si algo se mueve, debe ayudar a entender
- No rotar cámara ni objetos “porque queda bonito”
- Evitar movimientos bruscos o gratuitos

### 6. Tiempo para pensar

- Añadir `self.wait()` en momentos clave
- Dejar respirar la escena después de una idea importante
- La comprensión necesita pausas

---

## Patrones didácticos recomendados

### Patrón 1: Presentar → transformar → concluir

1. mostrar estado inicial
2. animar el cambio
3. dejar el resultado quieto un momento

### Patrón 2: Resaltar una sola idea por escena

Cada escena debe responder a una pregunta concreta:

- ¿qué objeto estamos estudiando?
- ¿qué cambia?
- ¿qué conclusión debe llevarse el alumno?

### Patrón 3: Mostrar la relación visualmente

Siempre que puedas:

- transforma en vez de sustituir
- conecta con flechas en vez de explicar con mucho texto
- usa color y posición para mostrar relaciones

---

## Estructura recomendada de una escena

```python
from manim import *
import numpy as np


class MyScene(Scene):
    def construct(self):
        # 1. Introducción visual
        title = Text("Onda senoidal", font_size=42)
        title.to_edge(UP)

        axes = Axes(
            x_range=[0, 2 * np.pi, np.pi / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=4,
        )

        curve = axes.plot(lambda x: np.sin(x), color=BLUE)

        self.play(Write(title))
        self.play(Create(axes))
        self.play(Create(curve), run_time=2)
        self.wait(1)
```

---

## Parámetros de render recomendados

### Desarrollo rápido

```bash
manim -pql archivo.py Escena
```

Úsalo para iterar rápido.

### Render final recomendado

```bash
manim -pqh archivo.py Escena
```

Esto debe ser el estándar para el vídeo que termina en el libro.

### Regla de calidad

- `-pql` → probar
- `-pqm` → revisión intermedia
- `-pqh` → salida final seria

**No meter en el libro un vídeo renderizado solo en baja calidad salvo que el usuario lo pida explícitamente.**

---

## Organización del repositorio

Los **scripts fuente** de Manim NO deben quedar dispersos por el repo. Guardarlos siempre así:

- `manim_videos/YYYY-MM-DD_nombre/scene.py`

Ejemplos:

- `manim_videos/2026-04-25_onda_senoidal/scene.py`
- `manim_videos/2026-04-25_onda_senoidal/README.md`
- `manim_videos/2026-04-25_onda_senoidal/assets/` si hace falta

Reglas:

- usar fecha ISO `YYYY-MM-DD`
- nombre corto y descriptivo
- una carpeta por animación o pequeño grupo relacionado

---

## Flujo recomendado del proyecto

1. Planear la idea visual: qué se quiere enseñar
2. Crear el script en `manim_videos/YYYY-MM-DD_nombre/scene.py`
3. Renderizar primero en baja calidad para iterar
4. Renderizar el resultado final en alta calidad
5. Copiar o mover el `.mp4` a `book/_static/videos/`
6. Insertarlo en la página con el patrón HTML5 + fallback LaTeX

---

## Patrón de inserción en el libro

El vídeo final debe quedar en una ruta estable, por ejemplo:

- `book/_static/videos/mi_animacion.mp4`

Inserción recomendada:

````md
```{raw} html
<video width="720" controls>
  <source src="_static/videos/mi_animacion.mp4" type="video/mp4">
  Tu navegador no soporta vídeo HTML5.
</video>
```

```{raw} latex
\begin{center}
\textbf{Vídeo:} consulte la versión HTML del libro para reproducir la animación.
\end{center}
```
````

---

## Ejemplo mínimo bueno

```python
from manim import *
import numpy as np


class SineWave(Scene):
    def construct(self):
        title = Text("Onda senoidal", font_size=42)
        title.to_edge(UP)

        axes = Axes(
            x_range=[0, 2 * np.pi, np.pi / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=4,
        )

        curve = axes.plot(lambda x: np.sin(x), color=BLUE)
        label = MathTex("y = \\sin(x)").next_to(axes, UP)

        self.play(Write(title))
        self.play(Create(axes))
        self.play(Create(curve), Write(label), run_time=2)
        self.wait(1)
```

Render:

```bash
manim -pqh manim_videos/2026-04-25_onda_senoidal/scene.py SineWave
```

---

## Qué hace que un vídeo “se vea bien”

### Sí hacer

- usar composiciones limpias
- mantener buen contraste
- usar textos grandes
- usar `Transform`, `ReplacementTransform`, `Create`, `Write` con intención
- añadir pausas
- revisar el render final antes de integrarlo

### No hacer

- texto diminuto
- demasiados objetos simultáneos
- animaciones frenéticas
- colores sin criterio
- cámara moviéndose sin aportar nada
- vídeos largos para explicar una idea pequeña

---

## Requisitos

- Python 3.10+
- FFmpeg instalado
- Manim Community instalado en el entorno que se use para renderizar
- LaTeX puede ser útil para `MathTex` complejos

Ejemplo de instalación manual:

```bash
python -m pip install manim
manim --version
ffmpeg -version
```

---

## Reglas del proyecto

| Regla | Detalle |
|---|---|
| Framework | SOLO **Manim Community Edition** |
| Import | `from manim import *` |
| Fuente | Guardar scripts en `manim_videos/YYYY-MM-DD_nombre/` |
| Salida final | Guardar `.mp4` en `book/_static/videos/` |
| Inserción | Usar siempre patrón dual HTML + LaTeX fallback |
| Calidad | El render final debe priorizar legibilidad y claridad |
| Multi-idioma | Si se documenta una animación en una página nueva, replicarla en todos los idiomas |
| ManimGL | Prohibido en este proyecto |

---

## Comandos recomendados

```bash
# Desarrollo rápido
manim -pql archivo.py NombreDeLaEscena

# Calidad media para revisión
manim -pqm archivo.py NombreDeLaEscena

# Calidad alta para integrar en el libro
manim -pqh archivo.py NombreDeLaEscena
```

---

## Checklist antes de dar por bueno un vídeo

- [ ] ¿Se entiende la idea sin pausar constantemente?
- [ ] ¿El texto se lee bien?
- [ ] ¿Los colores tienen sentido?
- [ ] ¿La escena tiene demasiado ruido?
- [ ] ¿El render final no está en baja calidad?
- [ ] ¿El `.mp4` quedó en `book/_static/videos/`?
- [ ] ¿La fuente quedó ordenada en `manim_videos/YYYY-MM-DD_nombre/`?
- [ ] ¿La página del libro tiene fallback para PDF?
