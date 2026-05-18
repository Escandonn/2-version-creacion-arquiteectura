import os
import sys
import time
import threading
from datetime import datetime

# Añadir directorio raíz al path de Python para importar correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from base_de_datos import db_manager
from carpeta_gestor import obtener_navegadores
from bot_sb import WhatsappBot

# Colores ANSI para diseño premium
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

def dibujar_cabecera():
    limpiar_pantalla()
    print(f"{CYAN}{BOLD}================================================================================{RESET}")
    print(f"{CYAN}{BOLD}       [BOT]  WHATSAPP MULTI-PERFIL - PANEL DE CONTROL Y ESTADISTICAS  [BOT]     {RESET}")
    print(f"{CYAN}{BOLD}================================================================================{RESET}")

def formatear_tabla(columnas, filas, anchos=None):
    """
    Dibuja una tabla ASCII con bordes estándar compatibles 100% con Windows.
    Las filas deben ser listas o tuplas de valores.
    """
    if not anchos:
        anchos = [len(col) for col in columnas]
        for fila in filas:
            for i, val in enumerate(fila):
                anchos[i] = max(anchos[i], len(str(val)))
    
    # Línea superior
    print(f"{CYAN}+" + "+".join("-" * (w + 2) for w in anchos) + f"+{RESET}")
    # Cabecera
    print(f"{CYAN}|{RESET}" + f"{CYAN}|{RESET}".join(f" {BOLD}{col.ljust(w)}{RESET} " for col, w in zip(columnas, anchos)) + f"{CYAN}|{RESET}")
    # Separador
    print(f"{CYAN}+" + "+".join("-" * (w + 2) for w in anchos) + f"+{RESET}")
    # Filas
    if not filas:
        mensaje = "Sin registros."
        ancho_total = sum(anchos) + 2 * (len(anchos) - 1) + 2
        print(f"{CYAN}|{RESET} {mensaje.ljust(ancho_total - 2)} {CYAN}|{RESET}")
    else:
        for fila in filas:
            elementos = []
            for val, w in zip(fila, anchos):
                val_str = str(val)
                # Acortar si supera el ancho asignado
                if len(val_str) > w:
                    val_str = val_str[:w-3] + "..."
                elementos.append(f" {val_str.ljust(w)} ")
            print(f"{CYAN}|{RESET}" + f"{CYAN}|{RESET}".join(elementos) + f"{CYAN}|{RESET}")
    # Línea inferior
    print(f"{CYAN}+" + "+".join("-" * (w + 2) for w in anchos) + f"+{RESET}")

# ==========================================
# VISTAS DE TABLAS
# ==========================================

def mostrar_tabla_perfiles():
    print(f"\n{GREEN}{BOLD}--- PERFILES REGISTRADOS EN BASE DE DATOS ---{RESET}")
    perfiles = db_manager.obtener_perfiles()
    
    columnas = ["ID", "Ruta de Perfil (Fisica)", "Nombre WhatsApp", "Correo", "Personalidad", "IA"]
    filas = []
    for p in perfiles:
        filas.append([
            p["id"],
            p["nombre_profile"],
            p["nombre_real_whatsapp"] or "N/A",
            p["correo"] or "N/A",
            p["personalidad"] or "Asistente",
            p["ia"] or "Desactivada"
        ])
    formatear_tabla(columnas, filas, anchos=[4, 30, 20, 20, 20, 12])

def mostrar_tabla_grupos():
    print(f"\n{GREEN}{BOLD}--- GRUPOS REGISTRADOS EN BASE DE DATOS ---{RESET}")
    grupos = db_manager.obtener_grupos()
    
    columnas = ["ID", "Nombre de Grupo", "Ultimo Mensaje Enviado", "Fecha Envio"]
    filas = []
    for g in grupos:
        filas.append([
            g["id"],
            g["nombre"],
            g["ultimo_mensaje"] or "Ninguno",
            g["ultimo_mensaje_fecha"] or "Nunca"
        ])
    formatear_tabla(columnas, filas, anchos=[4, 30, 35, 20])

