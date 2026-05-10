from gestores.carpeta_gestor import obtener_navegadores
from opciones.menu import seleccionar_perfiles


def main():

    datos = obtener_navegadores()

    seleccionar_perfiles(datos)


if __name__ == "__main__":
    main()
