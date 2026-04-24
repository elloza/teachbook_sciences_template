import os
import sys
import subprocess
import argparse
import shutil
import platform
import io

# Fix: Windows cp1252 can't encode emojis — force UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

VENV_DIR = ".venv"
REQUIREMENTS_FILE = "requirements.txt"
DEV_REQUIREMENTS_FILE = "requirements-dev.txt"
MIN_PYTHON_VERSION = (3, 10)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SKILLS_SOURCE = os.path.join(PROJECT_ROOT, ".github", "skills")
SKILLS_DESTINATIONS = [
    os.path.join(PROJECT_ROOT, ".claude", "skills"),
    os.path.join(PROJECT_ROOT, ".agents", "skills"),
    os.path.join(PROJECT_ROOT, ".agent", "skills"),
]
AGENTS_MD = os.path.join(PROJECT_ROOT, "AGENTS.md")
COPILOT_INSTRUCTIONS = os.path.join(PROJECT_ROOT, ".github", "copilot-instructions.md")


def check_prerequisites():
    print("🔍 Diagnóstico del sistema")
    print("─" * 40)

    print(f"  OS:        {platform.system()} {platform.release()}")
    print(f"  Arch:      {platform.machine()}")
    print(
        f"  Python:    {sys.executable} ({sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})"
    )

    git_available = shutil.which("git") is not None
    if git_available:
        try:
            git_ver = subprocess.check_output(["git", "--version"], text=True).strip()
            print(f"  Git:       ✅ {git_ver}")
        except Exception:
            print("  Git:       ✅ disponible")
    else:
        print("  Git:       ⚠️  NO encontrado (necesario para publicar)")

    uv_available = detect_uv()
    print(
        f"  uv:        {'✅ ' + get_uv_version() if uv_available else '⚠️  NO encontrado (recomendado)'}"
    )

    venv_exists = os.path.isdir(os.path.join(PROJECT_ROOT, VENV_DIR))
    print(f"  .venv:     {'✅ existe' if venv_exists else '❌ no existe (se creará)'}")

    if sys.version_info < MIN_PYTHON_VERSION:
        print(
            f"\n  ⚠️  Python {sys.version_info.major}.{sys.version_info.minor} es demasiado antiguo."
            f" Se necesita {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+."
        )

    if not git_available:
        print(
            "\n  ⚠️  Git no está instalado. Podrás compilar el libro, pero no publicar."
        )
        print("     Instala git desde https://git-scm.com")

    print()


def get_uv_version():
    try:
        return subprocess.check_output(["uv", "--version"], text=True).strip()
    except Exception:
        return ""


def detect_uv():
    if shutil.which("uv") is not None:
        return True

    common_paths = []
    home = os.path.expanduser("~")

    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        if local_app_data:
            common_paths.append(os.path.join(local_app_data, "uv", "uv.exe"))
        common_paths.append(os.path.join(home, ".local", "bin", "uv.exe"))
        common_paths.append(os.path.join(home, ".cargo", "bin", "uv.exe"))
    else:
        common_paths.append(os.path.join(home, ".local", "bin", "uv"))
        common_paths.append(os.path.join(home, ".cargo", "bin", "uv"))

    for path in common_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return True

    return False


def fix_path_for_uv():
    home = os.path.expanduser("~")
    extra_dirs = []

    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA", "")
        if local_app_data:
            extra_dirs.append(os.path.join(local_app_data, "uv"))
        extra_dirs.append(os.path.join(home, ".local", "bin"))
        extra_dirs.append(os.path.join(home, ".cargo", "bin"))
    else:
        extra_dirs.append(os.path.join(home, ".local", "bin"))
        extra_dirs.append(os.path.join(home, ".cargo", "bin"))

    current_path = os.environ.get("PATH", "")
    added = []
    for d in extra_dirs:
        if os.path.isdir(d) and d not in current_path:
            os.environ["PATH"] = d + os.pathsep + current_path
            current_path = os.environ["PATH"]
            added.append(d)

    if added:
        print(f"  🔧 PATH actualizado con: {added}")


def offer_install_uv():
    print("\n🚀 'uv' no está instalado — es un gestor de paquetes MUCHO más rápido.")
    print("   Recomendado por Astral (creadores de Ruff). 10-100x más rápido que pip.")
    try:
        answer = input("   ¿Instalar uv ahora? [Y/n]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        return False

    if answer in ("n", "no"):
        print("   Saltando uv. Se usará pip como fallback.")
        return False

    system = platform.system()
    try:
        if system == "Windows":
            print("   Instalando uv via PowerShell...")
            ps_cmd = "irm https://astral.sh/uv/install.ps1 | iex"
            subprocess.check_call(["powershell", "-Command", ps_cmd])
        else:
            print("   Instalando uv via shell script...")
            subprocess.check_call(
                ["sh", "-c", "curl -LsSf https://astral.sh/uv/install.sh | sh"]
            )
        fix_path_for_uv()
        if detect_uv():
            print("✅ uv instalado correctamente.")
            return True
        else:
            print("⚠️  uv instalado pero no detectable en esta sesión.")
            print("   Se usará pip como fallback. Reinicia la terminal para usar uv.")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"❌ No se pudo instalar uv: {e}")
        print("   Se usará pip como fallback.")
        return False


