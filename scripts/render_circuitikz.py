import io
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


# Fix: Windows cp1252 can't encode emojis — force UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "book" / "_static" / "generated"


def fail(message: str, code: int = 1):
    print(f"❌ {message}")
    sys.exit(code)


def ensure_tectonic():
    if shutil.which("tectonic") is None:
        fail(
            "No se encontró Tectonic. Instálalo con: python scripts/setup_latex.py"
        )


def ensure_pymupdf():
    try:
        import fitz  # noqa: F401
    except ImportError:
        fail(
            "Falta PyMuPDF para convertir PDF a PNG. Instálalo con: python -m pip install PyMuPDF"
        )


def build_full_document(content: str) -> str:
    stripped = content.strip()

    if "\\documentclass" in stripped:
        return content

    if "\\begin{circuitikz}" not in stripped:
        stripped = (
            "\\begin{circuitikz}\n"
            + stripped
            + "\n\\end{circuitikz}"
        )

    return rf"""
\documentclass[tikz,border=6pt]{{standalone}}
\usepackage{{circuitikz}}
\begin{{document}}
{stripped}
\end{{document}}
""".strip() + "\n"


def render_pdf(tex_file: Path, workdir: Path):
    result = subprocess.run(
        [
            "tectonic",
            str(tex_file.name),
            "--outdir",
            str(workdir),
        ],
        cwd=workdir,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        fail("Tectonic no pudo compilar el archivo CircuitikZ.")


def pdf_to_png(pdf_path: Path, png_path: Path):
    import fitz

    png_path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), alpha=False)
    pix.save(str(png_path))
    doc.close()


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Uso:")
        print("  python scripts/render_circuitikz.py <entrada.tex> [salida.png]")
        print()
        print("Ejemplo:")
        print(
            "  python scripts/render_circuitikz.py assets/circuito_rc.tex book/_static/generated/circuito_rc.png"
        )
        sys.exit(1)

    input_path = Path(sys.argv[1]).resolve()
    if not input_path.is_file():
        fail(f"No existe el archivo de entrada: {input_path}")

    if len(sys.argv) == 3:
        output_path = Path(sys.argv[2]).resolve()
    else:
        output_path = (DEFAULT_OUTPUT_DIR / f"{input_path.stem}.png").resolve()

    ensure_tectonic()
    ensure_pymupdf()

    print(f"📄 Leyendo fuente CircuitikZ: {input_path}")
    content = input_path.read_text(encoding="utf-8")
    full_doc = build_full_document(content)

    with tempfile.TemporaryDirectory(prefix="circuitikz_") as tmp:
        tmpdir = Path(tmp)
        tex_file = tmpdir / "diagram.tex"
        pdf_file = tmpdir / "diagram.pdf"

        tex_file.write_text(full_doc, encoding="utf-8")
        print("🧮 Compilando con Tectonic...")
        render_pdf(tex_file, tmpdir)

        if not pdf_file.is_file():
            fail("No se generó el PDF esperado.")

        print("🖼️ Convirtiendo PDF a PNG...")
        pdf_to_png(pdf_file, output_path)

    print(f"✅ Imagen generada correctamente en: {output_path}")
    print()
    print("Ahora puedes insertarla en MyST así:")
    relative = output_path.relative_to(PROJECT_ROOT / "book") if str(output_path).startswith(str(PROJECT_ROOT / "book")) else output_path
    print("```md")
    print(f"```{{figure}} {relative.as_posix()}")
    print(":alt: Circuito generado con CircuitikZ")
    print(":width: 70%")
    print(":align: center")
    print()
    print("Circuito generado con CircuitikZ.")
    print("```")
    print("```")


if __name__ == "__main__":
    main()
