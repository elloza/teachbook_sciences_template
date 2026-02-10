import subprocess
import os
import shutil
import sys
import glob

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
        return ["default"] # Single language mode
        
    return sorted(languages)

def check_latex_installed():
    """Checks if tectonic, latexmk or pdflatex is available."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_tectonic = os.path.join(script_dir, "tectonic.exe" if os.name == 'nt' else "tectonic")
    
    if os.path.exists(local_tectonic):
        return local_tectonic
        
    return shutil.which("tectonic") or shutil.which("latexmk") or shutil.which("pdflatex")

def ensure_static_dir():
    """Ensures the static directory exists."""
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

def glob_pdf(search_dir):
    for file in os.listdir(search_dir):
        if file.endswith(".pdf"):
            return os.path.abspath(os.path.join(search_dir, file))
    return None

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
        temp_root = os.path.abspath(os.path.join(BOOK_DIR, f"temp_pdf_{lang}"))
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
            
        shutil.copy2(os.path.join(BOOK_DIR, config_file), os.path.join(temp_root, "_config.yml"))
        shutil.copy2(os.path.join(BOOK_DIR, toc_file), os.path.join(temp_root, "_toc.yml"))
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
        cmd = ["jupyter-book", "build", "--builder", "latex", src_dir, "--all"]
        subprocess.run(cmd, shell=(os.name == 'nt'), check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en jupyter-book build ({lang}): {e}")
        return False

    print("🎨 Aplicando plantillas LaTeX personalizadas...", flush=True)
    templates_dir = os.path.abspath("latex_templates")
    if os.path.exists(templates_dir) and os.path.exists(latex_build_dir):
        for item in os.listdir(templates_dir):
            if item.endswith(".tex") or item.endswith(".cls") or item.endswith(".png"):
                shutil.copy2(os.path.join(templates_dir, item), os.path.join(latex_build_dir, item))

    print(f"📂 Compilando con Tectonic en {latex_build_dir}...")
    current_dir = os.getcwd()
    try:
        os.chdir(latex_build_dir)
        tex_files = glob.glob("*.tex")
        if not tex_files:
            print("❌ No se encontró archivo .tex.")
            return False
            
        main_tex = tex_files[0]
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
            cmd = [tex_engine_path, "-xelatex", "-interaction=nonstopmode", "-halt-on-error", main_tex]
        else:
            # Fallback to pdflatex
            cmd = [tex_engine_path, "-interaction=nonstopmode", "-halt-on-error", main_tex]

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
        return False
    finally:
        os.chdir(current_dir)
        if temp_mode and os.path.exists(src_dir):
            shutil.rmtree(src_dir)

def main():
    print("📚 Iniciando exportación de PDF multi-idioma...")
    if not check_latex_installed():
        print("⚠️  No se detectó un motor LaTeX. Instala Tectonic o TeX Live.")
        sys.exit(1)

    languages = get_languages()
    print(f"🔍 Idiomas detectados para PDF: {languages}")

    success_count = 0
    for lang in languages:
        if build_pdf_for_lang(lang):
            success_count += 1
    
    if success_count == len(languages):
        print(f"\n✅ Todos los PDFs ({success_count}) se generaron correctamente.")
        sys.exit(0)
    else:
        print(f"\n⚠️ Se generaron {success_count} de {len(languages)} PDFs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
