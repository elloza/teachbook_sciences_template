import io
import subprocess
import os
import shutil
import sys
import glob
import yaml
import re


# Determine script/project directories once, before any chdir.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Fix: Windows cp1252 can't encode emojis — force UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def get_jupyter_book():
    """Returns the path to jupyter-book executable. Prefers venv, falls back to system."""
    if os.name == "nt":
        venv_jb = os.path.join(PROJECT_ROOT, ".venv", "Scripts", "jupyter-book.exe")
    else:
        venv_jb = os.path.join(PROJECT_ROOT, ".venv", "bin", "jupyter-book")
    if os.path.isfile(venv_jb):
        return venv_jb
    return shutil.which("jupyter-book")


# Configuration
BOOK_DIR = "book"
STATIC_DIR = os.path.join(BOOK_DIR, "_static")
SUPPORTED_ENGINES = ("tectonic", "latexmk", "auto")


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


def find_tectonic_command():
    """Return a usable Tectonic executable if available."""
    executable_name = "tectonic.exe" if os.name == "nt" else "tectonic"

    candidates = []
    if os.name == "nt":
        candidates.extend(
            [
                os.path.join(PROJECT_ROOT, ".venv", "Scripts", executable_name),
                os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "teachbook", executable_name),
            ]
        )
    else:
        candidates.extend(
            [
                os.path.join(PROJECT_ROOT, ".venv", "bin", executable_name),
                os.path.expanduser(os.path.join("~", ".local", "bin", executable_name)),
            ]
        )

    candidates.append(os.path.join(SCRIPT_DIR, executable_name))

    for candidate in candidates:
        if os.path.exists(candidate):
            return os.path.abspath(candidate)

    return shutil.which("tectonic")


def find_latexmk_command():
    """Return latexmk only when its XeLaTeX dependency is available."""
    latexmk = find_command_with_common_latex_paths("latexmk")
    xelatex = find_command_with_common_latex_paths("xelatex")
    if latexmk and xelatex:
        return latexmk
    return None


def find_command_with_common_latex_paths(command_name):
    """Find LaTeX tools even before CI PATH updates take effect."""
    found = shutil.which(command_name)
    if found:
        return found

    executable = f"{command_name}.exe" if os.name == "nt" else command_name
    candidates = []
    if os.name == "nt":
        candidates.extend(
            [
                os.path.join("C:\\Program Files\\MiKTeX\\miktex\\bin\\x64", executable),
                os.path.join("C:\\Program Files\\MiKTeX\\miktex\\bin", executable),
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "MiKTeX", "miktex", "bin", "x64", executable),
            ]
        )
    else:
        candidates.extend(
            [
                os.path.join("/Library/TeX/texbin", executable),
                os.path.join("/usr/local/texlive/2026basic/bin/universal-darwin", executable),
                os.path.join("/usr/local/texlive/2025basic/bin/universal-darwin", executable),
                os.path.join("/usr/local/texlive/2024basic/bin/universal-darwin", executable),
                os.path.join("/usr/bin", executable),
                os.path.join("/usr/local/bin", executable),
            ]
        )

    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return candidate
    return None


def resolve_latex_engine(engine_name):
    """Resolve the requested LaTeX engine path.

    Default user flow is Tectonic. `latexmk` remains available as explicit
    advanced fallback. `auto` preserves a diagnostics-oriented fallback mode.
    """
    if engine_name == "tectonic":
        return find_tectonic_command()
    if engine_name == "latexmk":
        return find_latexmk_command()
    if engine_name == "auto":
        return (
            find_tectonic_command()
            or find_latexmk_command()
            or shutil.which("pdflatex")
        )
    return None


def resolve_latex_engine_candidates(engine_name):
    """Return ordered engine candidates.

    `auto` is the CI/CD and full local mode: try Tectonic first because it is the
    lightweight project default, then fall back to latexmk/XeLaTeX if Tectonic
    crashes or cannot compile the generated LaTeX on a platform.
    """
    if engine_name == "auto":
        candidates = []
        for name, path in (
            ("tectonic", find_tectonic_command()),
            ("latexmk", find_latexmk_command()),
            ("pdflatex", shutil.which("pdflatex")),
        ):
            if path:
                candidates.append((name, path))
        return candidates

    resolved = resolve_latex_engine(engine_name)
    if not resolved:
        return []
    return [(engine_name, resolved)]


def latex_env(tex_engine_path):
    """Return an environment that can find a project-local LaTeX engine."""
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    engine_dir = os.path.dirname(os.path.abspath(tex_engine_path))
    env["PATH"] = engine_dir + os.pathsep + env.get("PATH", "")
    return env


