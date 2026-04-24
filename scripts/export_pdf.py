import io
import subprocess
import os
import shutil
import sys
import glob
import yaml

# Fix: Windows cp1252 can't encode emojis — force UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def get_jupyter_book():
    """Returns the path to jupyter-book executable in the virtual environment."""
    if os.name == "nt":
        return os.path.join(".venv", "Scripts", "jupyter-book.exe")
    return os.path.join(".venv", "bin", "jupyter-book")


# Configuration
BOOK_DIR = "book"
STATIC_DIR = os.path.join(BOOK_DIR, "_static")


def get_languages():
    """Detects languages based on _config_<lang>.yml files."""
    configs = glob.glob(os.path.join(BOOK_DIR, "_config_*.yml"))
    languages = []

    for conf in configs:
        filename = os.path.basename(conf)
        lang_code = filename.replace("_config_", "").replace(".yml", "")
        languages.append(lang_code)

    if not languages and os.path.exists(os.path.join(BOOK_DIR, "_config.yml")):
        return ["default"]  # Single language mode

    return sorted(languages)


# Determine script directory once, before any chdir
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def check_latex_installed():
    """Checks if tectonic, latexmk or pdflatex is available."""
    local_tectonic = os.path.join(
        SCRIPT_DIR, "tectonic.exe" if os.name == "nt" else "tectonic"
    )

    if os.path.exists(local_tectonic):
        return local_tectonic

    return (
        shutil.which("tectonic") or shutil.which("latexmk") or shutil.which("pdflatex")
    )


def ensure_static_dir():
    """Ensures the static directory exists."""
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)


def glob_pdf(search_dir):
    for file in os.listdir(search_dir):
        if file.endswith(".pdf"):
            return os.path.abspath(os.path.join(search_dir, file))
    return None


def generate_metadata_tex(lang, latex_build_dir):
    """Reads metadata from the language YAML config and generates bookmetadata.tex."""
    if lang == "default":
        config_path = os.path.join(BOOK_DIR, "_config.yml")
    else:
        config_path = os.path.join(BOOK_DIR, f"_config_{lang}.yml")

    if not os.path.exists(config_path):
        print(f"⚠️ No config found at {config_path}, skipping metadata.")
        return

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # Extract optional metadata from the latex section or top-level
    latex_config = config.get("latex", {})

    metadata = {
        "BookISBN": latex_config.get("isbn", ""),
        "BookDOI": latex_config.get("doi", ""),
        "BookEdition": latex_config.get("edition", ""),
        "BookPublisher": latex_config.get("publisher", ""),
        "BookYear": str(config.get("copyright", "")),
        "BookSubtitle": latex_config.get("subtitle", ""),
        "BookInstitution": latex_config.get("institution", ""),
    }

    # Check for cover image (USAL logo)
    logo_src = os.path.join(BOOK_DIR, "_static", "usal_logo.png")
    if os.path.exists(logo_src):
        logo_dest = os.path.join(latex_build_dir, "usal_logo.png")
        shutil.copy2(logo_src, logo_dest)
        metadata["BookCoverImage"] = "usal_logo.png"
        print(f"   📷 Logo USAL copiado a build dir.")

    # Write bookmetadata.tex
    tex_path = os.path.join(latex_build_dir, "bookmetadata.tex")
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write("% Auto-generated metadata - do not edit manually\n")
        for cmd, value in metadata.items():
            if value:  # Only write non-empty values
                # Escape LaTeX special characters
                safe_value = (
                    str(value)
                    .replace("&", "\\&")
                    .replace("#", "\\#")
                    .replace("%", "\\%")
                )
                f.write(f"\\renewcommand{{\\{cmd}}}{{{safe_value}}}\n")

    print(f"   📝 Metadata TeX generado: {tex_path}")