def mostrar_reporte_estadisticas():
    dibujar_cabecera()
    print(f"\n{GREEN}{BOLD}*** REPORTE GLOBAL DE ESTADISTICAS (MENSAJES ENVIADOS POR PERFIL) ***{RESET}")
    stats = db_manager.obtener_estadisticas_globales()
    
    columnas = ["Perfil", "Grupo de Destino", "Mensajes", "Ultimo Mensaje", "Fecha y Hora"]
    filas = []
    for s in stats:
        filas.append([
            s["nombre_real_whatsapp"],
            s["nombre_grupo"],
            s["mensajes_enviados"],
            s["ultimo_mensaje_enviado"] or "N/A",
            s["ultimo_envio_fecha"] or "N/A"
        ])
    formatear_tabla(columnas, filas, anchos=[20, 25, 10, 30, 20])
    input(f"\n{YELLOW}Presiona ENTER para volver al Panel Principal...{RESET}")

def mostrar_relacion_perfil_grupo():
    print(f"\n{GREEN}{BOLD}--- GRUPOS ASOCIADOS POR PERFIL (MANY-TO-MANY) ---{RESET}")
    relaciones = db_manager.obtener_perfil_con_grupos()
    
    columnas = ["ID", "Perfil (Nombre WhatsApp)", "Ruta Carpeta", "Grupos Asociados"]
    filas = []
    for r in relaciones:
        filas.append([
            r["perfil_id"],
            r["nombre_real_whatsapp"] or "Temp Profile",
            r["nombre_profile"],
            r["grupos_asociados"] or "(Ninguno - No asociado)"
        ])
    formatear_tabla(columnas, filas, anchos=[4, 25, 25, 45])

# ==========================================
# FORMULARIOS DE REGISTRO
# ==========================================

def formulario_crear_perfil():
    dibujar_cabecera()
    print(f"\n{GREEN}{BOLD}[+] REGISTRAR NUEVO PERFIL DE WHATSAPP [+]{RESET}")
    print("Ingresa los datos para registrar un perfil en la Base de Datos:")
    
    nombre_profile = input(f"\n1. Ruta de Carpeta/Perfil (ej: perfiles/chrome/Profile 3): ").strip()
    if not nombre_profile:
        print(f"{RED}Error: La ruta del perfil no puede estar vacia.{RESET}")
        time.sleep(2)
        return
        
    nombre_real = input("2. Nombre Real/Visual de WhatsApp (ej: Mi Bot Personal): ").strip()
    correo = input("3. Correo Electronico: ").strip()
    contrasena = input("4. Contrasena: ").strip()
    personalidad = input("5. Personalidad de IA (ej: Amistosa, Profesional, Gracioso): ").strip()
    ia = input("6. Modelo de IA a usar (ej: GPT-4o, Claude-3.5, Gemini): ").strip()
    
    exito = db_manager.agregar_perfil(
        nombre_profile=nombre_profile,
        nombre_real=nombre_real if nombre_real else None,
        correo=correo if correo else None,
        contrasena=contrasena if contrasena else None,
        personalidad=personalidad if personalidad else None,
        ia=ia if ia else None
    )
    if exito:
        print(f"\n{GREEN}[OK] Perfil registrado exitosamente en la base de datos.{RESET}")
    time.sleep(2)

def formulario_crear_grupo():
    dibujar_cabecera()
    print(f"\n{GREEN}{BOLD}[+] REGISTRAR NUEVO GRUPO DE WHATSAPP [+]{RESET}")
    
    nombre = input(f"\nIngresa el nombre del grupo de WhatsApp tal como aparece en la aplicacion: ").strip()
    if not nombre:
        print(f"{RED}Error: El nombre del grupo no puede estar vacio.{RESET}")
        time.sleep(2)
        return
        
    exito = db_manager.agregar_grupo(nombre)
    if exito:
        print(f"\n{GREEN}[OK] Grupo '{nombre}' registrado exitosamente en la base de datos.{RESET}")
    time.sleep(2)

