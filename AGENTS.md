# TeachBook Sciences Template — Instrucciones para el Agente

## Objetivo del Proyecto

Plantilla para que docentes NO informáticos creen libros interactivos con Jupyter Book / TeachBooks.
El usuario típico es un profesor de la Facultad de Ciencias (USAL) que **nunca ha usado un terminal**.
Tu trabajo es que TODO funcione con fricción CERO.

## Reglas de Oro

1. **SIEMPRE** usa el entorno virtual `.venv`. Nunca instales paquetes en el Python global.
2. **Requiere Python 3.10+**. Si la versión es inferior, avisa al usuario.
3. **Acción > Explicación**. Ejecuta los scripts, no des clases de informática.
4. **Responde en español** siempre (salvo que te pidan lo contrario).
5. **No añadas frameworks JS** (React, Vue, etc.). El sistema de build es Jupyter Book, punto.
6. **No rompas la estructura multi-idioma**. Si añades contenido en un idioma, DEBE existir en TODOS los idiomas configurados.

## Arquitectura del Proyecto

```
teachbook_sciences_template/
├── book/                          # Contenido del libro
│   ├── _config_es.yml             # Configuración español (idioma principal)
│   ├── _config_en.yml             # Configuración inglés
│   ├── _toc_es.yml                # Tabla de contenidos español
│   ├── _toc_en.yml                # Tabla de contenidos inglés
│   ├── _static/                   # Assets estáticos (CSS, JS, logos, PDFs)
│   │   ├── custom.css
│   │   ├── custom.js
│   │   ├── logo.png
│   │   ├── usal_logo.png
│   │   └── references.bib         # Bibliografía BibTeX
│   ├── es/                        # Contenido en español
│   │   ├── intro.md
│   │   ├── 01_tutorial/           # Sección tutorial
│   │   ├── 02_grados/             # Sección ejemplos por grado
│   │   ├── 90_acerca_de.md
│   │   ├── 91_licencias.md
│   │   └── 92_como_citar.md
│   └── en/                        # Contenido en inglés (misma estructura)
├── scripts/                       # Scripts de automatización
│   ├── setup_env.py               # Configuración del entorno
│   ├── build_book.py              # Compilación HTML
│   ├── preview_book.py            # Vista previa con hot-reload
│   ├── export_pdf.py              # Exportación a PDF
│   ├── setup_latex.py             # Instalación de LaTeX (Tectonic)
│   └── git_helper.py              # Guardar y publicar
├── latex_templates/               # Plantillas LaTeX personalizadas
│   ├── common/                    # Estilos compartidos (jupyterBook.cls)
│   ├── es/                        # Ajustes español (language_support.tex)
│   └── en/                        # Ajustes inglés
├── .github/
│   ├── skills/                    # Skills del proyecto (FUENTE DE VERDAD)
│   └── workflows/deploy.yml       # GitHub Actions: build + deploy
├── AGENTS.md                      # Este archivo
└── requirements.txt               # Dependencias Python
```

## Idiomas Configurados

- **Español (es)**: Idioma principal. Config en `_config_es.yml`, TOC en `_toc_es.yml`.
- **Inglés (en)**: Idioma secundario. Config en `_config_en.yml`, TOC en `_toc_en.yml`.

Para añadir un nuevo idioma (ej: portugués `pt`):
1. Crear `book/_config_pt.yml` (copiar de `_config_es.yml` y adaptar).
2. Crear `book/_toc_pt.yml` (misma estructura que `_toc_es.yml`).
3. Crear `book/pt/` con TODO el contenido traducido (misma estructura de carpetas).
4. Crear `latex_templates/pt/language_support.tex` si se quiere PDF.
5. Añadir el código de idioma al mapa en `scripts/build_book.py` (`LANG_DISPLAY_NAMES`).

## Protocolo OBLIGATORIO para Añadir Contenido

Cuando añadas un capítulo o sección, DEBES seguir estos pasos EN ORDEN:

### 1. Crear el archivo de contenido en TODOS los idiomas
- Si creas `book/es/02_grados/grado_biologia/intro.md`, TAMBIÉN creas `book/en/02_degrees/grado_biology/intro.md`.
- Si un idioma no está traducido aún, crea el archivo con un placeholder: `*(Traducción pendiente)*`.

### 2. Actualizar TODOS los `_toc_<lang>.yml`
- Añadir la entrada en `_toc_es.yml` Y en `_toc_en.yml` (y cualquier otro idioma).
- La estructura debe ser IDÉNTICA en todos los TOC (mismas secciones, mismo orden).

### 3. Verificar que no hay contenido huérfano
- Ningún archivo `.md` en `book/es/` o `book/en/` debe existir sin estar referenciado en su `_toc.yml`.
- Ninguna entrada en `_toc.yml` debe apuntar a un archivo que no existe.

### 4. Commitear todo junto
- Los cambios de contenido + TOC deben ir en el mismo commit.

## Contenido Multimedia — Compatibilidad HTML y PDF