def build_pdf_for_lang(lang):
    """Builds the PDF for a specific language using a standalone temporary project."""
    print(f"\n🚀 Iniciando generación de PDF STANDALONE para: {lang.upper()}...")

    if lang == "default":
        config_file = "_config.yml"
        toc_file = "_toc.yml"
        pdf_filename = "teachbook.pdf"
        src_dir = os.path.abspath(BOOK_DIR)
        temp_mode = False
    else:
        config_file = f"_config_{lang}.yml"
        toc_file = f"_toc_{lang}.yml"
        pdf_filename = f"teachbook_{lang}.pdf"
        temp_mode = True

    if temp_mode:
        # Use _temp_pdf_{lang} at ROOT to avoid recursion/exclusion issues
        temp_root = os.path.abspath(os.path.join(os.getcwd(), f"_temp_pdf_{lang}"))
        if os.path.exists(temp_root):
            shutil.rmtree(temp_root)
        os.makedirs(temp_root)

        lang_src = os.path.join(BOOK_DIR, lang)
        lang_dst = os.path.join(temp_root, lang)
        print(f"📂 Preparando entorno standalone PDF: {temp_root}")
        shutil.copytree(lang_src, lang_dst)

        static_src = os.path.join(BOOK_DIR, "_static")
        if os.path.exists(static_src):
            shutil.copytree(static_src, os.path.join(temp_root, "_static"))

        dest_config = os.path.join(temp_root, "_config.yml")
        shutil.copy2(os.path.join(BOOK_DIR, config_file), dest_config)
        shutil.copy2(
            os.path.join(BOOK_DIR, toc_file), os.path.join(temp_root, "_toc.yml")
        )

        # Sanitize config to prevent self-exclusion
        sanitize_config(dest_config)
        src_dir = temp_root
    else:
        src_dir = os.path.abspath(BOOK_DIR)

    build_dir = os.path.join(src_dir, "_build")
    latex_build_dir = os.path.join(build_dir, "latex")
    dest_pdf_path = os.path.join(STATIC_DIR, pdf_filename)

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    print("📝 Generando archivos LaTeX con Jupyter Book...", flush=True)
    try:
        cmd = [get_jupyter_book(), "build", "--builder", "latex", src_dir, "--all"]
        subprocess.run(cmd, shell=(os.name == "nt"), check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en jupyter-book build ({lang}): {e}")
        return False

    print("🎨 Aplicando plantillas LaTeX personalizadas...", flush=True)
    templates_root = os.path.abspath("latex_templates")

    # 0. Generate metadata tex file from YAML config
    generate_metadata_tex(lang, latex_build_dir)

    # 1. Apply COMMON templates (base)
    common_dir = os.path.join(templates_root, "common")
    if os.path.exists(common_dir) and os.path.exists(latex_build_dir):
        print("   🔹 Aplicando plantillas comunes (latex_templates/common)...")
        for item in os.listdir(common_dir):
            s = os.path.join(common_dir, item)
            d = os.path.join(latex_build_dir, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)

    # 2. Apply LANGUAGE-SPECIFIC templates (overlay)
    lang_dir = os.path.join(templates_root, lang)
    if os.path.exists(lang_dir) and os.path.exists(latex_build_dir):
        print(f"   🔹 Aplicando plantillas para '{lang}' (latex_templates/{lang})...")
        for item in os.listdir(lang_dir):
            s = os.path.join(lang_dir, item)
            d = os.path.join(latex_build_dir, item)
            if os.path.isfile(s):
                shutil.copy2(s, d)

    print(f"📂 Compilando con Tectonic en {latex_build_dir}...")
    current_dir = os.getcwd()
    try:
        os.chdir(latex_build_dir)
        tex_files = [
            f
            for f in glob.glob("*.tex")
            if f not in ["bookmetadata.tex", "language_support.tex"]
        ]
        if not tex_files:
            print("❌ No se encontró archivo .tex compatible.")
            return False

        # Prioritize python.tex or the first file available
        main_tex = "python.tex" if "python.tex" in tex_files else tex_files[0]

        tex_engine_path = check_latex_installed()
        if not tex_engine_path:
            print("❌ No hay motor LaTeX.")
            return False

        print(f"🔧 Usando motor: {tex_engine_path}")

        # Determine commands based on engine
        engine_name = os.path.basename(tex_engine_path).lower()
        if "tectonic" in engine_name:
            cmd = [tex_engine_path, "-X", "compile", main_tex]
        elif "latexmk" in engine_name:
            # Use xelatex as per project config
            cmd = [
                tex_engine_path,
                "-xelatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                main_tex,
            ]
        else:
            # Fallback to pdflatex
            cmd = [
                tex_engine_path,
                "-interaction=nonstopmode",
                "-halt-on-error",
                main_tex,
            ]

        print(f"🚀 Ejecutando: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)

        found_pdf = glob_pdf(".")
        if found_pdf:
            os.chdir(current_dir)
            ensure_static_dir()
            shutil.copy(found_pdf, dest_pdf_path)
            print(f"🎉 PDF de '{lang}' exportado a: {dest_pdf_path}")
            return True
        else:
            print("❌ No se generó el PDF final.")
            return False
    except Exception as e:
        print(f"❌ Error compilando {lang}: {e}")
        # print(f"DEBUG: log log log...")
        return False
    finally:
        os.chdir(current_dir)
        if temp_mode and os.path.exists(src_dir):
            shutil.rmtree(src_dir)


def sanitize_config(config_path):
    """
    Removes exclusion patterns entirely to prevent EISDIR errors in temp environment.
    """
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        new_lines = []
        exclude_written = False
        for line in lines:
            if "exclude_patterns:" in line:
                # Force a safe, minimal exclusion list
                new_lines.append(
                    'exclude_patterns: ["_build", "**.ipynb_checkpoints", ".git", ".github"]\n'
                )
                exclude_written = True
                continue
            new_lines.append(line)

        if not exclude_written:
            new_lines.append(
                'exclude_patterns: ["_build", "**.ipynb_checkpoints", ".git", ".github"]\n'
            )

        with open(config_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"🔧 Configuración saneada (excludes minimos seguros) en: {config_path}")
    except Exception as e:
        print(f"⚠️ Error saneando configuración: {e}")


def main():
    print("📚 Iniciando exportación de PDF multi-idioma...")
    if not check_latex_installed():
        print("⚠️  No se detectó un motor LaTeX.")
        print("   Puedes instalarlo automáticamente ejecutando:")
        print("   python scripts/setup_latex.py")
        sys.exit(1)

    languages = get_languages()
    print(f"🔍 Idiomas detectados para PDF: {languages}")

    success_count: int = 0
    for lang in languages:
        if build_pdf_for_lang(lang):
            success_count = success_count + 1  # type: ignore

    if success_count == len(languages):
        print(f"\n✅ Todos los PDFs ({success_count}) se generaron correctamente.")
        sys.exit(0)
    else:
        print(f"\n⚠️ Se generaron {success_count} de {len(languages)} PDFs.")
        sys.exit(1)


if __name__ == "__main__":
    main()
