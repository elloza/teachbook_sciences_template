import subprocess
import sys
import shutil
import platform
import os
import urllib.request
import zipfile
import tarfile

def is_tectonic_installed():
    """Checks if tectonic is installed."""
    return shutil.which("tectonic") is not None

def install_tectonic_pip():
    """Tries installing tectonic via pip."""
    print("📦 Intentando instalar Tectonic con pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "tectonic"], check=True)
        print("✅ Tectonic instalado correctamente con pip.")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error instalando con pip.")
        return False

def install_tectonic_binary():
    """Downloads the binary directly."""
    print("⬇️  Descargando binario de Tectonic desde GitHub...")
    
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    url = ""
    filename = ""
    
    # Simple architecture detection (assuming x86_64 mostly)
    if system == "windows":
        url = "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-x86_64-pc-windows-msvc.zip"
        filename = "tectonic.zip"
    elif system == "darwin":
        url = "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-x86_64-apple-darwin.tar.gz"
        filename = "tectonic.tar.gz"
    elif system == "linux":
        url = "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-x86_64-unknown-linux-musl.tar.gz"
        filename = "tectonic.tar.gz"
    else:
        print(f"❌ Sistema operativo no soportado automáticamente: {system}")
        return False

    try:
        urllib.request.urlretrieve(url, filename)
        print("✅ Descarga completada.")
        
        print("📦 Extrayendo...")
        if filename.endswith(".zip"):
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(".")
        elif filename.endswith(".tar.gz"):
            with tarfile.open(filename, "r:gz") as tar_ref:
                tar_ref.extractall(".")
        
        # Cleanup archive
        os.remove(filename)

        # Move to Scripts or verify it's in path
        # For simplicity in this template, we leave it here and add instruction or move to a known location
        # A good location is scripts/ folder if we add it to PATH or call it directly
        
        executable_name = "tectonic.exe" if system == "windows" else "tectonic"
        
        # Move to current directory (scripts/) or python scripts folder? 
        # Let's put it in the same folder as this script for now, 
        # and we might need to tell export_pdf.py to look for it here.
        
        # Better: try to move to Python Scripts folder if possible, or just keep it local
        target_dir = os.path.dirname(sys.executable) # e.g. /usr/bin or Python311/
        # Check permissions?
        
        # Simplest: Leave in project root or scripts/ and add to PATH or tell user.
        # We'll rely on export_pdf finding it in current dir if we run from root?
        # export_pdf checks shutil.which.
        
        # Let's move it to the project root for easy access? Or scripts/
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        shutil.move(executable_name, os.path.join(current_script_dir, executable_name))
        
        print(f"✅ Tectonic colocado en: {os.path.join(current_script_dir, executable_name)}")
        print("ℹ️  Nota: Para que funcione globalmente, deberías añadir esa carpeta al PATH.")
        print("   Pero el script de exportación lo buscará ahí.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error descargando/extrayendo: {e}")
        return False

def main():
    print("🔍 Verificando entorno LaTeX...")
    
    if is_tectonic_installed():
        print("✅ Tectonic ya está instalado.")
        return

    print("ℹ️  No se encontró Tectonic.")
    print("   Tectonic es un motor LaTeX moderno y ligero.")
    
    confirm = input("¿Quieres instalarlo ahora? (s/n): ").strip().lower()
    if confirm == 's':
        if not install_tectonic_pip():
            print("⚠️  Pip falló. Intentando descarga directa...")
            install_tectonic_binary()
    else:
        print("⚠️  Instalación cancelada. No podrás generar PDFs localmente.")

if __name__ == "__main__":
    main()
