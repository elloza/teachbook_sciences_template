---
name: teachbook-export-pdf
description: >
  Exporta el libro completo a formato PDF para cada idioma configurado.
  Genera LaTeX intermedio, preprocesa SVG/rutas problemáticas y compila con Tectonic como flujo principal.
  Trigger phrases: "exportar PDF", "genera PDF", "PDF", "imprimible", "versión impresa",
  "quiero imprimir", "descargar PDF", "export pdf", "generate PDF".
---

# Skill: Exportar a PDF

## Cuándo usar esta skill

- Cuando se necesita una versión imprimible del libro.
- Para generar el archivo PDF descargable desde la web.
- Para validar que HTML y PDF siguen siendo compatibles.

## Flujo principal del proyecto

El flujo normal para usuario y agentes es:

```bash
python scripts/setup_latex.py --yes
python scripts/export_pdf.py
```

Eso instala **Tectonic** y lo usa como motor por defecto.

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

### Opción principal: Tectonic

- Es el default.
- Es la opción simple/portable.
- Debe resolverse cualquier problema concreto de SVG, Kroki, rutas o assets con preprocesado, NO cambiando el default.

Instalación/verificación:

```bash
python scripts/setup_latex.py --yes
python scripts/setup_latex.py --check
```

### Fallback avanzado explícito: latexmk + xelatex

Se mantiene solo para casos avanzados, diagnóstico o entornos concretos:

```bash
python scripts/setup_latex.py --ci-full
python scripts/export_pdf.py --engine latexmk
```

Verificación:

```bash
python scripts/setup_latex.py --check-full
```

## Instrucciones para el agente

### Paso 1: usar `.venv`

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/setup_latex.py --yes` |
| Windows PowerShell | `.venv\Scripts\python.exe scripts/setup_latex.py --yes` |

### Paso 2: exportar PDF

| Sistema | Comando |
|---|---|
| Linux / macOS | `.venv/bin/python scripts/export_pdf.py` |
| Windows PowerShell | `.venv\Scripts\python.exe scripts/export_pdf.py` |

### Paso 3: comprobar salida

Deben existir:

```text
book/_static/teachbook_es.pdf
book/_static/teachbook_en.pdf
```

## Workflows CI/CD

El deploy y los tests deben probar **Tectonic primero**:

```bash
python scripts/setup_latex.py --yes
python scripts/export_pdf.py
```

Si Tectonic falla en CI con un problema del motor, el workflow puede instalar el fallback avanzado y repetir con `--engine latexmk`. Eso mantiene Tectonic como flujo principal del usuario, pero evita que la publicación quede bloqueada por un fallo interno del binario de Tectonic en un runner concreto.

## Solución de problemas

| Problema | Solución |
|---|---|
| "No se detectó un motor LaTeX" | Ejecutar `scripts/setup_latex.py --yes` usando el Python de `.venv` |
| Error con SVG/Kroki | Convertir SVG a PNG antes de compilar; no dejar SVG crudo llegando a LaTeX |
| Error de rutas `_static` o `_images` | Replicar esas carpetas en rutas anidadas dentro del build LaTeX si Sphinx las serializa así |
| PowerShell bloquea scripts | No actives `.ps1`; usa `.venv\Scripts\python.exe ...` |
| Quiero forzar fallback avanzado | `python scripts/setup_latex.py --ci-full` y `python scripts/export_pdf.py --engine latexmk` |
| Tectonic falla en un entorno concreto | Corregir primero assets/rutas/preprocesado. Solo después usar `--engine latexmk` como diagnóstico o fallback explícito |

## Checklist final

- [ ] `book/_static/teachbook_es.pdf` existe.
- [ ] `book/_static/teachbook_en.pdf` existe.
- [ ] El flujo normal funciona con Tectonic.
- [ ] SVG/Kroki no llegan crudos a LaTeX.
- [ ] El fallback avanzado sigue siendo explícito, no default.
