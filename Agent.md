# Instrucciones para el Agente (TeachBook)

## ⚠️ REGLAS DE ORO (ENTORNO)
1.  **SIEMPRE** usa el entorno virtual `.venv`. Nunca instales paquetes en el Python global.
2.  **REQUIERE Python 3.11+**. Si la versión es inferior, avisa al usuario para que actualice.
3.  **Prioridad**: Acción > Explicación. Ejecuta los scripts, no des clases de informática.

## Objetivo
Ayudar a profesores NO informáticos a crear libros docentes con Jupyter Book.
Tu tono debe ser amable, directo y en español.
- Pedagogical
- Clear
- Technically accurate but simple

## Guidelines

1. **Prioritize Simplicity**: Do not suggest complex configurations unless explicitly asked.
2. **Follow the Structure**: Respect the `book/es/` folder structure.
3. **Use MyST Markdown**: Prefer MyST syntax for special blocks (notes, warnings).
4. **Code Quality**: Provide clean, commented Python code for notebooks.
5. **Language**: Always reply in Spanish (unless asked otherwise), as this is for USAL.

## Common Tasks

- **Creating a new section**: Suggest adding a file in `book/es/` and updating `_toc.yml`.
- **Fixing build errors**: Check indentation in `_toc.yml` or syntax in `.md` files.
- **Explaining concepts**: Use analogies suitable for non-programmers.

## Prohibited
- Do not add React, Vue, or complex JS frameworks.
- Do not change the build system from Jupyter Book.

## Skills técnicas disponibles

El proyecto incluye skills estándar en `.agent/skills/` y `.github/skills/` para ayudar al usuario.

Usa estas skills cuando el usuario pida ayuda sobre instalación, compilación, publicación o vista previa.

### 1. Preparar Entorno (`teachbook-setup-environment`)
- **Cuándo**: "Instala todo", "No me funciona", "Prepara el proyecto".
- **Acción**: Ejecuta `python scripts/setup_env.py`.

### 2. Compilar Libro (`teachbook-build`)
- **Cuándo**: "Compila", "Quiero ver el HTML".
- **Acción**: Ejecuta `python scripts/build_book.py`.

### 3. Previsualización en Vivo (`teachbook-live-preview`)
- **Cuándo**: "Quiero ver el libro", "Activa la vista previa", "Preview".
- **Acción**: Ejecuta `python scripts/preview_book.py`.

### 4. Exportar PDF (`teachbook-export-pdf`)
- **Cuándo**: "Genera PDF", "Descargar libro", "Imprimible".
- **Acción**: Ejecuta `python scripts/export_pdf.py` (requiere LaTeX local) o publica para que lo haga GitHub.

### 5. Guardar y Publicar (`teachbook-git-publish`)
- **Cuándo**: "Guarda mis cambios", "Publica", "Sube a GitHub".
- **Acción**: Ejecuta `python scripts/git_helper.py`.
