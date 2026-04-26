---
name: teachbook-export-pdf
description: >
  Exporta el libro completo a formato PDF para cada idioma configurado.
  Genera LaTeX intermedio, aplica plantillas personalizadas y compila con XeLaTeX/latexmk.
  Trigger phrases: "exportar PDF", "genera PDF", "PDF", "imprimible", "versión impresa",
  "quiero imprimir", "descargar PDF", "export pdf", "generate PDF".
---

# Skill: Exportar a PDF

## Cuándo usar esta skill

- Cuando se necesita una versión imprimible del libro.
- Para generar el archivo PDF que se descargará desde la web.
- Al finalizar el contenido y querer una copia offline.

## Qué hace `export_pdf.py`

1. **Verifica que LaTeX esté instalado**. Prefiere una toolchain completa `latexmk` + `xelatex` (TeX Live/MiKTeX); Tectonic queda solo como fallback ligero.
2. **Detecta los idiomas** desde los archivos `_config_<lang>.yml`.
3. **Para cada idioma**, genera los archivos LaTeX, aplica plantillas personalizadas y compila a PDF.
4. **Copia los PDFs** resultantes a `book/_static/`.

## Ubicación de salida

```
book/_static/teachbook_es.pdf    ← PDF en español
book/_static/teachbook_en.pdf    ← PDF en inglés
```

## Requisito previo: LaTeX real multi-OS

El PDF requiere un motor LaTeX. Para el libro completo, el flujo robusto usa **XeLaTeX + latexmk**:

- Linux/CI: TeX Live.
- macOS/CI: BasicTeX/TeX Live.
- Windows/CI: MiKTeX + Perl.

Tectonic se mantiene solo como fallback ligero, porque el libro completo ha provocado crashes de Tectonic en CI.

Regla importante para agentes: primero usa siempre `scripts/setup_latex.py`. Para CI o generación garantizada usa `scripts/setup_latex.py --ci-full`.

### Verificar si la toolchain completa está instalada

```bash
latexmk --version
xelatex --version
```

También puedes comprobarlo con el script:

```bash
python scripts/setup_latex.py --check-full
```

### Si NO está instalado, ejecutar PRIMERO:

El agente DEBE usar el Python del entorno virtual (`.venv`):

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/setup_latex.py --yes` |
| Windows PowerShell | `.venv\Scripts\python.exe scripts\setup_latex.py --yes` |

Para CI o para una generación multi-OS real, usa:

| Sistema | Comando CI |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/setup_latex.py --ci-full` |
| Windows PowerShell | `.venv\Scripts\python.exe scripts\setup_latex.py --ci-full` |

`--ci-full` instala una distribución LaTeX real mediante el gestor del sistema disponible en GitHub Actions.

Para comprobar sin instalar:

```bash
python scripts/setup_latex.py --check
python scripts/setup_latex.py --check-full
```

## Instrucciones para el agente

### Paso 1: Verificar LaTeX

Si `latexmk` + `xelatex` no están instalados, ejecutar `setup_latex.py --yes` primero. En CI o si el usuario pide generación garantizada, ejecutar `setup_latex.py --ci-full`.

### Paso 2: Ejecutar la exportación

