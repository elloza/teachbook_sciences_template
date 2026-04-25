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
  version: "2.1"
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

## Gestión de escenas: evitar superposiciones

Manim NO borra automáticamente lo anterior por ti. Si cambias de bloque visual sin retirar o transformar los objetos anteriores, se quedan en pantalla y la escena acaba con elementos superpuestos.

### Regla obligatoria

Antes de introducir una idea nueva, decide explícitamente qué pasa con los objetos anteriores:

1. **Transformar** si hay continuidad conceptual.
2. **FadeOut/Uncreate** si la idea anterior ya terminó.
3. **Agrupar y retirar** si varios objetos forman una etapa completa.
4. **Mantener solo un ancla visual** si ayuda a orientarse, por ejemplo el título o los ejes.

### Patrón recomendado por etapas

```python
class MyScene(Scene):
    def construct(self):
        title = Text("Idea principal", font_size=42).to_edge(UP)
        self.play(Write(title))

        # Etapa 1
        step_1 = VGroup(
            MathTex("ax^2 + bx + c = 0"),
            Text("Forma general", font_size=28),
        ).arrange(DOWN, buff=0.4)
        self.play(FadeIn(step_1))
        self.wait(1)

        # Retirar la etapa 1 antes de crear la etapa 2
        self.play(FadeOut(step_1))

        # Etapa 2
        step_2 = VGroup(
            MathTex(r"\Delta = b^2 - 4ac", color=YELLOW),
            Text("El discriminante decide el número de soluciones", font_size=28),
        ).arrange(DOWN, buff=0.4)
        self.play(FadeIn(step_2))
        self.wait(1)
```

### Checklist anti-superposición

- [ ] Cada bloque visual está en un `VGroup` con nombre claro (`intro`, `formula_block`, `case_block`, etc.).
- [ ] Antes de crear una etapa nueva, hay un `FadeOut(...)`, `ReplacementTransform(...)` o limpieza equivalente.
- [ ] No se crean nuevos títulos encima de títulos antiguos: se transforma o se reutiliza el título existente.
- [ ] Si hay ejes o gráficas, se limpian etiquetas y curvas antiguas antes de dibujar las nuevas.
- [ ] No se usa `self.clear()` como atajo salvo en cortes muy claros: normalmente es mejor animar la salida para que el estudiante entienda la transición.

---

## Carpetas oficiales y ciclo de vida de assets

Usa SIEMPRE estas rutas. No improvises carpetas nuevas.

| Tipo | Ruta | ¿Se commitea? | Uso |
|---|---|---:|---|
| Fuente Manim | `manim_videos/YYYY-MM-DD_nombre/scene.py` | Sí | Código reproducible de la animación |
| Assets fuente de la escena | `manim_videos/YYYY-MM-DD_nombre/assets/` | Sí, si son necesarios | Imágenes, datos o audios usados por `scene.py` |
| Salida temporal de Manim | `media/` o `.manim_media/` | No | Carpeta generada por Manim durante renders; se puede borrar |
| Vídeo final para el libro | `book/_static/videos/nombre_estable.mp4` | Sí | Archivo que se referencia desde las páginas del libro |

Reglas importantes:

- La carpeta `media/` es basura de render. NO se sube.
- La carpeta `.manim_media/` también es basura de render. NO se sube.
- No dejes versiones de prueba como `video_v2.mp4`, `video_v3.mp4` en `book/_static/videos/`.
- El vídeo integrado en el libro debe tener nombre estable: `ecuacion_segundo_grado.mp4`, no `ecuacion_segundo_grado_v3.mp4`.
- Si una versión nueva reemplaza a otra, sobrescribe el `.mp4` estable y conserva el `scene.py` fuente actualizado.
- La página del libro nunca debe apuntar a un vídeo cuyo `scene.py` fuente no exista.

Render recomendado con salida temporal controlada:

```bash
manim -pql --media_dir .manim_media manim_videos/2026-04-25_onda_senoidal/scene.py SineWave
manim -pqh --media_dir .manim_media manim_videos/2026-04-25_onda_senoidal/scene.py SineWave
```

Después del render final, copia SOLO el `.mp4` final a:

```text
book/_static/videos/onda_senoidal.mp4
```

Y borra si hace falta:

```text
media/
.manim_media/
```

---

## PDF: qué ocurre con los vídeos

Los vídeos locales `.mp4` funcionan en HTML, pero NO se reproducen dentro del PDF. Por eso toda inserción de vídeo DEBE tener fallback LaTeX.

El fallback PDF debe indicar claramente qué pierde el lector y, si procede, mencionar que la animación está disponible en la versión HTML:

````md
```{raw} latex
\begin{center}
\textbf{Vídeo:} esta animación está disponible en la versión HTML del libro.
\end{center}
```
````

Si el contenido del vídeo es imprescindible para entender la página, añade además una explicación textual o una imagen estática antes/después del vídeo. El PDF no puede depender únicamente del `.mp4`.

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
manim -pql --media_dir .manim_media archivo.py Escena
```

Úsalo para iterar rápido.

### Render final recomendado

```bash
manim -pqh --media_dir .manim_media archivo.py Escena
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
3. Renderizar primero en baja calidad con `--media_dir .manim_media` para iterar
4. Corregir superposiciones: cada etapa anterior debe transformarse o salir de pantalla
5. Renderizar el resultado final en alta calidad
6. Copiar o mover SOLO el `.mp4` final a `book/_static/videos/` con nombre estable
7. Insertarlo en la página con el patrón HTML5 + fallback LaTeX
8. Borrar `media/` o `.manim_media/` antes de dejar el repo listo para subir

---

## Patrón de inserción en el libro

El vídeo final debe quedar en una ruta estable, por ejemplo:

- `book/_static/videos/mi_animacion.mp4`

No uses sufijos de prueba (`_v2`, `_final`, `_nuevo`) en el archivo referenciado por el libro. Esos nombres son típicos de borradores y hacen que el repositorio se ensucie.

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
| Salida temporal | Usar `media/` o `.manim_media/`; nunca commitear |
| Salida final | Guardar `.mp4` estable en `book/_static/videos/` |
| Inserción | Usar siempre patrón dual HTML + LaTeX fallback |
| PDF | El vídeo no se reproduce: añadir fallback textual y explicación si el vídeo es esencial |
| Calidad | El render final debe priorizar legibilidad y claridad |
| Multi-idioma | Si se documenta una animación en una página nueva, replicarla en todos los idiomas |
| ManimGL | Prohibido en este proyecto |

---

## Comandos recomendados

```bash
# Desarrollo rápido
manim -pql --media_dir .manim_media archivo.py NombreDeLaEscena

# Calidad media para revisión
manim -pqm --media_dir .manim_media archivo.py NombreDeLaEscena

# Calidad alta para integrar en el libro
manim -pqh --media_dir .manim_media archivo.py NombreDeLaEscena
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
- [ ] ¿No quedan carpetas `media/` o `.manim_media/` para subir?
- [ ] ¿No quedan vídeos de prueba `_v2`, `_v3`, `_final`, etc. en `book/_static/videos/`?
