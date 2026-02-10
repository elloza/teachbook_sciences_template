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
    url = ""
    filename = ""
    
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
        
        os.remove(filename)
        executable_name = "tectonic.exe" if system == "windows" else "tectonic"
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        shutil.move(executable_name, os.path.join(current_script_dir, executable_name))
        
        print(f"✅ Tectonic colocado en: {os.path.join(current_script_dir, executable_name)}")
        return True
    except Exception as e:
        print(f"❌ Error descargando/extrayendo: {e}")
        return False

def main():
    print("🔍 Verificando entorno LaTeX...")
    if is_tectonic_installed():
        print("✅ Tectonic ya está instalado.")
        return

    auto_confirm = "--yes" in sys.argv or "-y" in sys.argv
    print("ℹ️  No se encontró Tectonic.")
    
    if auto_confirm:
        confirm = 's'
    else:
        confirm = input("¿Quieres instalarlo ahora? (s/n): ").strip().lower()
        
    if confirm == 's':
        if not install_tectonic_pip():
            print("⚠️  Pip falló. Intentando descarga directa...")
            install_tectonic_binary()
    else:
        print("⚠️  Instalación cancelada.")

if __name__ == "__main__":
    main()
