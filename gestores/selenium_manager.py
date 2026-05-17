import os
import time
from seleniumbase import SB
from gestores.sesiones_manager import SesionesManager
from whatsapp.acciones import entrar_a_grupos

def abrir_chrome(perfil):
    ruta = os.path.join("perfiles", "chrome", perfil)
    id_sesion = f"chrome_{perfil}"
    with SB(browser="chrome", uc=True, user_data_dir=ruta) as sb:
        sb.open("https://web.whatsapp.com/")
        print(f"[{id_sesion}] Esperando 15s para cargar WhatsApp...")
        time.sleep(15)
        entrar_a_grupos(sb)
        SesionesManager.registrar_sesion(id_sesion, sb)
        while id_sesion in SesionesManager.obtener_todas():
            time.sleep(2)
        print(f"[{id_sesion}] Sesión finalizada.")

def abrir_firefox(perfil):
    ruta = os.path.join("perfiles", "firefox", perfil)
    id_sesion = f"firefox_{perfil}"
    with SB(browser="firefox", user_data_dir=ruta) as sb:
        sb.open("https://web.whatsapp.com/")
        print(f"[{id_sesion}] Esperando 15s para cargar WhatsApp...")
        time.sleep(15)
        entrar_a_grupos(sb)
        SesionesManager.registrar_sesion(id_sesion, sb)
        while id_sesion in SesionesManager.obtener_todas():
            time.sleep(2)
        print(f"[{id_sesion}] Sesión finalizada.")

def abrir_edge(perfil):
    ruta = os.path.join("perfiles", "edge", perfil)
    id_sesion = f"edge_{perfil}"
    with SB(browser="edge", user_data_dir=ruta) as sb:
        sb.open("https://web.whatsapp.com/")
        print(f"[{id_sesion}] Esperando 15s para cargar WhatsApp...")
        time.sleep(15)
        entrar_a_grupos(sb)
        SesionesManager.registrar_sesion(id_sesion, sb)
        while id_sesion in SesionesManager.obtener_todas():
            time.sleep(2)
        print(f"[{id_sesion}] Sesión finalizada.")

def abrir_perfiles(activos):
    from gestores.thread_manager import NavegadorThread
    threads = []
    for navegador, perfiles in activos.items():
        for perfil in perfiles:
            print(f"Abriendo en thread -> {navegador} -> {perfil}")
            hilo = NavegadorThread(navegador, perfil)
            hilo.start()
            threads.append(hilo)