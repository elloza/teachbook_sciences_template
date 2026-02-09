import os
import sys
import subprocess
import shutil

# Configuration
VENV_DIR = ".venv"
REQUIREMENTS_FILE = "requirements.txt"
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

def install_requirements():
    """Installs dependencies from requirements.txt into the virtual environment."""
    if not os.path.exists(REQUIREMENTS_FILE):
        print(f"⚠️ Warning: '{REQUIREMENTS_FILE}' not found. Skipping installation.")
        return

    pip_cmd = get_venv_pip()
    print(f"⬇️  Installing dependencies from '{REQUIREMENTS_FILE}'...")
    
    try:
        # Upgrade pip first
        subprocess.check_call([get_venv_python(), "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL)
        
        # Install requirements
        subprocess.check_call([pip_cmd, "install", "-r", REQUIREMENTS_FILE])
        print("✅ Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print("❌ Error installing dependencies.")
        sys.exit(1)

def verify_installation():
    """Lists installed packages to verify the environment."""
    print("\n🔍 Verifying installed packages:")
    pip_cmd = get_venv_pip()
    try:
        result = subprocess.check_output([pip_cmd, "freeze"], text=True)
        print(result)
        
        # Check for key packages
        required_packages = ["jupyter-book", "sphinx-autobuild", "watchdog"]
        missing = [pkg for pkg in required_packages if pkg not in result]
        
        if missing:
             print(f"⚠️ Warning: Some key packages seem missing from 'pip freeze': {missing}")
        else:
             print("✨ All key packages verified.")

    except subprocess.CalledProcessError:
        print("❌ Error verification failed.")

def main():
    print("🛠️  TeachBook Environment Setup")
    print("=============================")
    
    check_python_version()
    create_venv()
    install_requirements()
    verify_installation()
    
    print("\n🎉 Setup Complete! Active the environment with:")
    if os.name == "nt":
        print(f"   {VENV_DIR}\\Scripts\\activate")
    else:
        print(f"   source {VENV_DIR}/bin/activate")

if __name__ == "__main__":
    main()
