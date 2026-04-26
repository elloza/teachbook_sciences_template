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
import time

# Fix: Windows cp1252 can't encode emojis — force UTF-8
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() not in ("utf-8", "utf8"):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


VENV_DIR = ".venv"


def run(cmd, **kwargs):
    """Run a command, showing it for transparent CI logs."""
    printable = " ".join(cmd) if isinstance(cmd, list) else str(cmd)
    print(f"$ {printable}")
    return subprocess.run(cmd, check=True, **kwargs)


def add_github_path(path):
    """Persist a PATH entry for later GitHub Actions steps."""
    github_path = os.environ.get("GITHUB_PATH")
    if github_path and os.path.isdir(path):
        with open(github_path, "a", encoding="utf-8") as f:
            f.write(path + "\n")
        print(f"✅ Añadido a GITHUB_PATH: {path}")


def command_exists(command):
    return shutil.which(command) is not None


def local_binary_candidates(binary_name):
    candidates = []
    venv_bin = get_venv_bin_dir()
    if os.path.isdir(venv_bin):
        candidates.append(os.path.join(venv_bin, binary_name))

    if os.name == "nt":
        appdata = os.environ.get("APPDATA", os.path.expanduser("~"))
        candidates.append(os.path.join(appdata, "teachbook", binary_name))
    else:
        candidates.append(os.path.expanduser(os.path.join("~", ".local", "bin", binary_name)))

    candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), binary_name))
    return candidates


def get_python_launcher():
    return get_effective_python()