El agente DEBE usar el Python del entorno virtual (`.venv`):

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/export_pdf.py` |
| Windows PowerShell | `.venv\Scripts\python.exe scripts\export_pdf.py` |

Al terminar deben existir:

```text
book/_static/teachbook_es.pdf
book/_static/teachbook_en.pdf
```

La web enlaza estos PDFs desde las páginas de introducción de cada idioma.

## Publicación en GitHub Pages

El workflow de despliegue ejecuta siempre:

```bash
python scripts/setup_latex.py --ci-full
python scripts/export_pdf.py
python scripts/build_book.py
```

Así los PDFs quedan dentro de `book/_static/` antes de construir el HTML y se incluyen en el artefacto publicado.
El deploy NO usa `--allow-existing`: si no puede generar PDFs reales, falla. Esto protege al profesorado de publicar PDFs obsoletos.

## Personalización de plantillas LaTeX

Las plantillas están en `latex_templates/`:

```
latex_templates/
├── common/                    ← Estilos compartidos (jupyterBook.cls, etc.)
├── es/                        ← Ajustes para español (language_support.tex)
├── en/                        ← Ajustes para inglés
├── latexmkrc                  ← Configuración para latexmk
└── Makefile
```

- Los archivos de `common/` se aplican a TODOS los idiomas (capa base).
- Los archivos de `<lang>/` se aplican SOLO a ese idioma (capa de idioma, sobreescribe common).
- Los metadatos (título, autor, ISBN, editorial) se leen automáticamente de `_config_<lang>.yml` sección `latex:`.

## Solución de problemas

| Problema | Solución |
|---|---|
| "No se detectó un motor LaTeX" | Ejecutar `.venv\Scripts\python.exe scripts\setup_latex.py --yes` en Windows o `.venv/bin/python scripts/setup_latex.py --yes` en macOS/Linux |
| CI debe generar PDF real | Ejecutar `python scripts/setup_latex.py --ci-full` y después `python scripts/export_pdf.py` |
| `tectonic` funciona en `.venv\Scripts` pero no en `tectonic --version` | Es normal en Windows. Usa siempre los scripts del proyecto; ellos buscan Tectonic dentro de `.venv` |
| Error de PATH en Windows | No edites variables globales si no hace falta. Reinstala con el script oficial para que quede en `.venv\Scripts\tectonic.exe` |
| PowerShell bloquea scripts | No actives el venv con `.ps1`; usa la ruta completa `.venv\Scripts\python.exe ...` |
| `UnicodeEncodeError` / caracteres raros en Windows | Usa los scripts actualizados; fuerzan salida UTF-8 segura |
| Error con videos de YouTube | Usar el patrón dual `{raw} html` + `{raw} latex` (ver skill `teachbook-multimedia`) |
| Error con imágenes SVG | Los scripts convierten SVG a PNG con CairoSVG antes de compilar; no referencies SVG directamente desde LaTeX |
| Error `convert` / ImageMagick con SVG de Kroki | No uses ImageMagick para esto en CI: puede fallar con SVG complejos. El flujo oficial usa CairoSVG |
| Tectonic termina con `SIGSEGV` en CI | No usar Tectonic como motor principal: instalar toolchain completa con `setup_latex.py --ci-full` |
| GitHub API devuelve `rate limit exceeded` instalando Tectonic en Actions | Pasar `GITHUB_TOKEN: ${{ github.token }}` al paso `setup_latex.py --yes` |
| Fórmulas mal renderizadas | Verificar que `dollarmath` está en `myst_enable_extensions` del config |
| Error "Font not found" | Verificar conexión a internet: Tectonic descarga paquetes/fuentes bajo demanda. Si persiste, evitar fuentes del sistema y usar paquetes LaTeX estándar |
| Error con `fontspec` o fuentes del sistema | No dependas de fuentes instaladas en Windows. Usa las fuentes por defecto de Sphinx/Tectonic o paquetes incluidos en TeX |
| Error descargando paquetes/fuentes | Reintentar con conexión estable; redes corporativas/proxy pueden bloquear descargas de Tectonic |
| Error con Babel español | Revisar `latex_templates/es/language_support.tex` y `latex.preamble` de `_config_es.yml` |
| El PDF no tiene estilos personalizados | Verificar que `latex_templates/common/` contiene los archivos `.cls` y `.sty` |

## Reglas sobre fuentes LaTeX

- No uses fuentes instaladas en el sistema operativo (`Arial`, `Calibri`, etc.) en las plantillas.
- No añadas `fontspec` con nombres de fuentes del sistema salvo que controles Windows, macOS y Linux.
- Preferir fuentes y paquetes disponibles en TeX Live/MiKTeX.
- Si se necesita una fuente corporativa, incluirla como archivo del repo y documentar su licencia; si no, NO usarla.
- Los errores de fuentes suelen aparecer en Windows antes que en Linux: si falla en Windows, el diseño no es robusto.

## Flujo completo

```bash
# 1. Instalar LaTeX (solo la primera vez)
python scripts/setup_latex.py --yes

# 2. Exportar PDFs para todos los idiomas
python scripts/export_pdf.py
```

En Windows, sin activar el entorno:

```powershell
.venv\Scripts\python.exe scripts\setup_latex.py --yes
.venv\Scripts\python.exe scripts\export_pdf.py
```

En CI o para validación multi-OS real:

```bash
python scripts/setup_latex.py --ci-full
python scripts/export_pdf.py
```

Checklist final:

- [ ] `book/_static/teachbook_es.pdf` existe.
- [ ] `book/_static/teachbook_en.pdf` existe.
- [ ] La portada se ve correctamente.
- [ ] Las tildes y caracteres españoles se ven correctamente.
- [ ] Los enlaces de la página de introducción descargan los PDFs.
- [ ] El contenido HTML-only tiene alternativa textual para PDF.
