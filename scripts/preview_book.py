import os
import sys
import subprocess
import time
from watchdog.observers import Observer  # type: ignore
from watchdog.events import FileSystemEventHandler  # type: ignore
# Add current directory to sys.path to ensure local modules can be imported
# This is needed because the script might be run from root or from scripts/
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

try:
    import build_book  # type: ignore
except ImportError:
    # Fallback or re-raise if needed
    raise

# Configuration
BOOK_DIR = "book"
BUILD_DIR = os.path.join(BOOK_DIR, "_build", "html")
PORT = 8000
CONFIG_FILE = os.path.abspath(os.path.join(BOOK_DIR, "_config.yml"))

class ConfigHandler(FileSystemEventHandler):
    """Watches for changes in _config.yml and regenerates sphinx config."""
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == CONFIG_FILE:
            print("\n🔄 Detectado cambio en _config.yml. Regenerando configuración...")
            generate_sphinx_config()
            # Touch a file to trigger sphinx-autobuild rebuild if needed
            # Usually updating conf.py (which generate_sphinx_config does) is enough

def generate_sphinx_config():
    """Generates a conf.py from _config.yml for sphinx-autobuild compatibility."""
    try:
        # Detect available languages first
        languages = build_book.get_languages()
        build_book.generate_languages_json(languages)
        
        cmd = ["jupyter-book", "config", "sphinx", BOOK_DIR]
        # Run quietly
        subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Explicitly touch conf.py to ensure watchdog sees the change
        conf_path = os.path.join(BOOK_DIR, "conf.py")
        if os.path.exists(conf_path):
            os.utime(conf_path, None)
            
        print("✅ Configuración actualizada y conf.py regenerado.")
    except subprocess.CalledProcessError:
        print("❌ Error regenerando configuración.")

def start_config_watcher():
    """Starts a background thread to watch _config.yml."""
    event_handler = ConfigHandler()
    observer = Observer()
    # Watch the book directory
    observer.schedule(event_handler, list(os.path.split(CONFIG_FILE))[0], recursive=False)
    observer.start()
    return observer

def main():
    print("🚀 Iniciando Previsualización Robusta (Full Build + Watch)...")
    
    # 0. RUN FULL BUILD FIRST
    # This ensures consistency, including English updates and static files.
    print("\n🔨 Ejecutando construcción completa inicial (build_book.py)...")
    try:
        build_book.main()
    except Exception as e:
        print(f"❌ Error en la construcción inicial: {e}")
        # We continue anyway to allow debugging via preview, or should we stop?
        # User requested consistency, but blocking preview might be annoying.
        # Let's pause to let them see the error.
        time.sleep(2)

    # 1. Initial config generation (for sphinx-autobuild internal use)
    generate_sphinx_config()
    
    # 2. Start Config Watcher
    observer = start_config_watcher()
    
    # 3. Start sphinx-autobuild
    cmd = [
        "sphinx-autobuild",
        BOOK_DIR,
        BUILD_DIR,
        "--port", str(PORT),
        "--open-browser",
        "--watch", BOOK_DIR, 
        "--ignore", "_build/*",
        "--ignore", ".*",
        "--re-ignore", "_config.yml", # Let our handler handle this one specifically if we wanted, 
                                      # but sphinx-autobuild also watches it. 
                                      # The key is that we NEED to run the generation command.
    ]
    
    try:
        # Run sphinx-autobuild in the foreground (no piping).
        # This keeps Ctrl+C working naturally on Windows.
        print(f"\n⏳ Iniciando servidor de previsualización en http://localhost:{PORT}...")
        print("⌨️  Pulsa Ctrl+C para detener.\n")
        
        process = subprocess.Popen(cmd, shell=True)
        process.wait()

    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor (Ctrl+C recibido)...")
        if 'observer' in locals(): observer.stop()
        if 'process' in locals():
            process.terminate()
            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                print("⚠️ Forzando detención...")
                process.kill()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if 'observer' in locals(): observer.stop()
    
    if 'observer' in locals():
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
