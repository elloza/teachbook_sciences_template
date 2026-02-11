# TeachBook Sciences Template 🎓

Plantilla para la creación de libros docentes interactivos en la **Facultad de Ciencias de la USAL**.

## 🛠️ Prerrequisitos

Para trabajar con este template necesitas instalar:
1.  **Python 3.8 o superior**: [Descargar aquí](https://www.python.org/downloads/).
    - *Nota*: Asegúrate de marcar "Add Python to PATH" durante la instalación.
2.  **Visual Studio Code**: [Descargar aquí](https://code.visualstudio.com/).
    - Se recomienda instalar las extensiones:
        - **Python** (de Microsoft).
        - **GitHub Copilot** (opcional, para usar el asistente de IA).
3.  **Git**: [Descargar aquí](https://git-scm.com/) (necesario solo si vas a publicar en GitHub).

## 🚀 Inicio rápido

Hemos incluido un script que prepara todo automáticamente:

1.  **Abrir en VS Code**: Abre la carpeta del proyecto.
2.  **Preparar entorno**:
    ```bash
    python scripts/setup_env.py
    ```
    Esto creará un entorno virtual (`.venv`) e instalará todas las librerías necesarias.
3.  **Activar entorno**:
    - En Windows: `.\.venv\Scripts\activate`
    - En Mac/Linux: `source .venv/bin/activate`
    *(VS Code suele detectarlo automáticamente y preguntarte si quieres usarlo).*

4.  **Explorar**: Abre la carpeta `book/es/` para ver el contenido.
5.  **Editar**: Modifica los archivos `.md` o `.ipynb`.
6.  **Previsualizar**:
    ```bash
    python scripts/preview_book.py
    ```
    Esto abrirá un navegador con la web y recargará automáticamente al guardar cambios.

## 📂 Estructura

- `book/es/`: Contiene todo el texto y código del libro.
- `book/_toc.yml`: Define el índice (tabla de contenidos).
- `book/_config.yml`: Configuración del libro.

## 🌍 Soporte Multi-idioma

El proyecto está configurado para generar versiones en **Español (es)** e **Inglés (en)**.
- **Contenido**:
  - `book/es/`: Contenido en español.
  - `book/en/`: Contenido en inglés.
- **Configuración**:
  - `_config_es.yml` / `_toc_es.yml`: Configuración para español.
  - `_config_en.yml` / `_toc_en.yml`: Configuración para inglés.
- **Traducción**: El script de construcción genera un selector de idioma automáticamente en la web.

## 📚 Documentación y Scripts

Lee los tutoriales incluidos en `book/es/01_tutorial/` para aprender más.

### 📄 Exportar a PDF
El template incluye generación automática de PDF para cada idioma.

- **En la nube (GitHub Actions)**: Los PDFs **no se generan en cada push** (para ahorrar tiempo de CI). Para regenerarlos, tienes dos opciones:
  1. **Incluir `[pdf]` en el mensaje del commit**:
     ```bash
     git commit -m "Actualizar contenido [pdf]"
     ```
     Esto activará los pasos de instalación de LaTeX y generación de PDF en el workflow.
  2. **Lanzar el workflow manualmente** desde la pestaña _Actions_ del repositorio en GitHub, marcando la opción _Build PDF_.

- **En local** (requiere LaTeX instalado):
  ```bash
  python scripts/export_pdf.py
  ```
  Esto generará `book/_static/teachbook_es.pdf` y `book/_static/teachbook_en.pdf`.

### 🎨 Personalización de PDF
Puedes personalizar la apariencia del PDF (portadas, estilos) editando los archivos en `latex_templates/`:
- `latex_templates/common/`: Archivos comunes (ej: macros matemáticas).
- `latex_templates/es/`: Archivos específicos para español.
- `latex_templates/en/`: Archivos específicos para inglés.

## 🤝 Contribuir
