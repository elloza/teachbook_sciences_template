---
name: teachbook-export-pdf
description: >
  Exporta el libro completo a formato PDF para cada idioma configurado.
  Genera LaTeX intermedio, preprocesa SVG/rutas problemáticas y compila con la misma política local/CI.
  Trigger phrases: "exportar PDF", "genera PDF", "PDF", "imprimible", "versión impresa",
  "quiero imprimir", "descargar PDF", "export pdf", "generate PDF".
---

# Skill: Exportar a PDF

## Cuándo usar esta skill

- Cuando se necesita una versión imprimible del libro.
- Para generar el archivo PDF descargable desde la web.
- Para validar que HTML y PDF siguen siendo compatibles.

## Flujo principal del proyecto

El flujo recomendado para que el alumno vea localmente lo mismo que publicará CI/CD es:

```bash
python scripts/setup_latex.py --yes --full
python scripts/export_pdf.py --engine auto
```

Eso instala **Tectonic** y también prepara el fallback avanzado (`latexmk` + XeLaTeX) cuando el sistema lo permite. La exportación con `--engine auto` prueba Tectonic primero y, si el motor falla, usa el fallback. Es la misma política que deben usar deploy y tests.

## Qué hace `export_pdf.py`

1. Verifica que el motor solicitado exista.
2. Detecta idiomas desde `_config_<lang>.yml`.
3. Genera LaTeX por idioma con Jupyter Book.
4. Aplica plantillas personalizadas.
5. Convierte SVG a PNG antes de compilar cuando hace falta.
6. Replica rutas compartidas como `_static/` y `_images/` si LaTeX las referencia desde rutas anidadas.
7. Copia los PDFs finales a `book/_static/`.

## Ubicación de salida

```text
book/_static/teachbook_es.pdf
book/_static/teachbook_en.pdf
```

## Motores soportados

### Opción principal ligera: Tectonic

- Es el default.
- Es la opción simple/portable.
- Debe resolverse cualquier problema concreto de SVG, Kroki, rutas o assets con preprocesado, NO cambiando el default.

Instalación/verificación:

```bash
python scripts/setup_latex.py --yes
python scripts/setup_latex.py --check
```

### Toolchain completa local/CI: Tectonic + latexmk/xelatex

Usar cuando se quiera paridad con CI/CD o generación robusta de PDFs:

```bash
python scripts/setup_latex.py --yes --full
python scripts/export_pdf.py --engine auto
```

Verificación:

```bash
python scripts/setup_latex.py --check-full
```

## Instrucciones para el agente

### Paso 1: usar `.venv`

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/setup_latex.py --yes --full` |
| Windows PowerShell | `.venv\Scripts\python.exe scripts/setup_latex.py --yes --full` |

### Paso 2: exportar PDF

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/export_pdf.py --engine auto` |
| Windows PowerShell | `.venv\Scripts\python.exe scripts/export_pdf.py --engine auto` |

### Paso 3: comprobar salida

Deben existir:

```text
book/_static/teachbook_es.pdf
book/_static/teachbook_en.pdf
```

## Workflows CI/CD

El deploy y los tests deben usar la misma política que el alumno:

```bash
.venv/bin/python scripts/setup_latex.py --yes --full
.venv/bin/python scripts/export_pdf.py --engine auto
```

Si Tectonic falla en CI con un problema del motor, `--engine auto` debe caer al fallback ya instalado. Así no se publica con un camino distinto al que puede reproducir el alumno localmente.

## Solución de problemas

| Problema | Solución |
|---|---|
| "No se detectó un motor LaTeX" | Ejecutar `scripts/setup_latex.py --yes --full` usando el Python de `.venv` |
| Error con SVG/Kroki | Convertir SVG a PNG antes de compilar; no dejar SVG crudo llegando a LaTeX |
| Error de rutas `_static` o `_images` | Replicar esas carpetas en rutas anidadas dentro del build LaTeX si Sphinx las serializa así |
| PowerShell bloquea scripts | No actives `.ps1`; usa `.venv\Scripts\python.exe ...` |
| Quiero forzar fallback avanzado | `python scripts/setup_latex.py --ci-full` y `python scripts/export_pdf.py --engine latexmk` |
| Tectonic falla en un entorno concreto | Corregir primero assets/rutas/preprocesado. Solo después usar `--engine latexmk` como diagnóstico o fallback explícito |

## Checklist final

- [ ] `book/_static/teachbook_es.pdf` existe.
- [ ] `book/_static/teachbook_en.pdf` existe.
- [ ] El flujo local/CI usa `setup_latex.py --yes --full` + `export_pdf.py --engine auto`.
- [ ] SVG/Kroki no llegan crudos a LaTeX.
- [ ] El fallback avanzado sigue siendo explícito, no default.
