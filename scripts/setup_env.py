import os
import sys
import subprocess
import argparse

# Configuration
VENV_DIR = ".venv"
REQUIREMENTS_FILE = "requirements.txt"
DEV_REQUIREMENTS_FILE = "requirements-dev.txt"
MIN_PYTHON_VERSION = (3, 7)

def check_python_version():
    """Verifies that the current Python version meets the minimum requirement."""
    if sys.version_info < MIN_PYTHON_VERSION:
        print(f"❌ Error: Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+ is required.")
        print(f"   Current version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        print("   Please install a newer version of Python.")
        sys.exit(1)
    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

def get_venv_python():
    """Returns the path to the Python executable within the virtual environment."""
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "python.exe")
    return os.path.join(VENV_DIR, "bin", "python")

def get_venv_pip():
    """Returns the path to the pip executable within the virtual environment."""
    if os.name == "nt":
        return os.path.join(VENV_DIR, "Scripts", "pip.exe")
    return os.path.join(VENV_DIR, "bin", "pip")

def create_venv():
    """Creates the virtual environment if it doesn't exist."""
    if not os.path.exists(VENV_DIR):
        print(f"📦 Creating virtual environment in '{VENV_DIR}'...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
            print("✅ Virtual environment created.")
        except subprocess.CalledProcessError:
            print("❌ Error creating virtual environment.")
            sys.exit(1)
    else:
        print(f"✅ Virtual environment '{VENV_DIR}' already exists.")

def install_requirements(dev_mode=False):
    """Installs dependencies from requirements.txt into the virtual environment."""
    pip_cmd = get_venv_pip()
    python_cmd = get_venv_python()

    # Upgrade pip first
    try:
        subprocess.check_call([python_cmd, "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("⚠️ Warning: Could not upgrade pip.")

    # 1. Install Production Requirements
    if os.path.exists(REQUIREMENTS_FILE):
        print(f"⬇️  Installing dependencies from '{REQUIREMENTS_FILE}'...")
        try:
            subprocess.check_call([pip_cmd, "install", "-r", REQUIREMENTS_FILE])
            print("✅ Core dependencies installed.")
        except subprocess.CalledProcessError:
            print("❌ Error installing core dependencies.")
            sys.exit(1)
    else:
        print(f"⚠️ Warning: '{REQUIREMENTS_FILE}' not found. Skipping.")

    # 2. Install Dev Requirements (if requested)
    if dev_mode:
        if os.path.exists(DEV_REQUIREMENTS_FILE):
             print(f"🛠️  Dev Mode: Installing dependencies from '{DEV_REQUIREMENTS_FILE}'...")
             try:
                 subprocess.check_call([pip_cmd, "install", "-r", DEV_REQUIREMENTS_FILE])
                 print("✅ Dev dependencies installed.")
                 
                 # 3. Playwright specific setup
                 install_playwright_browsers(python_cmd)

             except subprocess.CalledProcessError:
                 print("❌ Error installing dev dependencies.")
                 sys.exit(1)
        else:
            print(f"⚠️ Warning: '{DEV_REQUIREMENTS_FILE}' not found, but --dev was requested.")

def install_playwright_browsers(python_cmd):
    """Installs Playwright browsers using the venv python."""
    print("🎭 Checking Playwright browser installation...")
    try:
        # Check if we can import playwright
        subprocess.check_call([python_cmd, "-c", "import playwright"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("   Running 'playwright install' (this may take a while)...")
        subprocess.check_call([python_cmd, "-m", "playwright", "install"])
        print("✅ Playwright browsers installed.")
    except subprocess.CalledProcessError:
         print("⚠️  Playwright not found or failed to install browsers. Is it in requirements-dev.txt?")

def verify_installation(dev_mode=False):
    """Lists installed packages to verify the environment."""
    print("\n🔍 Verifying installed packages:")
    pip_cmd = get_venv_pip()
    try:
        result = subprocess.check_output([pip_cmd, "freeze"], text=True)
        # print(result) # Reduced verbosity
        
        # Check for key packages
        required_packages = ["jupyter-book", "sphinx-autobuild", "watchdog"]
        if dev_mode:
            required_packages.append("playwright")

        missing = [pkg for pkg in required_packages if pkg not in result]
        
        if missing:
             print(f"⚠️ Warning: Some key packages seem missing: {missing}")
        else:
             print("✨ All key packages verified.")

    except subprocess.CalledProcessError:
        print("❌ Error verification failed.")

def main():
    parser = argparse.ArgumentParser(description="Setup TeachBook Environment")
    parser.add_argument("--dev", action="store_true", help="Install development tools (Playwright, etc.)")
    args = parser.parse_args()

    print("🛠️  TeachBook Environment Setup")
    print("=============================")
    print(f"Mode: {'Development 🛠️' if args.dev else 'Production 🚀'}")
    
    check_python_version()
    create_venv()
    install_requirements(dev_mode=args.dev)
    verify_installation(dev_mode=args.dev)
    
    print("\n🎉 Setup Complete! Activate the environment with:")
    if os.name == "nt":
        print(f"   {VENV_DIR}\\Scripts\\activate")
    else:
        print(f"   source {VENV_DIR}/bin/activate")

if __name__ == "__main__":
    main()