def check_python_version():
    if sys.version_info < MIN_PYTHON_VERSION:
        print(
            f"⚠️  Python {sys.version_info.major}.{sys.version_info.minor} < {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}."
            f" Buscando una versión más reciente..."
        )
    else:
        print(
            f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )


def get_venv_python():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")


def get_venv_pip():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    return os.path.join(VENV_DIR, "bin", "pip")


def create_venv(use_uv=False):
    if os.path.exists(VENV_DIR):
        print(f"✅ Entorno virtual '{VENV_DIR}' ya existe.")
        return

    print(f"📦 Creando entorno virtual en '{VENV_DIR}'...")

    python_exe = sys.executable

    if sys.version_info < MIN_PYTHON_VERSION:
        if use_uv:
            print(
                "   Python demasiado antiguo. Intentando instalar Python 3.12 via uv..."
            )
            try:
                subprocess.check_call(["uv", "python", "install", "3.12"])
                subprocess.check_call(["uv", "venv", VENV_DIR, "--python", "3.12"])
                print("✅ Entorno virtual creado con Python 3.12 (gestionado por uv).")
                return
            except subprocess.CalledProcessError as e:
                print(f"⚠️  No se pudo instalar Python via uv: {e}")
                print("   Intentando con el Python del sistema...")

        if os.name == "nt":
            print("   Intentando encontrar versión más reciente via 'py' launcher...")
            try:
                out = subprocess.check_output(
                    ["py", "-3", "-c", "import sys; print(sys.executable)"],
                    text=True,
                ).strip()
                if out:
                    print(f"   Encontrado: {out}")
                    python_exe = out
            except Exception as e:
                print(f"   No se encontró Python más reciente via 'py': {e}")

    try:
        if use_uv:
            subprocess.check_call(["uv", "venv", VENV_DIR, "--python", python_exe])
        else:
            subprocess.check_call([python_exe, "-m", "venv", VENV_DIR])
        print("✅ Entorno virtual creado.")
    except subprocess.CalledProcessError:
        print("❌ Error creando el entorno virtual.")
        if platform.system() == "Linux":
            print(
                "   ¿Tienes python3-venv instalado? Prueba: sudo apt install python3-venv"
            )
        sys.exit(1)