def compile_latex_with_engine(tex_engine_path, main_tex):
    """Compile a LaTeX file with one concrete engine path."""
    print(f"🔧 Usando motor: {tex_engine_path}")
    env = latex_env(tex_engine_path)

    engine_basename = os.path.basename(tex_engine_path).lower()
    if "tectonic" in engine_basename:
        commands = [
            [tex_engine_path, "--keep-logs", "--keep-intermediates", main_tex],
            [tex_engine_path, "-X", "compile", main_tex],
        ]
    elif "latexmk" in engine_basename:
        commands = [
            [
                tex_engine_path,
                "-xelatex",
                "-interaction=nonstopmode",
                "-halt-on-error",
                main_tex,
            ]
        ]
    else:
        commands = [
            [
                tex_engine_path,
                "-interaction=nonstopmode",
                "-halt-on-error",
                main_tex,
            ]
        ]

    last_error = None
    for attempt, cmd in enumerate(commands, start=1):
        try:
            print(f"🚀 Ejecutando ({attempt}/{len(commands)}): {' '.join(cmd)}")
            subprocess.run(cmd, check=True, env=env)
            return True
        except subprocess.CalledProcessError as exc:
            last_error = exc
            print(f"⚠️  Falló el intento {attempt}: {exc}")
            if exc.returncode < 0:
                print(
                    "   El motor LaTeX terminó por señal del sistema "
                    f"({-exc.returncode}). Se probará el siguiente modo si existe."
                )

    if last_error is not None:
        raise last_error
    return False


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


def prepare_svg_images_for_latex(latex_build_dir):
    """Convert SVG images in the LaTeX build to PNG and rewrite TeX refs.

    Sphinx's default converter uses ImageMagick `convert`, which fails on some
    Kroki/Mermaid SVGs (`stroke-dasharray`).  XeLaTeX also cannot infer SVG
    bounding boxes directly.  CairoSVG handles these diagrams reliably enough
    for static PDF output and keeps the workflow cross-platform.
    """
    svg_paths = glob.glob(os.path.join(latex_build_dir, "**", "*.svg"), recursive=True)
    if not svg_paths:
        return True

    resvg = shutil.which("resvg")
    if not resvg:
        resvg_name = "resvg.exe" if os.name == "nt" else "resvg"
        resvg_candidates = [
            os.path.join(PROJECT_ROOT, ".venv", "Scripts", resvg_name),
            os.path.join(PROJECT_ROOT, ".venv", "bin", resvg_name),
            os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "teachbook", resvg_name),
            os.path.expanduser(os.path.join("~", ".local", "bin", resvg_name)),
            os.path.join(SCRIPT_DIR, resvg_name),
        ]
        for candidate in resvg_candidates:
            if os.path.isfile(candidate):
                resvg = candidate
                break

    rsvg_convert = shutil.which("rsvg-convert")
    cairosvg = None
    if not resvg and not rsvg_convert:
        try:
            import cairosvg as cairosvg_module

            cairosvg = cairosvg_module
        except Exception as exc:
            print("❌ Hay SVGs en el build LaTeX, pero no hay conversor SVG robusto.")
            print("   Instala resvg con scripts/setup_latex.py --yes, o usa rsvg-convert/CairoSVG.")
            print(f"   Detalle CairoSVG: {exc}")
            return False

    print(f"🖼️  Convirtiendo {len(svg_paths)} SVG(s) a PNG para LaTeX...")
    replacements = {}
    for svg_path in svg_paths:
        png_path = os.path.splitext(svg_path)[0] + ".png"
        try:
            if resvg:
                subprocess.run(
                    [resvg, svg_path, png_path],
                    check=True,
                )
            elif rsvg_convert:
                subprocess.run(
                    [rsvg_convert, "--width", "1600", "--output", png_path, svg_path],
                    check=True,
                )
            else:
                cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=1600)
        except Exception as exc:
            print(f"❌ No se pudo convertir {svg_path}: {exc}")
            return False
        svg_rel = os.path.relpath(svg_path, latex_build_dir).replace(os.sep, "/")
        png_rel = os.path.relpath(png_path, latex_build_dir).replace(os.sep, "/")
        replacements[svg_rel] = png_rel
        replacements[os.path.basename(svg_path)] = os.path.basename(png_path)

    for tex_path in glob.glob(os.path.join(latex_build_dir, "*.tex")):
        with open(tex_path, "r", encoding="utf-8") as f:
            text = f.read()
        original = text
        for svg_name, png_name in replacements.items():
            text = text.replace(svg_name, png_name)
        # Sphinx may emit SVG paths as `{{name}.svg}` rather than `name.svg`.
        # At this point every SVG in the LaTeX build directory has a PNG pair,
        # so rewriting the remaining `.svg` extensions in TeX files is safe.
        text = text.replace(".svg", ".png")
        if text != original:
            with open(tex_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"   🔁 Referencias SVG actualizadas en {os.path.basename(tex_path)}")

    return True


