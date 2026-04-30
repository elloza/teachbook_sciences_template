# 4. Publicación Web

La publicación se realiza de forma automática a través de **GitHub Pages**.

## Pasos para publicar
1. Asegúrate de que tu repositorio es público (o tienes acceso a GitHub Pages en privado).
2. Haz cambios en tu contenido.
3. Guarda los cambios un **Commit** y haz **Push** a la rama principal (`main`).
4. Una "Acción de GitHub" se ejecutará automáticamente y construirá tu libro.
5. Esa misma acción genera también un **PDF nuevo para cada idioma** antes de publicar, de modo que los botones de descarga apuntan a la versión imprimible más reciente.
6. En unos minutos, verás tu libro actualizado en la URL de tu repositorio (configurada en Settings > Pages).

## ¿Qué se despliega exactamente?

Cada `push` a `main` ejecuta `.github/workflows/deploy.yml`. Ese workflow siempre sigue este orden:

1. Prepara el entorno TeachBook con `scripts/setup_env.py`.
2. Instala la cadena completa local/CI para PDF con `scripts/setup_latex.py --yes --full`.
3. Genera PDFs nuevos con `scripts/export_pdf.py --engine auto`.
4. Compila la web HTML con `scripts/build_book.py`.
5. Sube `book/_build/html/` a GitHub Pages.

No publiques subiendo solo el HTML manualmente: eso puede dejar PDFs antiguos. La ruta soportada de publicación es **commit + push a `main`**, dejando que GitHub Actions regenere tanto HTML como PDFs.