### Imágenes
```md
```{image} _static/mi_imagen.png
:alt: Descripción de la imagen
:width: 80%
:align: center
```
```
- Formato: PNG, JPG o SVG.
- Ubicación: `book/_static/` (compartido) o junto al `.md`.
- Funciona en HTML ✅ y PDF ✅.

### Figuras con etiqueta y referencia
```md
```{figure} _static/mi_imagen.png
---
width: 70%
name: fig-ejemplo
align: center
---
Descripción de la figura.
```

Como se ve en {numref}`fig-ejemplo`, la figura puede citarse.
```

### Videos de YouTube (compatible HTML + PDF)
Usa SIEMPRE este patrón para que funcione en ambos formatos:

```md
```{raw} html
<iframe width="560" height="315" src="https://www.youtube.com/embed/VIDEO_ID" frameborder="0" allowfullscreen></iframe>
```

```{raw} latex
\begin{center}
\textbf{Video:} \url{https://www.youtube.com/watch?v=VIDEO_ID}
\end{center}
```
```

- En HTML se ve el video embebido.
- En PDF se ve el enlace como texto.
- NUNCA uses `iframe` sin el bloque `{raw} latex` alternativo.

### Código Python ejecutable (Notebooks)
- Los notebooks `.ipynb` se ejecutan si `_config.yml` tiene `execute_notebooks: auto`.
- Por defecto están DESACTIVADOS (`off`) para velocidad. Actívalo solo si el usuario lo pide.

### Ecuaciones LaTeX
```md
Ecuación inline: $E = mc^2$

Ecuación display numerada:
$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$ (eq-gaussiana)

Referencia: la ecuación {eq}`eq-gaussiana` calcula...
```
- Funciona en HTML ✅ y PDF ✅ (requiere `dollarmath` en `myst_enable_extensions`, ya configurado).

### Citas Bibliográficas (BibTeX)
- Archivo de referencias: `book/_static/references.bib`.
- Citar en el texto: `{cite:t}`\`clave_cita\` (textual) o `{cite:p}`\`clave_cita\` (parentética).
- Añadir bibliografía al final: ````{bibliography}` / ````.

### Admonitions (cajas de información)
```md
```{admonition} Título
:class: tip

Contenido de la caja.
```
```
Clases disponibles: `tip`, `warning`, `note`, `important`, `caution`, `dropdown` (colapsable), `error`, `seealso`.

### Dropdowns (contenido colapsable)
```md
```{admonition} Solución
:class: dropdown

Aquí va la solución que el estudiante puede desplegar.
```
```

### Tabs (pestañas, requiere sphinx-design)
````md
```{tabbed} Python
```python
print("Hola")
```
```

```{tabbed} R
```r
print("Hola")
```
```
````

### Referencias cruzadas
- Secciones: `(mi-seccion)=` antes del título, luego `{ref}`\`mi-seccion\`
- Figuras: `{numref}`\`fig-ejemplo\`
- Ecuaciones: `{eq}`\`eq-gaussiana\`
- Tablas: `{numref}`\`tabla-ejemplo\`

### Diagramas con Kroki (HTML ✅ y PDF ✅)
Kroki convierte texto en diagramas SVG. Funciona en **HTML y PDF**. Usa Mermaid por defecto.

````md
```{kroki}
:type: mermaid
:align: center

flowchart LR
    A[Inicio] --> B[Proceso]
    B --> C[Fin]
```
````

Tipos disponibles: `mermaid` (recomendado), `plantuml`, `graphviz`, `excalidraw`, `vegalite`, `wavedrom`, `ditaa`, y 15+ más.
Requiere internet durante el build (no al leer). GitHub Actions siempre tiene internet.
Para añadir título: usar `{kroki-figure}` con `:caption: Título`.

**NO usar `{mermaid}`** (requiere sphinxcontrib-mermaid, no funciona en PDF). Usar siempre `{kroki}` con `:type: mermaid`.

### CircuitikZ (opción avanzada para circuitos precisos)
CircuitikZ usa LaTeX para generar esquemas eléctricos con acabado profesional. En TeachBook se usa como flujo **a imagen**:

1. Crear un archivo `.tex` con el circuito.
2. Renderizarlo con:

```bash
python scripts/render_circuitikz.py ruta/al/circuito.tex book/_static/generated/circuito.png
```

3. Insertar la imagen con `{figure}`.

```md
```{figure} _static/generated/circuito.png
:alt: Circuito generado con CircuitikZ
:width: 70%
:align: center

Circuito generado con CircuitikZ.
```
```

- Funciona en HTML ✅ y PDF ✅ porque el resultado final es una imagen.
- Requiere Tectonic (`python scripts/setup_latex.py`).
- **SchemDraw** sigue siendo la opción sencilla; **CircuitikZ** es la opción avanzada.

### HTML interactivo autocontenido (SOLO HTML)
````md
```{raw} html
<details>
<summary>Ver pista</summary>
<p>Texto oculto que se despliega.</p>
</details>
```

```{raw} latex
\textbf{Pista:} Texto alternativo para PDF.
```
````

### Tabla de compatibilidad HTML/PDF

| Elemento | HTML | PDF | Regla |
|---|---|---|---|
| Texto, listas, imágenes | ✅ | ✅ | Usar libremente |
| Ecuaciones LaTeX | ✅ | ✅ | Usar libremente |
| Admonitions | ✅ | ✅ | Usar libremente |
| Dropdowns | ✅ | ✅ expandido | Usar libremente |
| Diagramas Kroki (Mermaid, etc.) | ✅ | ✅ | Usar `{kroki}` con `:type: mermaid` |
| iframe/YouTube | ✅ | ❌ | Añadir `{raw} latex` con URL |
| Thebe live code | ✅ | ❌ | Código visible como texto |
| Tabs | ✅ | ❌ | Añadir alternativa sin tabs |
| HTML personalizado | ✅ | ❌ | Añadir `{raw} latex` fallback |

## Comandos Disponibles

Todos los comandos se ejecutan desde la raíz del proyecto usando el Python del `.venv`:

| Tarea | Comando | Qué hace |
|---|---|---|
| Configurar entorno | `python scripts/setup_env.py` | Crea .venv, instala deps, sincroniza skills |
| Configurar + dev | `python scripts/setup_env.py --dev` | Lo anterior + herramientas de testing |
| Solo sincronizar skills | `python scripts/setup_env.py --sync-only` | Copia skills a .claude/, .agents/, .agent/ sin tocar deps |
| Compilar libro | `python scripts/build_book.py` | Genera HTML multi-idioma en `book/_build/html/` |
| Vista previa | `python scripts/preview_book.py` | Servidor local con hot-reload en `localhost:8000` |
| Exportar PDF | `python scripts/export_pdf.py` | Genera PDF para cada idioma en `book/_static/` |
| Instalar LaTeX | `python scripts/setup_latex.py` | Instala Tectonic (motor LaTeX ligero) |
| Renderizar CircuitikZ | `python scripts/render_circuitikz.py <entrada.tex> [salida.png]` | Compila CircuitikZ y genera una imagen PNG |
| Convertir PDF a MD | `python scripts/pdf_to_markdown.py <ruta>` | Convierte PDFs a Markdown para el libro |
| Guardar y publicar | `python scripts/git_helper.py` | git add + commit + push |

**IMPORTANTE**: En Windows, si `python` no funciona, probar con `py`. Los scripts manejan ambas opciones.

## Publicación en GitHub Pages

El proyecto incluye un GitHub Action (`.github/workflows/deploy.yml`) que:
1. Se ejecuta automáticamente al hacer `push` a la rama principal.
2. Compila el libro HTML para todos los idiomas.
3. Genera los PDFs.
4. Despliega a GitHub Pages.

Para que funcione, el usuario debe:
1. Tener el repo en GitHub.
2. Ir a Settings → Pages → Source: `GitHub Actions`.
3. Hacer el primer `push`.

## Skills Disponibles

Las skills están en `.github/skills/` (fuente de verdad) y se sincronizan a `.claude/skills/`, `.agents/skills/` y `.agent/skills/` durante `setup_env.py`.

| Skill | Cuándo usarla |
|---|---|
| `teachbook-setup-environment` | Primera vez, algo no funciona, cambio de ordenador |
| `teachbook-build` | Compilar, ver HTML, verificar contenido |
| `teachbook-live-preview` | Escribir y ver cambios en tiempo real |
| `teachbook-export-pdf` | Generar PDF imprimible |
| `teachbook-git-publish` | Guardar y publicar cambios |
| `teachbook-add-content` | Añadir nuevos capítulos o secciones |
| `teachbook-multimedia` | Insertar imágenes, videos, ecuaciones |
| `teachbook-pdf-to-markdown` | Convertir PDFs existentes a Markdown |
| `teachbook-generate-diagram` | Crear diagramas Kroki (Mermaid, PlantUML, GraphViz, etc.) compatibles con HTML y PDF |
| `teachbook-generate-schemdraw-circuit` | Crear diagramas de circuitos eléctricos |
| `teachbook-generate-circuitikz` | Crear circuitos precisos con CircuitikZ exportados a imagen |
| `teachbook-generate-teaching-notebook` | Crear notebooks docentes con código ejecutable |
| `teachbook-generate-interactive-html` | Añadir HTML interactivo sin frameworks JS |
| `teachbook-generate-quiz` | Crear cuestionarios con respuestas ocultas |
| `teachbook-generate-thebe-pyodide-page` | Crear páginas con código ejecutable en navegador |
| `teachbook-review-teaching-quality` | Revisar calidad docente del contenido |
| `teachbook-review-html-pdf-compatibility` | Verificar que contenido funciona en HTML y PDF |

## Tono de Comunicación

- Amable, directo, en español.
- Sin jerga técnica innecesaria.
- Usa analogías de la vida real para explicar conceptos.
- Si algo falla, explica QUÉ falló y CÓMO se arregla, no POR QUÉ falló técnicamente.
