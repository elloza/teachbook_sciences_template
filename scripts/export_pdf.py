import subprocess
import os
import shutil
import sys
import glob

# Configuration
BOOK_DIR = "book"
BUILD_PDF_DIR = os.path.join(BOOK_DIR, "_build", "latex")
STATIC_DIR = os.path.join(BOOK_DIR, "_static")
PDF_FILENAME = "teachbook.pdf"
DEST_PDF_PATH = os.path.join(STATIC_DIR, PDF_FILENAME)

def check_latex_installed():
    """Checks if tectonic, latexmk or pdflatex is available."""
    # Also check if tectonic is in scripts/ folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_tectonic = os.path.join(script_dir, "tectonic.exe" if os.name == 'nt' else "tectonic")
    
    if os.path.exists(local_tectonic):
        return local_tectonic
        
    return shutil.which("tectonic") or shutil.which("latexmk") or shutil.which("pdflatex")

def ensure_static_dir():
    """Ensures the static directory exists."""
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)
        print(f"📁 Directorio creado: {STATIC_DIR}")

def build_pdf():
    """Builds the PDF using jupyter-book latex builder + tectonic/latexmk."""
    
    # 0. Check for LaTeX tools
    if not check_latex_installed():
        print("⚠️  No se detectó un motor LaTeX.")
        print("ℹ️  Puedes instalar uno ligero ejecutando: python scripts/setup_latex.py")
        print("ℹ️  O espera a publicar: el PDF se generará automáticamente en GitHub Actions.")
        return False

    print("🚀 Iniciando generación de PDF (esto puede tardar)...")
    
    # 1. Generate LaTeX source
    print("📝 Generando archivos LaTeX con Jupyter Book...", flush=True)
    try:
        # Debug: Check version via CLI
        subprocess.run(["jupyter-book", "--version"], check=False)
        
        # Build command: Use --builder before the directory
        # We don't use check=True here so we can handle the error manually and show output
        result = subprocess.run(
            ["jupyter-book", "build", "--builder", "latex", BOOK_DIR], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            print("❌ Error en jupyter-book build:", flush=True)
            print("--- STDOUT ---", flush=True)
            print(result.stdout, flush=True)
            print("--- STDERR ---", flush=True)
            print(result.stderr, flush=True)
            return False
            
    except Exception as e:
        print(f"❌ Error inesperado ejecutando jupyter-book: {e}", flush=True)
        return False

    # 2. Compile PDF
    print(f"📂 Archivos LaTeX generados en {BUILD_PDF_DIR}")
    current_dir = os.getcwd()
    os.chdir(BUILD_PDF_DIR)
    
    try:
        # Find the main .tex file
        tex_files = glob.glob("*.tex")
        if not tex_files:
             print("❌ No se encontró ningún archivo .tex generado.")
             return False
        
        main_tex = tex_files[0]
        print(f"📄 Archivo principal encontrado: {main_tex}")

        latex_path = check_latex_installed()
        
        # Priority 1: Tectonic
        if latex_path and "tectonic" in str(latex_path).lower():
            print(f"🔨 Compilando con Tectonic ({latex_path})...")
            # Tectonic downloads packages on the fly, so we allow network access
            # We run it on the .tex file directly
            cmd = [latex_path, "-X", "compile", main_tex]
            subprocess.run(cmd, check=True)
            
        # Priority 2: Make (Unix/Linux standard)
        elif shutil.which("make"):
            print("🔨 Compilando con Make...")
            subprocess.run(["make"], check=True)
            
        # Priority 3: Latexmk (Windows standard if no make)
        elif shutil.which("latexmk"):
            current_tex = main_tex
            print("🔨 Compilando con Latexmk...")
            subprocess.run(["latexmk", "-pdf", "-f", "-interaction=nonstopmode", current_tex], check=True)
            
        else:
            print("❌ Se detectó pdflatex pero no una herramienta de automatización compatible (tectonic/make/latexmk).")
            return False

        print("✅ Compilación terminada.")
        
        # 3. Copy to _static
        # Tectonic produces the pdf in the same folder by default
        pdf_source = glob_pdf()
        if pdf_source:
             os.chdir(current_dir) # Go back before copying
             ensure_static_dir()
             shutil.copy(pdf_source, DEST_PDF_PATH)
             print(f"🎉 PDF exportado correctamente a:\n   {DEST_PDF_PATH}")
             return True
        else:
             print("❌ No se encontró el archivo PDF final.")
             return False

    except subprocess.CalledProcessError:
        print("❌ Error durante la compilación del PDF.")
        print("   (Si usas Tectonic, asegúrate de tener conexión a Internet la primera vez).")
        return False
    finally:
        os.chdir(current_dir)

def glob_pdf():
    # Find the generated pdf in the current dir
    for file in os.listdir("."):
        if file.endswith(".pdf"):
            return os.path.abspath(file)
    return None

if __name__ == "__main__":
    success = build_pdf()
    if not success:
        sys.exit(1)