def formulario_asociar_perfil_grupo():
    dibujar_cabecera()
    print(f"\n{GREEN}{BOLD}[*] ASOCIAR PERFIL CON GRUPO (RELACION MANY-TO-MANY) [*]{RESET}")
    
    mostrar_tabla_perfiles()
    mostrar_tabla_grupos()
    
    try:
        perfil_id = int(input(f"\nSelecciona el ID del Perfil: "))
        grupo_id = int(input("Selecciona el ID del Grupo: "))
        
        exito = db_manager.asociar_perfil_con_grupo(perfil_id, grupo_id)
        if exito:
            print(f"\n{GREEN}[OK] Asociacion registrada correctamente. El perfil ahora esta vinculado al grupo.{RESET}")
    except ValueError:
        print(f"{RED}Error: Debes ingresar IDs validos (numeros enteros).{RESET}")
    except Exception as e:
        print(f"{RED}Error al realizar asociacion: {e}{RESET}")
    time.sleep(2)

def formulario_editar_perfil():
    dibujar_cabecera()
    print(f"\n{GREEN}{BOLD}[*] EDITAR CONFIGURACION DE PERFIL [*]{RESET}")
    mostrar_tabla_perfiles()
    
    try:
        perfil_id = int(input(f"\nSelecciona el ID del Perfil a editar: "))
        perfiles = db_manager.obtener_perfiles()
        perfil_sel = next((p for p in perfiles if p["id"] == perfil_id), None)
        
        if not perfil_sel:
            print(f"{RED}Error: Perfil no encontrado.{RESET}")
            time.sleep(2)
            return
            
        print(f"\nEditando perfil: {BOLD}{perfil_sel['nombre_profile']}{RESET}")
        print("(Deja en blanco para conservar el valor actual)")
        
        nombre_real = input(f"Nombre WhatsApp [{perfil_sel['nombre_real_whatsapp']}]: ").strip()
        correo = input(f"Correo [{perfil_sel['correo']}]: ").strip()
        contrasena = input(f"Contrasena [{perfil_sel['contrasena']}]: ").strip()
        personalidad = input(f"Personalidad [{perfil_sel['personalidad']}]: ").strip()
        ia = input(f"IA [{perfil_sel['ia']}]: ").strip()
        
        # Conservar valores si se ingreso vacio
        nombre_real = nombre_real if nombre_real else perfil_sel['nombre_real_whatsapp']
        correo = correo if correo else perfil_sel['correo']
        contrasena = contrasena if contrasena else perfil_sel['contrasena']
        personalidad = personalidad if personalidad else perfil_sel['personalidad']
        ia = ia if ia else perfil_sel['ia']
        
        exito = db_manager.actualizar_perfil(perfil_id, nombre_real, correo, contrasena, personalidad, ia)
        if exito:
            print(f"\n{GREEN}[OK] Perfil actualizado exitosamente en la base de datos.{RESET}")
    except ValueError:
        print(f"{RED}Error: Debes ingresar un ID numerico.{RESET}")
    time.sleep(2)

# ==========================================
# MENU MAESTRO EN EJECUCION (AUTOMATIZACION)
# ==========================================

bots_activos = {}

def lanzar_hilo_bot(navegador, perfil, user_data_dir):
    id_sesion = f"{navegador}_{perfil}"
    bot = WhatsappBot(navegador=navegador, user_data_dir=user_data_dir)
    bots_activos[id_sesion] = bot
    
    try:
        bot.run()
    except Exception as e:
        print(f"\n{RED}Error en {id_sesion}: {e}{RESET}")
    finally:
        if id_sesion in bots_activos:
            del bots_activos[id_sesion]

