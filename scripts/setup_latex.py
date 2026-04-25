import io
import subprocess
import sys
import shutil
import platform
import os
import json
import stat
import urllib.request
import zipfile
import tarfile
import tempfile

# Fix: Windows cp1252 can't encode emojis — force UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


VENV_DIR = ".venv"


def get_venv_python():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")


def get_effective_python():
    venv_python = get_venv_python()
    if os.path.isfile(venv_python):
        return venv_python
    return sys.executable


def get_venv_bin_dir():
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts")
    return os.path.join(VENV_DIR, "bin")


def local_tectonic_candidates():
    executable_name = "tectonic.exe" if os.name == "nt" else "tectonic"
    candidates = []

    venv_bin = get_venv_bin_dir()
    if os.path.isdir(venv_bin):
        candidates.append(os.path.join(venv_bin, executable_name))

    if os.name == "nt":
        appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
        candidates.append(os.path.join(appdata, "teachbook", executable_name))
    else:
        candidates.append(os.path.expanduser(os.path.join("~", ".local", "bin", executable_name)))

    candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), executable_name))
    return candidates


def get_tectonic_command():
    found = shutil.which("tectonic")
    if found:
        return found
    for candidate in local_tectonic_candidates():
        if os.path.isfile(candidate):
            return candidate
    return None


def is_tectonic_installed():
    return get_tectonic_command() is not None


