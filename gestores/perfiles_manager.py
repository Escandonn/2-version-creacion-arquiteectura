import os

RUTA_PERFILES = "perfiles"


def obtener_navegadores():

    navegadores = {}

    if not os.path.exists(RUTA_PERFILES):

        os.makedirs(RUTA_PERFILES)

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