def panel_lanzar_bots():
    dibujar_cabecera()
    print(f"\n{GREEN}{BOLD}[*] LANZAMIENTO CONTROLADO DE BOTS DE WHATSAPP [*]{RESET}")
    
    # 1. Obtener y mostrar perfiles de la DB
    perfiles = db_manager.obtener_perfiles()
    if not perfiles:
        print(f"{RED}No hay perfiles registrados en la Base de Datos.{RESET}")
        time.sleep(2)
        return
        
    columnas = ["Opcion", "Ruta de Perfil", "Nombre WhatsApp", "IA", "Personalidad"]
    filas = []
    for idx, p in enumerate(perfiles, 1):
        filas.append([
            idx,
            p["nombre_profile"],
            p["nombre_real_whatsapp"] or "N/A",
            p["ia"] or "N/A",
            p["personalidad"] or "N/A"
        ])
    formatear_tabla(columnas, filas, anchos=[8, 30, 20, 15, 20])
    
    seleccion = input(f"\nSelecciona los numeros de perfiles a abrir (separados por coma, ej: 1,2) o escribe 'todos': ").strip()
    if not seleccion:
        return
        
    perfiles_a_lanzar = []
    if seleccion.lower() == "todos":
        perfiles_a_lanzar = perfiles
    else:
        try:
            indices = [int(i.strip()) - 1 for i in seleccion.split(",")]
            for idx in indices:
                if 0 <= idx < len(perfiles):
                    perfiles_a_lanzar.append(perfiles[idx])
        except ValueError:
            print(f"{RED}Seleccion invalida.{RESET}")
            time.sleep(2)
            return

    if not perfiles_a_lanzar:
        print(f"{RED}No se selecciono ningun perfil valido.{RESET}")
        time.sleep(2)
        return

    print(f"\nIniciando {len(perfiles_a_lanzar)} perfiles en paralelo...")
    
    # Iniciar los hilos para cada bot seleccionado
    for p in perfiles_a_lanzar:
        ruta = p["nombre_profile"]
        # Obtener navegador a partir de la ruta del perfil (ej: perfiles/chrome/Profile 1)
        partes = ruta.replace("\\", "/").split("/")
        navegador = "chrome"
        perfil_nombre = "Profile 1"
        if len(partes) >= 3:
            navegador = partes[1]
            perfil_nombre = partes[2]
            
        t = threading.Thread(
            target=lanzar_hilo_bot, 
            args=(navegador, perfil_nombre, ruta),
            daemon=True
        )
        t.start()
        
    # Dar unos segundos para iniciar los navegadores en hilos de fondo
    time.sleep(2)

    # Entrar en el Bucle del Menú Maestro
    while True:
        print(f"\n{CYAN}{BOLD}=== MENU MAESTRO (BOTS EN PARALELO) ==={RESET}")
        print("1. Entrar a la pestaña Grupos (en todos los bots listos)")
        print("2. Imprimir títulos de grupos (en todos los bots listos)")
        print("3. Enviar mensaje (Grupos distintos por perfil, según asociación DB)")
        print("4. Enviar mensaje (Mismo grupo para todos)")
        print("5. Detener todos los bots y volver al Panel Principal")
        
        op = input(f"{YELLOW}Elige una opción: {RESET}").strip()
        
        # Filtrar solo bots que se encuentren listos
        bots_listos = {k: v for k, v in bots_activos.items() if v.ready}
        
        if op in ["1", "2", "3", "4"] and not bots_listos:
            print(f"\n{RED}Ningún perfil de WhatsApp está listo todavía. Espera a que se muestre '[perfil] LISTO PARA COMANDOS'.{RESET}")
            continue
            
        if op == "1":
            print(f"\n{GREEN}Enviando comando para entrar a la pestaña Grupos...{RESET}")
            for name, bot in bots_listos.items():
                t_job = threading.Thread(target=bot.entrar_a_grupos)
                t_job.start()
                
        elif op == "2":
            print(f"\n{GREEN}Enviando comando para obtener títulos de grupos...{RESET}")
            for name, bot in bots_listos.items():
                t_job = threading.Thread(target=bot.obtener_titulos_grupos)
                t_job.start()
                
        elif op == "3":
            # Grupos distintos por perfil. Buscamos en la base de datos a qué grupos está asociado cada perfil
            print(f"\n{GREEN}Enviando mensajes personalizados según asociaciones de la Base de Datos...{RESET}")
            
            # Consultamos la relación de perfiles y grupos
            relaciones = db_manager.obtener_perfil_con_grupos()
            
            for name, bot in list(bots_listos.items()):
                # Buscar el registro del perfil actual en la base de datos
                rel_perfil = next((r for r in relaciones if r["nombre_profile"] == bot.user_data_dir), None)
                
                if not rel_perfil or not rel_perfil["grupos_asociados"]:
                    print(f"{RED}[{bot.user_data_dir}] Error: Este perfil no tiene grupos asociados en la base de datos.{RESET}")
                    continue
                
                # Tomar los nombres de grupos (soporta múltiples separados por coma, enviará al primero por defecto)
                grupos = [g.strip() for g in rel_perfil["grupos_asociados"].split(",")]
                grupo_destino = grupos[0]
                
                # Crear personalidad o mensaje basado en la DB
                personalidad = "Asistente"
                perfiles_db = db_manager.obtener_perfiles()
                p_db = next((p for p in perfiles_db if p["nombre_profile"] == bot.user_data_dir), None)
                if p_db and p_db["personalidad"]:
                    personalidad = p_db["personalidad"]
                
                mensaje = f"Hola, este es un mensaje automático de control. Personalidad: {personalidad}."
                
                # Función secuencial en un hilo secundario para no bloquear el menú
                def job_envio_personalizado(b=bot, g=grupo_destino, msg=mensaje):
                    b.entrar_a_chat(g)
                    time.sleep(2)
                    b.escribir_y_enviar_mensaje(msg)
                
                t_job = threading.Thread(target=job_envio_personalizado)
                t_job.start()
                
        elif op == "4":
            grupo = input(f"\n{YELLOW}Digita el nombre exacto del grupo: {RESET}").strip()
            mensaje = input(f"{YELLOW}Digita el mensaje a enviar: {RESET}").strip()
            
            if not grupo or not mensaje:
                print(f"{RED}Campos incompletos.{RESET}")
                continue
                
            print(f"\n{GREEN}Enviando mensaje masivo al grupo '{grupo}'...{RESET}")
            for name, bot in list(bots_listos.items()):
                def job_envio_masivo(b=bot, g=grupo, msg=mensaje):
                    b.entrar_a_chat(g)
                    time.sleep(2)
                    b.escribir_y_enviar_mensaje(msg)
                    
                t_job = threading.Thread(target=job_envio_masivo)
                t_job.start()
                
        elif op == "5":
            print(f"\n{RED}Cerrando todas las sesiones de bots activos...{RESET}")
            for bot in list(bots_activos.values()):
                bot.is_running = False
            time.sleep(3)
            break
        else:
            print(f"{RED}Opción inválida.{RESET}")

