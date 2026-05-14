import os
from seleniumbase import SB


def abrir_chrome(perfil):

    ruta = os.path.join(
        "perfiles",
        "chrome",
        perfil
    )

    with SB(
        browser="chrome",
        uc=True,
        user_data_dir=ruta
    ) as sb:

        sb.open("https://google.com")

        sb.sleep(999)


def abrir_firefox(perfil):

    ruta = os.path.join(
        "perfiles",
        "firefox",
        perfil
    )

    with SB(
        browser="firefox",
        user_data_dir=ruta
    ) as sb:

        sb.open("https://google.com")

        sb.sleep(999)


def abrir_edge(perfil):

    ruta = os.path.join(
        "perfiles",
        "edge",
        perfil
    )

    with SB(
        browser="edge",
        user_data_dir=ruta
    ) as sb:

        sb.open("https://google.com")

        sb.sleep(999)


def abrir_perfiles(activos):

    from gestores.thread_manager import NavegadorThread

    threads = []

    for navegador, perfiles in activos.items():

        for perfil in perfiles:

            print(f"Abriendo en thread -> {navegador} -> {perfil}")

            hilo = NavegadorThread(
                navegador,
                perfil
            )

            hilo.start()

            threads.append(hilo)