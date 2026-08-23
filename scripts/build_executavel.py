import os
import sys
import subprocess
import shutil

def compilar():
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    main_py = os.path.join(raiz, "main.py")
    icone_ico = os.path.join(raiz, "src", "presentation", "assets", "icons", "app_icon.ico")
    assets_dir = os.path.join(raiz, "src", "presentation", "assets")
    dist_dir = os.path.join(raiz, "dist")
    build_dir = os.path.join(raiz, "build")

    print("[*] Iniciando geracao do executavel...")
    print(f"[*] Diretorio raiz: {raiz}")

    # Garante que o icone ICO existe
    if not os.path.exists(icone_ico):
        from gerar_icone_ico import gerar_ico
        gerar_ico()

    # Comando PyInstaller
    # Sintaxe no Windows: --add-data "origem;destino"
    separador = ";" if sys.platform.startswith("win") else ":"
    add_data_arg = f"{assets_dir}{separador}src/presentation/assets"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--clean",
        "--name", "ValidadorRateLimit",
        "--icon", icone_ico,
        "--add-data", add_data_arg,
        main_py
    ]

    print("[*] Executando comando:")
    print(" ".join(cmd))

    resultado = subprocess.run(cmd, cwd=raiz)
    if resultado.returncode == 0:
        exe_path = os.path.join(dist_dir, "ValidadorRateLimit.exe" if sys.platform.startswith("win") else "ValidadorRateLimit")
        print(f"\n[SUCESSO] Executavel gerado com sucesso!")
        print(f"[ARQUIVO] -> {exe_path}")
        return True
    else:
        print(f"\n[ERRO] Falha na compilacao (codigo {resultado.returncode})")
        return False

if __name__ == "__main__":
    compilar()
