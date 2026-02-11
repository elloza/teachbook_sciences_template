---
name: teachbook-export-pdf
description: Exporta el libro completo a formato PDF (requiere LaTeX local o uso de GitHub Actions).
---

# Skill: Exportar PDF 📄

Genera un archivo PDF imprimible de todo el contenido del libro.

## ¿Qué hace?
- Convierte el libro a formato LaTeX.
- Compila el LaTeX a PDF.
- Copia el resultado a `book/_static/teachbook.pdf`.

## ¿Cuándo usarla?
- Cuando quieras una versión para imprimir o leer offline.
- Para generar el archivo final que se descargará desde la web.

## Cómo pedirla al Agente
> "Genera el PDF."
> "Quiero una versión imprimible."
> "Exporta a PDF."

## Requisitos
- **En la nube**: No necesitas nada; GitHub Actions lo genera automáticamente.
- **En local**: Si no tienes LaTeX, el script te ofrecerá instalar **Tectonic** (un motor ligero y automático) automáticamente.

## Personalización y Estilo (LaTeX) 🎨

El proyecto utiliza una clase LaTeX personalizada llamada `jupyterBook.cls` ubicada en `latex_templates/common/`.

### Modificar la Portada y Estilo Común
Para cambiar colores, el diseño de la portada (usando TikZ), o añadir comandos matemáticos globales:
1. Edita `latex_templates/common/jupyterBook.cls`.
2. Los colores corporativos de la USAL (**Rojo Vítor**) están definidos allí como `usalRed`.

### Ajustes por Idioma (Traducciones)
Si necesitas traducir términos específicos del PDF (ej: "Chapter" a "Capítulo") o añadir paquetes que solo afecten a un idioma:
1. Edita el archivo `language_support.tex` en la carpeta del idioma correspondiente:
   - `latex_templates/es/language_support.tex` (Español)
   - `latex_templates/en/language_support.tex` (Inglés)
2. El script `export_pdf.py` copia automáticamente estos archivos al directorio de compilación antes de generar el PDF.

### Metadatos (ISBN, DOI, Editorial)
Estos campos se extraen de la sección `latex` en `_config_es.yml` o `_config_en.yml`. El script genera un archivo `bookmetadata.tex` al vuelo que la clase LaTeX lee para rellenar la banda inferior de la portada.

## Acción Técnica
El agente ejecutará:
```bash
python scripts/export_pdf.py
```
- Si detecta que faltan herramientas, te sugerirá ejecutar `python scripts/setup_latex.py`.
