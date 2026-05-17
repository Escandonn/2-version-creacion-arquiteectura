import time
import os
import threading
from carpeta_gestor import obtener_navegadores
from bot_sb import WhatsappBot

# Diccionario para guardar las instancias de bots activos
bots_activos = {}

def lanzar_bot(navegador, perfil):
    id_sesion = f"{navegador}_{perfil}"
    ruta = os.path.join("perfiles", navegador, perfil)
    bot = WhatsappBot(navegador=navegador, user_data_dir=ruta)
    bots_activos[id_sesion] = bot
    
    try:
        bot.run()
    except Exception as e:
        print(f"Error en {id_sesion}: {e}")
    finally:
        if id_sesion in bots_activos:
            del bots_activos[id_sesion]

def enviar_mensaje_paralelo(bot, grupo, mensaje):
    try:
        print(f"[{bot.user_data_dir}] Buscando grupo '{grupo}'...")
        bot.entrar_a_chat(grupo)
        print(f"[{bot.user_data_dir}] Enviando mensaje...")
        bot.escribir_y_enviar_mensaje(mensaje)
    except Exception as e:
        print(f"[{bot.user_data_dir}] Error en envío: {e}")

def main():
    print("INICIANDO BOT DE WHATSAPP (VERSIÓN CONSOLA - MULTI-PERFIL)")
    datos = obtener_navegadores()
    
    opciones = []
    i = 1
    for nav, perfiles in datos.items():
        for p in perfiles:
            opciones.append((nav, p))
            print(f"{i}. {nav.upper()} -> {p}")
            i += 1
            
    if not opciones:
        print("No se detectaron perfiles en la carpeta 'perfiles'. Por favor ejecuta el script principal o crea las carpetas.")
        return
        
    seleccion = input("\nSelecciona los números de perfiles a abrir (separados por coma, ej: 1,2) o escribe 'todos': ")
    seleccionados = []
    if seleccion.lower() == 'todos':
        seleccionados = opciones
    else:
        indices = [int(x.strip()) for x in seleccion.split(",") if x.strip().isdigit()]
        for idx in indices:
            if 1 <= idx <= len(opciones):
                seleccionados.append(opciones[idx-1])
                
    if not seleccionados:
        print("Ningún perfil seleccionado. Saliendo...")
        return
        
    print(f"\nIniciando {len(seleccionados)} perfiles en paralelo...")
    for nav, p in seleccionados:
        t = threading.Thread(target=lanzar_bot, args=(nav, p), daemon=True)
        t.start()
        
    # Dar tiempo a que los hilos se inicialicen y no pisen el menú de inmediato
    time.sleep(2) 
    
    while True:
        if not bots_activos:
            print("\nEsperando a que las sesiones de WhatsApp se abran y estén listas...")
            time.sleep(3)
            if not bots_activos:
                continue
            
        print("\n=== MENÚ MAESTRO ===")
        print("1. Entrar a la pestaña Grupos (en todos)")
        print("2. Imprimir títulos de grupos (en todos)")
        print("3. Enviar mensaje (Grupos distintos por perfil)")
        print("4. Enviar mensaje (Mismo grupo para todos)")
        print("5. Salir")
        
        op = input("Elige una opción: ")
        
        if op == "1":
            bots_ready = [b for b in bots_activos.values() if b.ready]
            if not bots_ready:
                print("\nNingún perfil de WhatsApp está listo todavía. Espera a que se muestre '[perfil] LISTO PARA COMANDOS'.")
                continue
            for bot in bots_ready:
                threading.Thread(target=bot.entrar_a_grupos, daemon=True).start()
        elif op == "2":
            bots_ready = [b for b in bots_activos.values() if b.ready]
            if not bots_ready:
                print("\nNingún perfil de WhatsApp está listo todavía. Espera a que se muestre '[perfil] LISTO PARA COMANDOS'.")
                continue
            for bot in bots_ready:
                threading.Thread(target=bot.obtener_titulos_grupos, daemon=True).start()
        elif op == "3":
            bots_ready = {id_s: b for id_s, b in bots_activos.items() if b.ready}
            if not bots_ready:
                print("\nNingún perfil de WhatsApp está listo todavía. Espera a que se muestre '[perfil] LISTO PARA COMANDOS'.")
                continue
            configuraciones = []
            for id_s, bot in bots_ready.items():
                print(f"\nConfigurando [{id_s}]:")
                g = input("  Nombre del grupo al que debe ir este perfil: ")
                m = input("  Mensaje a enviar desde este perfil: ")
                if g and m:
                    configuraciones.append((bot, g, m))
                
            if configuraciones:
                print("\nIniciando envío independiente en paralelo...")
                for bot, g, m in configuraciones:
                    threading.Thread(target=enviar_mensaje_paralelo, args=(bot, g, m), daemon=True).start()
                
        elif op == "4":
            bots_ready = [b for b in bots_activos.values() if b.ready]
            if not bots_ready:
                print("\nNingún perfil de WhatsApp está listo todavía. Espera a que se muestre '[perfil] LISTO PARA COMANDOS'.")
                continue
            g = input("\nNombre del grupo común: ")
            m = input("Mensaje común a enviar: ")
            if g and m:
                for bot in bots_ready:
                    threading.Thread(target=enviar_mensaje_paralelo, args=(bot, g, m), daemon=True).start()
                
        elif op == "5":
            print("Cerrando todas las sesiones...")
            for bot in bots_activos.values():
                bot.is_running = False
            time.sleep(2)
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()