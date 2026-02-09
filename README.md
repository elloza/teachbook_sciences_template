# TeachBook Sciences Template 🎓

Plantilla para la creación de libros docentes interactivos en la **Facultad de Ciencias de la USAL**.

## 🚀 Inicio rápido

1. **Abrir en VS Code**: Asegúrate de tener la extensión de Python instalada.
2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Explorar**: Abre la carpeta `book/es/` para ver el contenido.
4. **Editar**: Modifica los archivos `.md` o `.ipynb`.
5. **Construir (opcional)**:
   ```bash
   jupyter-book build book/
   ```

## 📂 Estructura

- `book/es/`: Contiene todo el texto y código del libro.
- `book/_toc.yml`: Define el índice (tabla de contenidos).
- `book/_config.yml`: Configuración del libro.

## 📚 Documentación

Lee los tutoriales incluidos en `book/es/01_tutorial/` para aprender más.

### 📄 Exportar a PDF
El template incluye generación automática de PDF.
- **En la nube**: GitHub Actions generará el PDF automáticamente cada vez que subas cambios, y aparecerá un botón de "Descargar PDF" en la web.
- **En local**: Si tienes LaTeX instalado, puedes ejecutar `python scripts/export_pdf.py` (o usar la Skill "Exportar PDF").

## 🤝 Contribuir
