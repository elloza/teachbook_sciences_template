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


def verify_full_latex():
    """Verify the robust PDF toolchain used by Jupyter Book."""
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
    """Install a real XeLaTeX + latexmk toolchain on GitHub Actions.

    This is intentionally heavier than Tectonic.  The full TeachBook has shown
    Tectonic crashes in CI, so CI must use the boring, proven distribution:
    TeX Live on Linux/macOS and MiKTeX on Windows.
    """
    print("🔧 Instalando toolchain LaTeX completa para CI...")
    system = platform.system().lower()

    if verify_full_latex():
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
                "xindy",
            ]
        )
        return verify_full_latex()

    if system == "darwin":
        if not command_exists("brew"):
            print("❌ Homebrew no está disponible; no puedo instalar BasicTeX automáticamente.")
            return False
        run(["brew", "install", "cairo", "pkg-config"])
        run(["brew", "install", "--cask", "basictex"])
        texbin = "/Library/TeX/texbin"
        os.environ["PATH"] = texbin + os.pathsep + os.environ.get("PATH", "")
        add_github_path(texbin)
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
                "xindy",
            ]
        )
        return verify_full_latex()

    if system == "windows":
        if not command_exists("choco"):
            print("❌ Chocolatey no está disponible; no puedo instalar MiKTeX automáticamente.")
            return False
        run(["choco", "install", "miktex", "strawberryperl", "gtk-runtime", "-y", "--no-progress"])
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
        if initexmf:
            subprocess.run([initexmf, "--set-config-value", "[MPM]AutoInstall=1"], check=False)
            subprocess.run([initexmf, "--update-fndb"], check=False)
        mpm = shutil.which("mpm")
        if mpm:
            subprocess.run([mpm, "--update-db"], check=False)
        return verify_full_latex()

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
  python scripts/setup_latex.py --ci-full # instala TeX Live/MiKTeX para CI real

En Windows usa siempre el Python del proyecto:
  .venv\\Scripts\\python.exe scripts\\setup_latex.py --yes
""")
        return

    if "--ci-full" in sys.argv:
        if install_full_latex_ci():
            return
        sys.exit(1)

    if "--check-full" in sys.argv:
        if verify_full_latex():
            return
        sys.exit(1)

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
