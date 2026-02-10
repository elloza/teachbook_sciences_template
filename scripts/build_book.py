import subprocess
import sys
import os
import glob
import shutil
import json

# Mapping of language codes to display names
LANG_DISPLAY_NAMES = {
    "es": "Español",
    "en": "English",
    "fr": "Français",
    "pt": "Português",
    "de": "Deutsch",
    "it": "Italiano"
}

BOOK_DIR = "book"
BUILD_ROOT = os.path.join(BOOK_DIR, "_build")
FINAL_HTML_DIR = os.path.join(BUILD_ROOT, "html")

def get_languages():
    """Detects languages based on _config_<lang>.yml files."""
    configs = glob.glob(os.path.join(BOOK_DIR, "_config_*.yml"))
    languages = []
    
    for conf in configs:
        filename = os.path.basename(conf)
        # Extract 'es' from '_config_es.yml'
        lang_code = filename.replace("_config_", "").replace(".yml", "")
        languages.append(lang_code)
    
    if not languages and os.path.exists(os.path.join(BOOK_DIR, "_config.yml")):
        return ["default"] # Single language mode
        
    return sorted(languages)

def generate_languages_json(languages, output_static_dir=None):
    """Generates a JSON file with available languages for the JS switcher."""
    lang_data = []
    for lang in languages:
        if lang == "default":
            continue
        lang_data.append({
            "code": lang,
            "name": LANG_DISPLAY_NAMES.get(lang, lang.upper())
        })
    
    # Target directory: either source or specified build dir
    target_dir = output_static_dir if output_static_dir else os.path.join(BOOK_DIR, "_static")
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    json_path = os.path.join(target_dir, "languages.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(lang_data, f, indent=2, ensure_ascii=False)
    
    print(f"🌍 Archivo de idiomas generado en: {json_path}")

def fix_pdf_paths(build_dir, pdf_filename):
    """Fixes relative paths for the PDF download button in HTML files within a specific build dir."""
    print(f"🔧 Corrigiendo rutas del botón PDF en {build_dir}...")
    
    for html_file in glob.glob(os.path.join(build_dir, "**", "*.html"), recursive=True):
        rel_to_root = os.path.relpath(build_dir, os.path.dirname(html_file))
        
        if rel_to_root == ".":
            correct_path = f"_static/{pdf_filename}"
        else:
            correct_path = f"{rel_to_root}/_static/{pdf_filename}".replace("\\", "/")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        target_string = f'_static/{pdf_filename}'
        
        if target_string in content:
            new_content = content.replace(f'href="{target_string}"', f'href="{correct_path}"')
            
            if new_content != content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)

def build_language(lang):
    """Builds the book for a specific language using a standalone temporary directory."""
    print(f"\n🔨 Construyendo versión STANDALONE: {lang.upper()}...")
    
    if lang == "default":
        # Default behavior: build the root book (usually Spanish)
        config_file = "_config.yml"
        toc_file = "_toc.yml"
        build_cache_dir = os.path.join(BOOK_DIR, "_build")
        final_dest = FINAL_HTML_DIR
        pdf_name = "teachbook.pdf"
        
        # Standard build logic for default
        if os.path.exists(build_cache_dir):
            shutil.rmtree(build_cache_dir)
            
        cmd = [
            "jupyter-book", "build", os.path.abspath(BOOK_DIR),
            "--config", os.path.abspath(os.path.join(BOOK_DIR, config_file)),
            "--toc", os.path.abspath(os.path.join(BOOK_DIR, toc_file)),
            "--all"
        ]
        try:
            print(f"🚀 Ejecutando build DEFAULT: {' '.join(cmd)}")
            subprocess.check_call(cmd, shell=(os.name == 'nt'))
            print(f"✅ Versión default lista en: {final_dest}")
        except subprocess.CalledProcessError:
            print(f"❌ Error compilando idioma: {lang}")
            sys.exit(1)
        return

    # LOCALIZED STANDALONE BUILD (en, fr, etc.)
    config_file = f"_config_{lang}.yml"
    toc_file = f"_toc_{lang}.yml"
    pdf_name = f"teachbook_{lang}.pdf"
    
    # 1. Create temporary standalone project
    temp_build_root = os.path.abspath(os.path.join(BOOK_DIR, f"temp_build_{lang}"))
    if os.path.exists(temp_build_root):
        shutil.rmtree(temp_build_root)
    os.makedirs(temp_build_root)
    
    # 2. Copy localized content AS A SUBFOLDER to keep paths valid (e.g., temp_en/en/intro.md)
    lang_src_dir = os.path.join(BOOK_DIR, lang)
    lang_dst_dir = os.path.join(temp_build_root, lang)
    if not os.path.exists(lang_src_dir):
        print(f"❌ Error: No existe la carpeta de contenido para '{lang}': {lang_src_dir}")
        return

    print(f"📂 Preparando entorno standalone en: {temp_build_root}")
    print(f"📂 Copiando contenido de '{lang}' a carpeta interna para mantener rutas...")
    shutil.copytree(lang_src_dir, lang_dst_dir)
            
    # 3. Copy _static folder (required for logo, css, js)
    static_src = os.path.join(BOOK_DIR, "_static")
    static_dst = os.path.join(temp_build_root, "_static")
    if os.path.exists(static_src):
        shutil.copytree(static_src, static_dst)
        
    # 4. Copy and rename config/toc
    shutil.copy2(os.path.join(BOOK_DIR, config_file), os.path.join(temp_build_root, "_config.yml"))
    shutil.copy2(os.path.join(BOOK_DIR, toc_file), os.path.join(temp_build_root, "_toc.yml"))
    
    # 5. Build from the temp directory
    cmd = ["jupyter-book", "build", temp_build_root, "--all"]
    
    try:
        print(f"🚀 Ejecutando build STANDALONE ({lang}): {' '.join(cmd)}")
        subprocess.check_call(cmd, shell=(os.name == 'nt'))
        
        # The output will be in temp_build_root/_build/html/en/ (since en is a subfolder)
        built_html_path_nested = os.path.join(temp_build_root, "_build", "html", lang)
        final_dest = os.path.join(FINAL_HTML_DIR, lang)

        if not os.path.exists(built_html_path_nested):
             built_html_path_nested = os.path.join(temp_build_root, "_build", "html")

        # Fix PDF paths BEFORE moving
        if os.path.exists(built_html_path_nested):
            fix_pdf_paths(built_html_path_nested, pdf_name)

        print(f"🚚 Moviendo de {built_html_path_nested} a {final_dest}")
        if os.path.exists(final_dest):
            shutil.rmtree(final_dest)
        shutil.copytree(built_html_path_nested, final_dest)
        print(f"✅ Versión {lang} movida correctamente.")

        # CRITICAL FIX: Merge the generated _static folder (containing theme assets)
        # from the temp build to the final root _static folder.
        temp_static_dir = os.path.join(temp_build_root, "_build", "html", "_static")
        final_static_dir = os.path.join(FINAL_HTML_DIR, "_static")
        
        if os.path.exists(temp_static_dir):
            print(f"📦 Merging theme assets from temp build ({lang}) to global _static...")
            
            # DEBUG: List source files to verify we actually have something to copy
            print(f"   🔍 Source _static content ({temp_static_dir}):")
            try:
                for item in os.listdir(temp_static_dir):
                    print(f"      - {item}")
            except Exception as e:
                print(f"      ⚠️ Error listing source: {e}")

            if not os.path.exists(final_static_dir):
                os.makedirs(final_static_dir)
            
            # Use the robust merge_dir_into (now global)
            merge_dir_into(temp_static_dir, final_static_dir)
            
            # DEBUG: Verify copy
            print(f"   ✅ Merge complete. Final _static count: {len(os.listdir(final_static_dir))}")

    except subprocess.CalledProcessError:
        print(f"❌ Error compilando idioma standalone: {lang}")
        sys.exit(1)
    finally:
        # Cleanup temp directory
        if os.path.exists(temp_build_root):
            shutil.rmtree(temp_build_root)

