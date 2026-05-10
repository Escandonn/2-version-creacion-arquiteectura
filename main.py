from gestores.perfiles_manager import obtener_navegadores
from opciones.menu import seleccionar_perfiles
from gestores.selenium_manager import abrir_perfiles


def main():

    datos = obtener_navegadores()

    activos = seleccionar_perfiles(datos)

    abrir_perfiles(activos)


if __name__ == "__main__":
    main()