def verify_tectonic():
    tectonic = get_tectonic_command()
    if not tectonic:
        return False
    try:
        result = subprocess.run(
            [tectonic, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        if result.returncode == 0:
            version = result.stdout.strip().split("\n")[0]
            print(f"✅ Tectonic {version} funcionando correctamente.")
            print(f"   Ejecutable: {tectonic}")
            return True
    except (subprocess.TimeoutExpired, OSError):
        pass
    print("❌ Tectonic se instaló pero no se pudo ejecutar.")
    return False


def install_tectonic_pip():
    print("📦 Intentando instalar Tectonic con pip...")
    python = get_effective_python()
    is_venv = python != sys.executable
    if is_venv:
        print(f"   Usando entorno virtual: {python}")
    else:
        print("   Usando Python del sistema.")
    try:
        result = subprocess.run(
            [python, "-m", "pip", "install", "tectonic"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            print("❌ Tectonic no está disponible como paquete pip para esta plataforma.")
            print("   Esto es normal en muchos equipos; se usará descarga directa del binario oficial.")
            return False
        print("✅ Tectonic instalado correctamente con pip.")
        return True
    except Exception as exc:
        print(f"❌ Error ejecutando pip: {exc}")
        return False


def get_arch_tag():
    machine = platform.machine().lower()
    if machine in ("x86_64", "amd64"):
        return "amd64"
    if machine in ("arm64", "aarch64"):
        return "arm64"
    return None


def get_platform_target():
    system = platform.system().lower()
    arch = get_arch_tag()
    if arch is None:
        return None, None, None
    targets = {
        ("windows", "amd64"): ("x86_64-pc-windows-msvc", ".zip"),
        ("darwin", "amd64"): ("x86_64-apple-darwin", ".tar.gz"),
        ("darwin", "arm64"): ("aarch64-apple-darwin", ".tar.gz"),
        ("linux", "amd64"): ("x86_64-unknown-linux-musl", ".tar.gz"),
        ("linux", "arm64"): ("aarch64-unknown-linux-musl", ".tar.gz"),
    }
    result = targets.get((system, arch))
    if result is None:
        return None, None, None
    return system, result[0], result[1]


def fetch_latest_release():
    api_url = (
        "https://api.github.com/repos/tectonic-typesetting/tectonic/releases/latest"
    )
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "teachbook-setup"}
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("tag_name"), data.get("assets", [])
    except Exception as e:
        print(f"❌ Error consultando GitHub API: {e}")
        return None, []


def find_asset_url(assets, rust_target, ext):
    for asset in assets:
        name = asset.get("name", "")
        if rust_target in name and name.endswith(ext):
            return asset.get("browser_download_url"), name
    return None, None


def get_binary_install_dir():
    venv_bin = get_venv_bin_dir()
    if os.path.isdir(venv_bin):
        # Prefer installing inside the project venv. This is the most robust
        # option for Windows agents because it avoids global PATH edits.
        return venv_bin

    if os.name == "nt":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
        dest = os.path.join(base, "teachbook")
    else:
        dest = os.path.expanduser("~/.local/bin")
    os.makedirs(dest, exist_ok=True)
    return dest


def install_tectonic_binary():
    print("⬇️  Descargando binario de Tectonic desde GitHub...")

    system, rust_target, ext = get_platform_target()
    if rust_target is None:
        machine = platform.machine()
        sysname = platform.system()
        print(f"❌ Plataforma no soportada: {sysname} {machine}")
        print("   Plataformas soportadas: Windows/macOS/Linux en x86_64 o ARM64.")
        return False

    tag_name, assets = fetch_latest_release()
    if not tag_name or not assets:
        print("❌ No se pudo obtener la última versión desde GitHub.")
        return False

    version = tag_name.lstrip("tectonic@")
    print(f"   Última versión disponible: {version}")

    download_url, asset_name = find_asset_url(assets, rust_target, ext)
    if not download_url:
        print(f"❌ No se encontró binario para {rust_target} en la release {tag_name}.")
        print("   Revisa https://github.com/tectonic-typesetting/tectonic/releases")
        return False

    print(f"   Descargando {asset_name}...")

    install_dir = get_binary_install_dir()
    with tempfile.TemporaryDirectory(prefix="tectonic_") as tmp:
        archive_path = os.path.join(tmp, asset_name)

        try:
            urllib.request.urlretrieve(download_url, archive_path)
        except Exception as e:
            print(f"❌ Error descargando: {e}")
            return False

        print("📦 Extrayendo...")
        extract_dir = os.path.join(tmp, "extracted")
        os.makedirs(extract_dir, exist_ok=True)

        if ext == ".zip":
            with zipfile.ZipFile(archive_path, "r") as zf:
                zf.extractall(extract_dir)
        else:
            with tarfile.open(archive_path, "r:gz") as tf:
                tf.extractall(extract_dir)

        executable_name = "tectonic.exe" if system == "windows" else "tectonic"
        extracted_bin = os.path.join(extract_dir, executable_name)

        if not os.path.isfile(extracted_bin):
            for root, dirs, files in os.walk(extract_dir):
                if executable_name in files:
                    extracted_bin = os.path.join(root, executable_name)
                    break

        if not os.path.isfile(extracted_bin):
            print("❌ No se encontró el ejecutable dentro del archivo descargado.")
            return False

        dest_path = os.path.join(install_dir, executable_name)
        shutil.copy2(extracted_bin, dest_path)

        if system != "windows":
            st = os.stat(dest_path)
            os.chmod(dest_path, st.st_mode | stat.S_IEXEC)

    print(f"✅ Tectonic instalado en: {dest_path}")

    if os.path.abspath(install_dir) == os.path.abspath(get_venv_bin_dir()):
        print("   Instalado dentro de .venv: no hace falta tocar el PATH global.")
        return True

    if not shutil.which("tectonic"):
        print()
        print(
            "⚠️  Tectonic no está en tu PATH. Para usarlo, añade esta línea a tu shell:"
        )
        if system == "windows":
            print(f'   set PATH="%APPDATA%\\teachbook;%PATH%"')
            print(
                "   (O añade la carpeta en Configuración → Sistema → Variables de entorno)"
            )
            print("   Los scripts del proyecto también buscarán Tectonic en %APPDATA%\\teachbook.")
        else:
            print(f'   export PATH="{install_dir}:$PATH"')
            shell_rc = os.path.expanduser("~/.bashrc")
            preferred_shell = os.environ.get("SHELL", "")
            if "zsh" in preferred_shell:
                shell_rc = os.path.expanduser("~/.zshrc")
            print(f"   O añade la línea anterior a {shell_rc}")
        print()

    return True


def main():
    print("🔍 Verificando entorno LaTeX...")

    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
Uso:
  python scripts/setup_latex.py          # pregunta antes de instalar
  python scripts/setup_latex.py --yes    # instala sin preguntar
  python scripts/setup_latex.py --check  # solo verifica

En Windows usa siempre el Python del proyecto:
  .venv\\Scripts\\python.exe scripts\\setup_latex.py --yes
""")
        return

    if is_tectonic_installed():
        if verify_tectonic():
            return
        print("⚠️  Tectonic encontrado pero no funciona. Se reinstalará.")

    if "--check" in sys.argv:
        print("❌ Tectonic no está instalado o no funciona.")
        sys.exit(1)

    auto_confirm = "--yes" in sys.argv or "-y" in sys.argv
    print("ℹ️  No se encontró Tectonic (motor LaTeX ligero para generar PDFs).")

    if auto_confirm:
        confirm = "s"
    else:
        confirm = input("¿Quieres instalarlo ahora? (s/n): ").strip().lower()

    if confirm != "s":
        print("⚠️  Instalación cancelada. No se podrán generar PDFs.")
        return

    if install_tectonic_pip():
        verify_tectonic()
        return

    print("⚠️  Pip falló. Intentando descarga directa del binario...")
    if install_tectonic_binary():
        verify_tectonic()
    else:
        print()
        print("❌ No se pudo instalar Tectonic automáticamente.")
        print("   Puedes instalarlo manualmente:")
        print("   • pip install tectonic")
        print("   • https://tectonic-typesetting.github.io/book/latest/installation/")
        sys.exit(1)


if __name__ == "__main__":
    main()