# ==========================================
# BUCLE PRINCIPAL DEL DASHBOARD
# ==========================================

def mostrar_dashboard_principal():
    # Inicializar la base de datos y sincronizar perfiles locales físicos
    db_manager.inicializar_base_de_datos()
    
    # Obtener perfiles de la carpeta de disco física e importarlos
    perfiles_disco = obtener_navegadores()
    db_manager.sincronizar_perfiles_desde_disco(perfiles_disco)
    
    while True:
        dibujar_cabecera()
        mostrar_tabla_perfiles()
        mostrar_relacion_perfil_grupo()
        
        print(f"\n{CYAN}{BOLD}--- MENU DE OPERACIONES PRINCIPALES ---{RESET}")
        print("1. Administrar Perfiles (Registrar Nuevo)")
        print("2. Administrar Grupos (Registrar Nuevo)")
        print("3. Asociar Perfil con Grupo (Relacion Many-to-Many)")
        print("4. Editar Datos/Personalidad de Perfil")
        print("5. Ver Reporte de Estadisticas Globales (Mensajes Enviados)")
        print("6. Iniciar Bots y Automatizacion")
        print("7. Salir")
        
        op = input(f"\n{YELLOW}Selecciona una opcion (1-7): {RESET}").strip()
        
        if op == "1":
            formulario_crear_perfil()
        elif op == "2":
            formulario_crear_grupo()
        elif op == "3":
            formulario_asociar_perfil_grupo()
        elif op == "4":
            formulario_editar_perfil()
        elif op == "5":
            mostrar_reporte_estadisticas()
        elif op == "6":
            panel_lanzar_bots()
        elif op == "7":
            print(f"\n{GREEN}¡Gracias por usar WhatsApp Multi-Perfil! Saliendo del sistema...{RESET}")
            sys.exit(0)
        else:
            print(f"{RED}Opción inválida. Reintenta.{RESET}")
            time.sleep(1.5)

if __name__ == "__main__":
    # Activar la compatibilidad con códigos ANSI de Windows PowerShell si es necesario
    if sys.platform == "win32":
        os.system("")
    mostrar_dashboard_principal()
