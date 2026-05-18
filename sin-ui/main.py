import sys
import os

# Asegurar que el directorio raíz está en el path de Python
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from Ui.dashboard import mostrar_dashboard_principal

def main():
    # Lanzar el Panel de Control y Dashboard principal integrado con SQLite
    mostrar_dashboard_principal()

if __name__ == "__main__":
    # Activar la compatibilidad con códigos ANSI de Windows PowerShell si es necesario
    if sys.platform == "win32":
        os.system("")
    main()