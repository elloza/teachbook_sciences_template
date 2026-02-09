import os
import sys
import subprocess
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
try:
    # Try importing as if we are in the scripts directory or it's in path
    import detect_languages
except ImportError:
    # If we are running from root, add scripts to path explicitly if needed, 
    # but usually 'from scripts import ...' is what fails if scripts/ is in path.
    # Let's try to add current dir to path and import
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import detect_languages

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
        detect_languages.detect_and_save_languages()
        
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
    print("🚀 Iniciando Previsualización Robusta (sphinx-autobuild + config watch)...")
    
    # 1. Initial config generation
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
    
    print(f"\n🌍 Servidor activo en: http://localhost:{PORT}")
    print("⌨️  Pulsa Ctrl+C para detener.")
    
    try:
        subprocess.call(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...")
        observer.stop()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    main()