def install_requirements(dev_mode=False, use_uv=False):
    pip_cmd = get_venv_pip()
    python_cmd = get_venv_python()

    if not use_uv:
        try:
            subprocess.check_call(
                [python_cmd, "-m", "pip", "install", "--upgrade", "pip"],
                stdout=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            print("⚠️  No se pudo actualizar pip.")

    if os.path.exists(REQUIREMENTS_FILE):
        print(f"⬇️  Instalando dependencias desde '{REQUIREMENTS_FILE}'...")
        try:
            if use_uv:
                subprocess.check_call(["uv", "pip", "install", "-r", REQUIREMENTS_FILE])
            else:
                subprocess.check_call([pip_cmd, "install", "-r", REQUIREMENTS_FILE])
            print("✅ Dependencias principales instaladas.")
        except subprocess.CalledProcessError:
            print("❌ Error instalando dependencias principales.")
            sys.exit(1)
    else:
        print(f"⚠️  '{REQUIREMENTS_FILE}' no encontrado. Saltando.")

    if dev_mode:
        if os.path.exists(DEV_REQUIREMENTS_FILE):
            print(
                f"🛠️  Modo Dev: Instalando dependencias desde '{DEV_REQUIREMENTS_FILE}'..."
            )
            try:
                if use_uv:
                    subprocess.check_call(
                        ["uv", "pip", "install", "-r", DEV_REQUIREMENTS_FILE]
                    )
                else:
                    subprocess.check_call(
                        [pip_cmd, "install", "-r", DEV_REQUIREMENTS_FILE]
                    )
                print("✅ Dependencias de desarrollo instaladas.")
                install_playwright_browsers(python_cmd)
            except subprocess.CalledProcessError:
                print("❌ Error instalando dependencias de desarrollo.")
                sys.exit(1)
        else:
            print(f"⚠️  '{DEV_REQUIREMENTS_FILE}' no encontrado, pero se pidió --dev.")


def install_playwright_browsers(python_cmd):
    print("🎭 Verificando instalación de navegadores Playwright...")
    try:
        subprocess.check_call(
            [python_cmd, "-c", "import playwright"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print("   Ejecutando 'playwright install' (puede tardar)...")
        subprocess.check_call([python_cmd, "-m", "playwright", "install"])
        print("✅ Navegadores Playwright instalados.")
    except subprocess.CalledProcessError:
        print("⚠️  Playwright no encontrado o falló la instalación de navegadores.")


def verify_installation(dev_mode=False):
    print("\n🔍 Verificando paquetes instalados:")
    python_cmd = get_venv_python()
    try:
        result = subprocess.check_output([python_cmd, "-m", "pip", "freeze"], text=True)

        required_packages = ["jupyter-book", "sphinx-autobuild", "watchdog"]
        if dev_mode:
            required_packages.append("playwright")

        missing = [pkg for pkg in required_packages if pkg not in result]

        if missing:
            print(f"⚠️  Paquetes faltantes: {missing}")
        else:
            print("✨ Todos los paquetes clave verificados.")

    except subprocess.CalledProcessError:
        print("❌ Error en la verificación.")


def sync_skills():
    print("\n🔄 Sincronizando skills...")
    if not os.path.isdir(SKILLS_SOURCE):
        print(f"❌ Origen de skills no encontrado: {SKILLS_SOURCE}")
        return False

    synced = 0
    total = len(SKILLS_DESTINATIONS)
    for dest in SKILLS_DESTINATIONS:
        dest_name = os.path.relpath(dest, PROJECT_ROOT)
        try:
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(SKILLS_SOURCE, dest)
            print(f"  ✅ {dest_name}")
            synced += 1
        except Exception as e:
            print(f"  ❌ {dest_name}: {e}")

    return synced == total


def sync_instructions():
    print("\n📄 Sincronizando archivos de instrucciones...")
    if not os.path.isfile(AGENTS_MD):
        print(f"  ❌ AGENTS.md no encontrado en {AGENTS_MD}")
        return False

    dest_dir = os.path.dirname(COPILOT_INSTRUCTIONS)
    try:
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(AGENTS_MD, COPILOT_INSTRUCTIONS)
        dest_name = os.path.relpath(COPILOT_INSTRUCTIONS, PROJECT_ROOT)
        print(f"  ✅ {dest_name}")
        return True
    except Exception as e:
        print(f"  ❌ copilot-instructions.md: {e}")
        return False


def print_summary(dev_mode=False, use_uv=False):
    venv_python = get_venv_python()
    venv_python_full = os.path.join(PROJECT_ROOT, venv_python)

    python_ver = "??"
    if os.path.isfile(venv_python_full):
        try:
            python_ver = subprocess.check_output(
                [venv_python_full, "--version"], text=True
            ).strip()
        except Exception:
            python_ver = "instalado"

    pkg_manager = "uv ⚡" if use_uv else "pip 🐍"

    git_status = "✅ disponible" if shutil.which("git") else "⚠️  no encontrado"

    skills_ok = all(os.path.isdir(d) for d in SKILLS_DESTINATIONS)
    skills_status = (
        f"✅ sincronizadas ({len(SKILLS_DESTINATIONS)} destinos)"
        if skills_ok
        else "⚠️  incompletas"
    )

    mode_str = " (dev)" if dev_mode else ""

    print()
    print("╔══════════════════════════════════════════════════╗")
    print(f"║  🎉 ¡Entorno TeachBook listo{mode_str}!                 ║")
    print("╠══════════════════════════════════════════════════╣")
    print(f"║  Python:  {python_ver:<37} ║")
    print(f"║  Gestor:  {pkg_manager:<37} ║")
    print(f"║  Git:     {git_status:<37} ║")
    print(f"║  Skills:  {skills_status:<37} ║")
    print("║                                                  ║")
    print("║  Siguiente paso: compilar el libro               ║")
    print("║  → python scripts/build_book.py                  ║")
    print("╚══════════════════════════════════════════════════╝")


def main():
    parser = argparse.ArgumentParser(description="Configurar entorno TeachBook")
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Instalar herramientas de desarrollo (Playwright, etc.)",
    )
    parser.add_argument(
        "--sync-only",
        action="store_true",
        help="Solo sincronizar skills e instrucciones (sin venv/dependencias)",
    )
    args = parser.parse_args()

    if args.sync_only:
        print("🔄 TeachBook — Modo Solo Sincronización")
        print("=" * 40)
        sync_skills()
        sync_instructions()
        print("\n🎉 ¡Sincronización completa!")
        return

    print("🛠️  TeachBook — Configuración del Entorno")
    print("=" * 40)
    print(f"Modo: {'Desarrollo 🛠️' if args.dev else 'Producción 🚀'}")

    check_prerequisites()

    use_uv = detect_uv()
    if not use_uv:
        use_uv = offer_install_uv()

    if use_uv:
        print("⚡ Usando 'uv' como gestor de paquetes")
    else:
        print("🐍 Usando 'pip' como gestor de paquetes")

    check_python_version()
    create_venv(use_uv=use_uv)
    install_requirements(dev_mode=args.dev, use_uv=use_uv)
    verify_installation(dev_mode=args.dev)

    sync_skills()
    sync_instructions()

    print_summary(dev_mode=args.dev, use_uv=use_uv)


if __name__ == "__main__":
    main()
