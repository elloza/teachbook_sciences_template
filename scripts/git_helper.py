import subprocess
import sys
import datetime

def run_git(args):
    try:
        subprocess.check_call(["git"] + args)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando: git {' '.join(args)}")
        sys.exit(1)

def main():
    print("🚀 Iniciando proceso de guardado y publicación...")

    # 1. Status
    print("\n📄 Estado actual:")
    run_git(["status", "-s"])

    # 2. Add all changes
    print("\n➕ Añadiendo cambios...")
    run_git(["add", "."])

    # 3. Commit
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"Actualización automática {timestamp}"
    print(f"\n💾 Guardando versión: {message}")
    try:
        run_git(["commit", "-m", message])
    except:
        print("⚠️  No hay cambios para guardar.")
        return

    # 4. Push
    print("\n☁️  Subiendo a GitHub...")
    run_git(["push"])

    print("\n✨ ¡Todo guardado y publicado correctamente!")

if __name__ == "__main__":
    main()
