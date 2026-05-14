import os

RUTA_PERFILES = "perfiles"


NAVS = [
    "chrome",
    "firefox",
    "edge"
]

# perfiles y navegador

PERFILES = {
    
}


def crear_estructura():

    if not os.path.exists(RUTA_PERFILES):
        os.makedirs(RUTA_PERFILES)

    for nav in NAVS:

        ruta = os.path.join(
            RUTA_PERFILES,
            nav
        )

        if not os.path.exists(ruta):
            os.makedirs(ruta)



def obtener_navegadores():

    crear_estructura()

    navegadores = {}

    for navegador in os.listdir(RUTA_PERFILES):

        ruta_navegador = os.path.join(
            RUTA_PERFILES,
            navegador
        )

        if os.path.isdir(ruta_navegador):

            perfiles = []

            for perfil in os.listdir(ruta_navegador):

                ruta_perfil = os.path.join(
                    ruta_navegador,
                    perfil
                )

                if os.path.isdir(ruta_perfil):
                    perfiles.append(perfil)

            navegadores[navegador] = perfiles

    return navegadores