def mirror_shared_asset_paths_for_latex(latex_build_dir):
    """Mirror root `_static` and `_images` into nested paths referenced by Sphinx LaTeX.

    In standalone per-language builds, MyST/Sphinx may serialize an image
    reference such as `_static/logo.png` from a nested source page as
    `es/05_contenidos_basicos/_static/logo.png`.  The real files live in the
    LaTeX build root `_static/`.  The same can happen with `_images/` assets.
    Mirroring those directories into the referenced
    nested locations avoids OS-specific path hacks and works on all runners.
    """
    asset_sources = {
        "_static": os.path.join(latex_build_dir, "_static"),
        "_images": os.path.join(latex_build_dir, "_images"),
    }
    if not os.path.isdir(asset_sources["_static"]):
        asset_sources["_static"] = os.path.join(PROJECT_ROOT, BOOK_DIR, "_static")

    needed_dirs = {"_static": set(), "_images": set()}
    for tex_path in glob.glob(os.path.join(latex_build_dir, "*.tex")):
        with open(tex_path, "r", encoding="utf-8") as f:
            text = f.read()
        for asset_dir in needed_dirs:
            pattern = rf"([A-Za-z0-9_./-]+/{re.escape(asset_dir)}/)"
            for match in re.finditer(pattern, text):
                prefix = match.group(1).strip("./")
                if prefix and prefix != f"{asset_dir}/":
                    needed_dirs[asset_dir].add(os.path.join(latex_build_dir, prefix))

    for asset_dir, source_dir in asset_sources.items():
        if not os.path.isdir(source_dir):
            continue
        for dest_dir in sorted(needed_dirs[asset_dir]):
            if os.path.abspath(dest_dir) == os.path.abspath(source_dir):
                continue
            parent = os.path.dirname(dest_dir)
            os.makedirs(parent, exist_ok=True)
            if os.path.exists(dest_dir):
                continue
            shutil.copytree(source_dir, dest_dir)
            print(
                f"   📁 {asset_dir} replicado para LaTeX: "
                f"{os.path.relpath(dest_dir, latex_build_dir)}"
            )


def copy_root_latex_support_files(latex_build_dir):
    """Copy top-level helper files like latexmkrc into the build dir."""
    templates_root = os.path.abspath("latex_templates")
    if not os.path.isdir(templates_root):
        return

    for item in os.listdir(templates_root):
        source = os.path.join(templates_root, item)
        dest = os.path.join(latex_build_dir, item)
        if os.path.isfile(source):
            shutil.copy2(source, dest)


