from gestores.carpeta_gestor import obtener_navegadores
from front.ventana import seleccionar_perfiles


def main():

    datos = obtener_navegadores()

    seleccionar_perfiles(datos)


if __name__ == "__main__":
    main()
