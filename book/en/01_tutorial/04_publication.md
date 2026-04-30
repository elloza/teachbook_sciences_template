# 4. Web Publication

Publication is done automatically through **GitHub Pages**.

## Steps to publish

1. Ensure your repository is public (or you have access to GitHub Pages in private).
2. Make changes to your content.
3. Save changes with a **Commit** and **Push** to the main branch (`main`).
4. A "GitHub Action" will run automatically and build your book.
5. The same action also generates a **new PDF for each language** before publishing, so the download buttons point to the latest printable version.
6. In a few minutes, you will see your updated book at your repository URL (configured in Settings > Pages).

## What exactly is deployed?

Each push to `main` runs `.github/workflows/deploy.yml`. That workflow always follows this order:

1. Prepare the TeachBook environment with `scripts/setup_env.py`.
2. Install the full local/CI PDF toolchain with `scripts/setup_latex.py --yes --full`.
3. Generate fresh PDFs with `scripts/export_pdf.py --engine auto`.
4. Build the HTML site with `scripts/build_book.py`.
5. Upload `book/_build/html/` to GitHub Pages.

Do not publish by uploading only HTML manually: that would leave stale PDF files. The supported publishing path is **commit + push to `main`**, letting GitHub Actions regenerate both HTML and PDFs.