def build_pdf_for_lang(lang, engine_name):
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
        jupyter_book = get_jupyter_book()
        if not jupyter_book:
            print("❌ No se encontró jupyter-book.")
            print("   Ejecuta primero el setup oficial del proyecto y usa el Python de .venv:")
            if os.name == "nt":
                print(r"   py scripts\setup_env.py")
                print(r"   .venv\Scripts\python.exe scripts\export_pdf.py")
            else:
                print("   python scripts/setup_env.py")
                print("   .venv/bin/python scripts/export_pdf.py")
            return False

        cmd = [jupyter_book, "build", "--builder", "latex", src_dir, "--all"]
        subprocess.run(cmd, shell=(os.name == "nt"), check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en jupyter-book build ({lang}): {e}")
        return False
    except OSError as e:
        print(f"❌ No se pudo ejecutar jupyter-book ({lang}): {e}")
        return False
    finally:
        if temp_mode and not os.path.exists(latex_build_dir) and os.path.exists(src_dir):
            shutil.rmtree(src_dir)

    print("🎨 Aplicando plantillas LaTeX personalizadas...", flush=True)
    templates_root = os.path.abspath("latex_templates")

    # 0. Generate metadata tex file from YAML config
    generate_metadata_tex(lang, latex_build_dir)
    copy_root_latex_support_files(latex_build_dir)

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

    if not prepare_svg_images_for_latex(latex_build_dir):
        return False
    mirror_shared_asset_paths_for_latex(latex_build_dir)

    print(f"📂 Compilando PDF en {latex_build_dir}...")
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

        engine_candidates = resolve_latex_engine_candidates(engine_name)
        if not engine_candidates:
            print(f"❌ No se encontró el motor solicitado: {engine_name}.")
            return False

        last_error = None
        for candidate_index, (candidate_name, tex_engine_path) in enumerate(engine_candidates, start=1):
            try:
                if len(engine_candidates) > 1:
                    print(
                        f"🔁 Motor candidato {candidate_index}/{len(engine_candidates)}: "
                        f"{candidate_name}"
                    )
                compile_latex_with_engine(tex_engine_path, main_tex)
                last_error = None
                break
            except subprocess.CalledProcessError as exc:
                last_error = exc
                print(f"⚠️  Falló el motor {candidate_name}: {exc}")
                if candidate_index < len(engine_candidates):
                    print("   Probando el siguiente motor disponible...")

        if last_error is not None:
            raise last_error

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
    allow_existing = "--allow-existing" in sys.argv
    engine = "tectonic"

    if "--engine" in sys.argv:
        try:
            engine = sys.argv[sys.argv.index("--engine") + 1].strip().lower()
        except IndexError:
            print("❌ Falta el valor de --engine. Usa: --engine tectonic|latexmk|auto")
            sys.exit(1)

    if engine not in SUPPORTED_ENGINES:
        print(f"❌ Motor no soportado: {engine}")
        print(f"   Motores válidos: {', '.join(SUPPORTED_ENGINES)}")
        sys.exit(1)

    if "--help" in sys.argv or "-h" in sys.argv:
        print(
            """
Uso:
  python scripts/export_pdf.py                                   # usa Tectonic por defecto
  python scripts/export_pdf.py --engine tectonic                 # flujo normal/simple/portable
  python scripts/export_pdf.py --engine latexmk                  # fallback avanzado explícito
  python scripts/export_pdf.py --engine auto                     # diagnóstico: Tectonic → latexmk → pdflatex
  python scripts/export_pdf.py --allow-existing                  # en CI, permite continuar si ya existen PDFs publicados

La opción --allow-existing es un salvavidas para despliegue: NO oculta el fallo
de generación, pero permite publicar la web si `book/_static/teachbook_<lang>.pdf`
ya existe y tiene contenido.
"""
        )
        return

    selected_engine = resolve_latex_engine(engine)
    if not selected_engine:
        print(f"⚠️  No se detectó el motor solicitado: {engine}.")
        if engine == "tectonic":
            print("   El flujo principal del proyecto usa Tectonic.")
            print("   Puedes instalarlo automáticamente ejecutando:")
            if os.name == "nt":
                print(r"   .venv\Scripts\python.exe scripts\setup_latex.py --yes")
            else:
                print("   .venv/bin/python scripts/setup_latex.py --yes")
        elif engine == "latexmk":
            print("   El fallback avanzado requiere latexmk + xelatex ya instalados.")
            print("   Para CI o diagnóstico avanzado usa:")
            if os.name == "nt":
                print(r"   .venv\Scripts\python.exe scripts\setup_latex.py --ci-full")
            else:
                print("   .venv/bin/python scripts/setup_latex.py --ci-full")
        else:
            print("   Instala Tectonic con setup_latex.py --yes o usa --engine latexmk si ya tienes toolchain completa.")
        sys.exit(1)

    print(f"🔧 Motor PDF solicitado: {engine} ({selected_engine})")

    languages = get_languages()
    print(f"🔍 Idiomas detectados para PDF: {languages}")

    success_count: int = 0
    for lang in languages:
        if build_pdf_for_lang(lang, engine):
            success_count = success_count + 1  # type: ignore

    if success_count == len(languages):
        print(f"\n✅ Todos los PDFs ({success_count}) se generaron correctamente.")
        sys.exit(0)
    else:
        print(f"\n⚠️ Se generaron {success_count} de {len(languages)} PDFs.")
        if allow_existing:
            missing_or_empty = []
            for lang in languages:
                pdf_path = os.path.join(STATIC_DIR, f"teachbook_{lang}.pdf")
                if not os.path.isfile(pdf_path) or os.path.getsize(pdf_path) == 0:
                    missing_or_empty.append(pdf_path)

            if not missing_or_empty:
                print(
                    "✅ Modo --allow-existing: la generación falló, pero existen "
                    "PDFs publicados para todos los idiomas. El deploy puede continuar."
                )
                sys.exit(0)

            print("❌ Modo --allow-existing: faltan PDFs existentes válidos:")
            for pdf_path in missing_or_empty:
                print(f"   - {pdf_path}")

        sys.exit(1)


if __name__ == "__main__":
    main()