def merge_dir_into(src_dir, dst_dir):
    """Merge src_dir into dst_dir without deleting dst_dir first.
    Overwrites files that already exist. Skips locked files gracefully."""
    print(f"   🔄 Merging '{src_dir}' -> '{dst_dir}'")
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        target_dir = os.path.join(dst_dir, rel_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(target_dir, file)
            try:
                shutil.copy2(src_file, dst_file)
            except PermissionError:
                print(f"      ⚠️  Skipped locked file: {dst_file}")
            except Exception as e:
                print(f"      ⚠️  Copy error: {e}")

def create_redirect_index(default_lang="es"):
    """Creates a root index.html that redirects to the default language."""
    redirect_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url={default_lang}/intro.html" />
        <script>window.location.href = "{default_lang}/intro.html";</script>
    </head>
    <body>
        <p>Redirecting to <a href="{default_lang}/intro.html">{default_lang} version</a>...</p>
    </body>
    </html>
    """
    with open(os.path.join(FINAL_HTML_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(redirect_html)
    print(f"🔀 Redirección raíz creada apuntando a: /{default_lang}/")

def main():
    print("📚 Iniciando proceso de construcción multi-idioma...")
    languages = get_languages()
    print(f"🔍 Idiomas detectados: {languages}")
    
    # Pre-create root _static to avoid race conditions or missing dirs
    if not os.path.exists(FINAL_HTML_DIR):
        os.makedirs(FINAL_HTML_DIR)
    final_static = os.path.join(FINAL_HTML_DIR, "_static")
    if not os.path.exists(final_static):
        os.makedirs(final_static)

    generate_languages_json(languages)
    
    for lang in languages:
        build_language(lang)
    
    # 1. Merge our custom static files into the root _static
    custom_static = os.path.join(BOOK_DIR, "_static")
    if os.path.exists(custom_static):
        merge_dir_into(custom_static, final_static)
        print(f"📦 Custom static assets merged into: {final_static}")

    # 2. Regenerate languages.json in ALL _static directories (Just in case)
    generate_languages_json(languages, final_static)
    
    if "default" not in languages and len(languages) > 0:
        default_lang = "es" if "es" in languages else languages[0]
        create_redirect_index(default_lang)
        
    print("\n✅ ¡Construcción completa!")
    print(f"🌍 Web disponible en: {os.path.abspath(FINAL_HTML_DIR)}")

    # Ensure .nojekyll exists to prevent GitHub Pages from ignoring _static
    nojekyll_path = os.path.join(FINAL_HTML_DIR, ".nojekyll")
    if not os.path.exists(nojekyll_path):
        with open(nojekyll_path, 'w') as f:
            pass
        print("✅ Archivo .nojekyll creado para GitHub Pages.")

if __name__ == "__main__":
    main()
