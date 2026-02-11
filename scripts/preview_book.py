import os
import sys
import subprocess
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
try:
    # Try importing as if we are in the scripts directory or it's in path
    import build_book
except ImportError:
    # If we are running from root, add scripts to path explicitly if needed
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import build_book

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
    
    print(f"\n⏳ Iniciando servidor de previsualización...")
    
    try:
        # Use Popen to capture stderr/stdout
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            bufsize=1, 
            encoding='utf-8', 
            errors='replace'
        )

        def echo_output(p):
            for line in p.stdout:
                # Watch for the "ready" signal to clear screen for a friendly view
                if "Serving on" in line:
                    # Clear screen on Windows or Unix
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("\n" + "="*50)
                    print(f"✅  ¡Todo listo! El libro está funcionando.")
                    print(f"🌍  Web local: http://localhost:{PORT}")
                    print(f"⌨️   Pulsa Ctrl+C para detener.")
                    print("="*50 + "\n")
                else:
                    sys.stdout.write(line)

        def echo_stderr(p):
            for line in p.stderr:
                # Filter out the noisy asyncio connection reset errors (Multi-line traceback)
                # We filter common lines found in that specific asyncio/proactor error dump
                args_to_ignore = [
                    "ConnectionResetError", "WinError 10054",
                    "asyncio", "proactor_events.py",
                    "_ProactorBasePipeTransport._call_connection_lost",
                    "files in the same directory", # benign warning
                    "self._context.run(self._callback",
                    "self._sock.shutdown(socket.SHUT_RDWR",
                    "Traceback (most recent call last):", # Risky, but usually part of the noise if accompanied by others
                    "Exception in callback _ProactorBasePipeTransport"
                ]
                
                # Check if line matches any ignored pattern
                if any(ignored in line for ignored in args_to_ignore):
                    continue
                
                sys.stderr.write(line)
                sys.stderr.flush()

        # Run readers in threads
        t_out = threading.Thread(target=echo_output, args=(process,))
        t_out.daemon = True
        t_out.start()
        
        t_err = threading.Thread(target=echo_stderr, args=(process,))
        t_err.daemon = True
        t_err.start()

        # Wait for the process to finish
        # Wait for the process to finish using a loop to keep main thread responsive to signals
        try:
            while process.poll() is None:
                time.sleep(0.5)
        except KeyboardInterrupt:
            # Forward the interrupt to the subprocess
            print("\n🛑 Deteniendo servidor (Ctrl+C recibido)...")
            
            # Stop observer first
            if 'observer' in locals():
                observer.stop()
                
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                print("⚠️ Forzando detención...")
                process.kill()
                
        t_out.join(timeout=1)
        t_err.join(timeout=1)

    except KeyboardInterrupt:
        print("\n🛑 Deteniendo servidor...")
        if 'observer' in locals(): observer.stop()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if 'observer' in locals(): observer.stop()
    
    if 'observer' in locals():
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()
