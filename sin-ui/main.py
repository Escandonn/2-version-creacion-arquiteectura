import sys
import os

# Asegurar que el directorio raíz está en el path de Python
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from Ui.gui_app import lanzar_gui

def main():
    # Lanzar la aplicación gráfica de escritorio premium con PyQt5
    lanzar_gui()

if __name__ == "__main__":
    # Activar la compatibilidad con códigos ANSI de Windows PowerShell si es necesario
    if sys.platform == "win32":
        os.system("")
    main()