def python_module_available(module_name):
    python = get_python_launcher()
    try:
        result = subprocess.run(
            [python, "-c", f"import {module_name}"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
        )
        return result.returncode == 0
    except Exception:
        return False


def pip_available():
    python = get_python_launcher()
    try:
        result = subprocess.run(
            [python, "-m", "pip", "--version"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
        )
        return result.returncode == 0
    except Exception:
        return False


def ensure_pip_available():
    if pip_available():
        return True
    python = get_python_launcher()
    print("🧰 Pip no está disponible en el Python del proyecto. Intentando activarlo...")
    try:
        result = subprocess.run(
            [python, "-m", "ensurepip", "--upgrade"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=180,
        )
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip())
    except Exception as exc:
        print(f"⚠️  No se pudo activar pip automáticamente: {exc}")
        return False
    return pip_available()


def verify_svg_converter():
    resvg = get_resvg_command()
    if resvg:
        print(f"✅ Conversor SVG detectado: {resvg}")
        return True

    converter = shutil.which("rsvg-convert")
    if converter:
        print(f"✅ Conversor SVG detectado: {converter}")
        return True

    if python_module_available("cairosvg"):
        print("✅ CairoSVG disponible en el Python del proyecto.")
        return True

    print("❌ Falta conversor SVG robusto (rsvg-convert o CairoSVG).")
    return False


def install_cairosvg_with_pip():
    if not ensure_pip_available():
        return False

    python = get_python_launcher()
    print("📦 Intentando instalar CairoSVG en el entorno del proyecto...")
    try:
        result = subprocess.run(
            [python, "-m", "pip", "install", "cairosvg"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=900,
        )
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip())
        return result.returncode == 0
    except Exception as exc:
        print(f"⚠️  Falló la instalación de CairoSVG con pip: {exc}")
        return False


def install_svg_converter():
    if verify_svg_converter():
        return True

    print("🖼️  Instalando soporte SVG para PDF con Tectonic...")
    if install_resvg_binary() and verify_svg_converter():
        return True
    if install_cairosvg_with_pip() and verify_svg_converter():
        return True

    system = platform.system().lower()

    if system == "windows" and command_exists("choco"):
        try:
            run(["choco", "install", "librsvg", "gtk-runtime", "-y", "--no-progress"])
            gtk_candidates = [
                r"C:\Program Files\GTK3-Runtime Win64\bin",
                r"C:\Program Files\GTK2-Runtime\bin",
                r"C:\tools\gtk-runtime\bin",
            ]
            for gtk_bin in gtk_candidates:
                if os.path.isdir(gtk_bin):
                    os.environ["PATH"] = gtk_bin + os.pathsep + os.environ.get("PATH", "")
                    add_github_path(gtk_bin)
            return verify_svg_converter()
        except Exception as exc:
            print(f"⚠️  No se pudo instalar librsvg con Chocolatey: {exc}")

    if system == "darwin" and command_exists("brew"):
        try:
            run(["brew", "install", "librsvg", "cairo", "pkg-config"])
            return verify_svg_converter()
        except Exception as exc:
            print(f"⚠️  No se pudo instalar librsvg con Homebrew: {exc}")

    if system == "linux" and (os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS")):
        try:
            apt = ["apt-get"] if os.geteuid() == 0 else ["sudo", "apt-get"]
            run(apt + ["update"])
            run(apt + ["install", "-y", "librsvg2-bin"])
            return verify_svg_converter()
        except Exception as exc:
            print(f"⚠️  No se pudo instalar librsvg en Linux: {exc}")

    print("⚠️  No se pudo dejar listo el conversor SVG automáticamente.")
    print("   El flujo PDF con Tectonic necesita rsvg-convert o CairoSVG para los SVG/Kroki.")
    return False


def verify_full_latex():
    """Verify the advanced fallback PDF toolchain (latexmk + XeLaTeX)."""
    latexmk = shutil.which("latexmk")
    xelatex = shutil.which("xelatex")
    if latexmk and xelatex:
        print("✅ Toolchain LaTeX completa detectada.")
        print(f"   latexmk: {latexmk}")
        print(f"   xelatex: {xelatex}")
        try:
            subprocess.run([xelatex, "--version"], check=False, timeout=15)
        except Exception:
            pass
        return True

    print("❌ Falta toolchain LaTeX completa.")
    print(f"   latexmk: {latexmk or 'NO encontrado'}")
    print(f"   xelatex: {xelatex or 'NO encontrado'}")
    return False


def install_full_latex_ci():
    """Install the advanced XeLaTeX + latexmk fallback toolchain on CI.

    Tectonic remains the default user-facing flow because it is simpler and
    more portable. This installer is kept for explicit fallback scenarios,
    deeper diagnostics, or environments that require a full LaTeX distro.
    """
    print("🔧 Instalando toolchain LaTeX completa AVANZADA para CI/fallback...")
    system = platform.system().lower()

    full_latex_ready = verify_full_latex()

    if full_latex_ready and verify_svg_converter():
        return True

    if system == "linux":
        if os.geteuid() == 0:
            apt = ["apt-get"]
        else:
            apt = ["sudo", "apt-get"]
        run(apt + ["update"])
        run(
            apt
            + [
                "install",
                "-y",
                "latexmk",
                "texlive-xetex",
                "texlive-latex-recommended",
                "texlive-latex-extra",
                "texlive-fonts-recommended",
                "texlive-fonts-extra",
                "texlive-lang-spanish",
                "texlive-lang-english",
                "librsvg2-bin",
                "xindy",
            ]
        )
        return verify_full_latex() and verify_svg_converter()

    if system == "darwin":
        if not command_exists("brew"):
            print("❌ Homebrew no está disponible; no puedo instalar BasicTeX automáticamente.")
            return False
        run(["brew", "install", "librsvg", "cairo", "pkg-config"])
        if not full_latex_ready:
            run(["brew", "install", "--cask", "basictex"])
        texbin = "/Library/TeX/texbin"
        os.environ["PATH"] = texbin + os.pathsep + os.environ.get("PATH", "")
        add_github_path(texbin)
        if not full_latex_ready:
            tlmgr = os.path.join(texbin, "tlmgr")
            run(["sudo", tlmgr, "update", "--self"])
            run(
                [
                    "sudo",
                    tlmgr,
                    "install",
                    "latexmk",
                    "collection-xetex",
                    "collection-latexrecommended",
                    "collection-latexextra",
                    "collection-fontsrecommended",
                    "collection-langspanish",
                    "collection-langenglish",
                    "bbm",
                    "bbm-macros",
                    "xindy",
                ]
            )
        return verify_full_latex() and verify_svg_converter()

    if system == "windows":
        if not command_exists("choco"):
            print("❌ Chocolatey no está disponible; no puedo instalar MiKTeX automáticamente.")
            return False
        packages = [] if verify_svg_converter() else ["gtk-runtime"]
        if not full_latex_ready:
            packages = ["miktex", "strawberryperl"] + packages
        if packages:
            run(["choco", "install", *packages, "-y", "--no-progress"])
        miktex_bin = r"C:\Program Files\MiKTeX\miktex\bin\x64"
        perl_bin = r"C:\Strawberry\perl\bin"
        gtk_candidates = [
            r"C:\Program Files\GTK3-Runtime Win64\bin",
            r"C:\Program Files\GTK2-Runtime\bin",
            r"C:\tools\gtk-runtime\bin",
        ]
        extra_paths = [miktex_bin, perl_bin] + [p for p in gtk_candidates if os.path.isdir(p)]
        os.environ["PATH"] = os.pathsep.join(extra_paths) + os.pathsep + os.environ.get("PATH", "")
        add_github_path(miktex_bin)
        add_github_path(perl_bin)
        for gtk_bin in gtk_candidates:
            add_github_path(gtk_bin)
        initexmf = shutil.which("initexmf")
        if initexmf and not full_latex_ready:
            subprocess.run([initexmf, "--set-config-value", "[MPM]AutoInstall=1"], check=False)
            subprocess.run([initexmf, "--update-fndb"], check=False)
        mpm = shutil.which("mpm")
        if mpm and not full_latex_ready:
            subprocess.run([mpm, "--update-db"], check=False)
            subprocess.run([mpm, "--install=bbm"], check=False)
            subprocess.run([mpm, "--install=bbm-macros"], check=False)
        return verify_full_latex() and verify_svg_converter()

    print(f"❌ Sistema no soportado para instalación CI: {platform.system()}")
    return False


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
    return local_binary_candidates(executable_name)


def local_resvg_candidates():
    executable_name = "resvg.exe" if os.name == "nt" else "resvg"
    return local_binary_candidates(executable_name)


def get_tectonic_command():
    found = shutil.which("tectonic")
    if found:
        return found
    for candidate in local_tectonic_candidates():
        if os.path.isfile(candidate):
            return candidate
    return None


def get_resvg_command():
    found = shutil.which("resvg")
    if found:
        return found
    for candidate in local_resvg_candidates():
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
    python = get_python_launcher()
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
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("tag_name"), data.get("assets", [])
    except Exception as e:
        print(f"❌ Error consultando GitHub API: {e}")
        return None, []


def fetch_latest_release_for_repo(repo_slug):
    api_url = f"https://api.github.com/repos/{repo_slug}/releases/latest"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "teachbook-setup"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("tag_name"), data.get("assets", [])
    except Exception as e:
        print(f"❌ Error consultando GitHub API ({repo_slug}): {e}")
        return None, []


def download_file_with_retries(url, destination, label, attempts=4):
    """Download a release asset with retries and CI-friendly headers."""
    headers = {"User-Agent": "teachbook-setup"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and "github.com" in url:
        headers["Authorization"] = f"Bearer {token}"

    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            print(f"   Descargando {label} (intento {attempt}/{attempts})...")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=120) as resp:
                with open(destination, "wb") as f:
                    shutil.copyfileobj(resp, f)
            if os.path.getsize(destination) > 0:
                return True
            last_error = "archivo descargado vacío"
        except Exception as exc:
            last_error = exc

        if attempt < attempts:
            wait_seconds = min(2 * attempt, 8)
            print(f"   ⚠️  Descarga fallida ({last_error}). Reintentando en {wait_seconds}s...")
            time.sleep(wait_seconds)

    print(f"❌ Error descargando {label}: {last_error}")
    return False


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


def verify_resvg():
    resvg = get_resvg_command()
    if not resvg:
        return False
    try:
        result = subprocess.run(
            [resvg, "--version"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        if result.returncode == 0:
            version = (result.stdout or result.stderr).strip().split("\n")[0]
            print(f"✅ resvg {version} funcionando correctamente.")
            print(f"   Ejecutable: {resvg}")
            return True
    except (subprocess.TimeoutExpired, OSError):
        pass
    print("❌ resvg se instaló pero no se pudo ejecutar.")
    return False


def get_resvg_asset_name(system, arch):
    mapping = {
        ("windows", "amd64"): ("resvg-win64.zip", ".zip"),
        ("darwin", "amd64"): ("resvg-macos-x86_64.zip", ".zip"),
        ("darwin", "arm64"): ("resvg-macos-aarch64.zip", ".zip"),
        ("linux", "amd64"): ("resvg-linux-x86_64.tar.gz", ".tar.gz"),
    }
    return mapping.get((system, arch), (None, None))


def install_resvg_binary():
    print("⬇️  Intentando instalar resvg (conversor SVG portable)...")
    system = platform.system().lower()
    arch = get_arch_tag()
    asset_name, ext = get_resvg_asset_name(system, arch)
    if not asset_name or not ext:
        print(f"⚠️  No hay binario resvg predefinido para {platform.system()} {platform.machine()}.")
        return False

    tag_name, assets = fetch_latest_release_for_repo("linebender/resvg")
    if not tag_name or not assets:
        print("❌ No se pudo obtener la última release de resvg.")
        return False

    asset = next((item for item in assets if item.get("name") == asset_name), None)
    if not asset:
        print(f"❌ No se encontró el asset {asset_name} en la release {tag_name}.")
        return False

    download_url = asset.get("browser_download_url")
    install_dir = get_binary_install_dir()
    executable_name = "resvg.exe" if system == "windows" else "resvg"

    with tempfile.TemporaryDirectory(prefix="resvg_") as tmp:
        archive_path = os.path.join(tmp, asset_name)
        extract_dir = os.path.join(tmp, "extracted")
        os.makedirs(extract_dir, exist_ok=True)

        if not download_file_with_retries(download_url, archive_path, asset_name):
            return False

        try:
            if ext == ".zip":
                with zipfile.ZipFile(archive_path, "r") as zf:
                    zf.extractall(extract_dir)
            else:
                with tarfile.open(archive_path, "r:gz") as tf:
                    tf.extractall(extract_dir)
        except Exception as e:
            print(f"❌ Error extrayendo resvg: {e}")
            return False

        extracted_bin = os.path.join(extract_dir, executable_name)
        if not os.path.isfile(extracted_bin):
            for root, dirs, files in os.walk(extract_dir):
                if executable_name in files:
                    extracted_bin = os.path.join(root, executable_name)
                    break

        if not os.path.isfile(extracted_bin):
            print("❌ No se encontró el ejecutable de resvg dentro del archivo descargado.")
            return False

        dest_path = os.path.join(install_dir, executable_name)
        shutil.copy2(extracted_bin, dest_path)
        if system != "windows":
            st = os.stat(dest_path)
            os.chmod(dest_path, st.st_mode | stat.S_IEXEC)

    print(f"✅ resvg instalado en: {dest_path}")
    if os.path.abspath(install_dir) == os.path.abspath(get_venv_bin_dir()):
        print("   Instalado dentro de .venv: no hace falta tocar el PATH global.")
    return verify_resvg()


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

    install_dir = get_binary_install_dir()
    with tempfile.TemporaryDirectory(prefix="tectonic_") as tmp:
        archive_path = os.path.join(tmp, asset_name)

        if not download_file_with_retries(download_url, archive_path, asset_name):
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
  python scripts/setup_latex.py            # pregunta antes de instalar Tectonic
  python scripts/setup_latex.py --yes      # instala Tectonic sin preguntar
  python scripts/setup_latex.py --check    # solo verifica Tectonic
  python scripts/setup_latex.py --ci-full  # instala latexmk + XeLaTeX como fallback avanzado
  python scripts/setup_latex.py --check-full # verifica el fallback avanzado

En Windows usa siempre el Python del proyecto:
  .venv\\Scripts\\python.exe scripts\\setup_latex.py --yes
""")
        return

    if "--ci-full" in sys.argv:
        print("ℹ️  Modo avanzado: instalando fallback completo latexmk + XeLaTeX.")
        if install_full_latex_ci():
            return
        sys.exit(1)

    if "--check-full" in sys.argv:
        if verify_full_latex():
            return
        sys.exit(1)

    if is_tectonic_installed():
        if verify_tectonic():
            if verify_svg_converter():
                return
            print("⚠️  Tectonic está bien, pero falta el conversor SVG necesario para PDF.")
            if "--check" in sys.argv:
                sys.exit(1)
            if install_svg_converter():
                return
            sys.exit(1)
        print("⚠️  Tectonic encontrado pero no funciona. Se reinstalará.")

    if "--check" in sys.argv:
        print("❌ Tectonic no está instalado/no funciona, o falta el conversor SVG.")
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
        if verify_tectonic() and install_svg_converter():
            return

    print("⚠️  Pip falló. Intentando descarga directa del binario...")
    if install_tectonic_binary():
        if verify_tectonic() and install_svg_converter():
            return
        sys.exit(1)
    else:
        print()
        print("❌ No se pudo instalar Tectonic automáticamente.")
        print("   Puedes instalarlo manualmente:")
        print("   • pip install tectonic")
        print("   • https://tectonic-typesetting.github.io/book/latest/installation/")
        sys.exit(1)


if __name__ == "__main__":
    main()
