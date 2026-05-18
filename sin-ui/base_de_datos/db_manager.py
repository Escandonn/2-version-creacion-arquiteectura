import sqlite3
import os
from datetime import datetime

# Ruta por defecto de la base de datos
DB_DIR = "base_de_datos"
DB_PATH = os.path.join(DB_DIR, "whatsapp_bot.db")

def obtener_conexion():
    """Establece conexión con la base de datos y retorna el objeto de conexión"""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
    # Habilitar soporte para claves foráneas
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def inicializar_base_de_datos():
    """Crea la estructura de tablas de la base de datos si no existe"""
    conn = obtener_conexion()
    cursor = conn.cursor()

    # 1. Tabla de Perfiles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS perfiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_profile TEXT UNIQUE NOT NULL,
        nombre_real_whatsapp TEXT,
        correo TEXT,
        contrasena TEXT,
        personalidad TEXT,
        ia TEXT
    );
    """)

    # 2. Tabla de Grupos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grupos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        ultimo_mensaje TEXT,
        ultimo_mensaje_fecha TEXT
    );
    """)

    # 3. Tabla Relacional Perfil - Grupo (Many-to-Many + Estadísticas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS perfil_grupo (
        perfil_id INTEGER,
        grupo_id INTEGER,
        mensajes_enviados INTEGER DEFAULT 0,
        ultimo_mensaje_enviado TEXT,
        ultimo_envio_fecha TEXT,
        PRIMARY KEY (perfil_id, grupo_id),
        FOREIGN KEY (perfil_id) REFERENCES perfiles (id) ON DELETE CASCADE,
        FOREIGN KEY (grupo_id) REFERENCES grupos (id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print("[Base de Datos] Inicialización completada exitosamente.")

def sincronizar_perfiles_desde_disco(navegadores_dict):
    """
    Sincroniza las carpetas físicas de perfiles detectadas en disco con la base de datos.
    Si encuentra una carpeta que no está registrada, crea el perfil automáticamente.
    """
    conn = obtener_conexion()
    cursor = conn.cursor()

    for navegador, perfiles_lista in navegadores_dict.items():
        for perfil in perfiles_lista:
            # Formato de la ruta física que usa el bot como nombre único de perfil
            ruta_perfil = os.path.join("perfiles", navegador, perfil)
            
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO perfiles (nombre_profile, nombre_real_whatsapp, personalidad, ia) VALUES (?, ?, ?, ?)",
                    (ruta_perfil, f"WhatsApp {navegador.upper()} - {perfil}", "Asistente Estándar", "Desactivada")
                )
            except Exception as e:
                print(f"[Base de Datos] Error al sincronizar perfil '{ruta_perfil}': {e}")

    conn.commit()
    conn.close()

# ==========================================
# MÉTODOS CRUD - PERFILES
# ==========================================

def agregar_perfil(nombre_profile, nombre_real=None, correo=None, contrasena=None, personalidad=None, ia=None):
    """Registra un nuevo perfil en la base de datos"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    exito = False
    try:
        cursor.execute("""
            INSERT INTO perfiles (nombre_profile, nombre_real_whatsapp, correo, contrasena, personalidad, ia)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre_profile, nombre_real, correo, contrasena, personalidad, ia))
        conn.commit()
        exito = True
    except sqlite3.IntegrityError:
        print(f"[Base de Datos] Error: El perfil '{nombre_profile}' ya está registrado.")
    except Exception as e:
        print(f"[Base de Datos] Error al agregar perfil: {e}")
    finally:
        conn.close()
    return exito

def obtener_perfiles():
    """Retorna una lista con todos los perfiles registrados"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM perfiles ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def actualizar_perfil(perfil_id, nombre_real, correo, contrasena, personalidad, ia):
    """Actualiza la información de un perfil existente"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    exito = False
    try:
        cursor.execute("""
            UPDATE perfiles
            SET nombre_real_whatsapp = ?, correo = ?, contrasena = ?, personalidad = ?, ia = ?
            WHERE id = ?
        """, (nombre_real, correo, contrasena, personalidad, ia, perfil_id))
        conn.commit()
        exito = True
    except Exception as e:
        print(f"[Base de Datos] Error al actualizar perfil: {e}")
    finally:
        conn.close()
    return exito

# ==========================================
# MÉTODOS CRUD - GRUPOS
# ==========================================

def agregar_grupo(nombre):
    """Registra un nuevo grupo de WhatsApp"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    exito = False
    try:
        cursor.execute("INSERT INTO grupos (nombre) VALUES (?)", (nombre,))
        conn.commit()
        exito = True
    except sqlite3.IntegrityError:
        print(f"[Base de Datos] Error: El grupo '{nombre}' ya está registrado.")
    except Exception as e:
        print(f"[Base de Datos] Error al agregar grupo: {e}")
    finally:
        conn.close()
    return exito

def obtener_grupos():
    """Retorna una lista con todos los grupos registrados"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grupos ORDER BY nombre ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ==========================================
# ASOCIACIONES Y ESTADÍSTICAS
# ==========================================

def asociar_perfil_con_grupo(perfil_id, grupo_id):
    """Crea una asociación Many-to-Many entre un perfil y un grupo"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    exito = False
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO perfil_grupo (perfil_id, grupo_id)
            VALUES (?, ?)
        """, (perfil_id, grupo_id))
        conn.commit()
        exito = True
    except Exception as e:
        print(f"[Base de Datos] Error al asociar perfil y grupo: {e}")
    finally:
        conn.close()
    return exito

def registrar_mensaje_enviado(nombre_profile, nombre_grupo, mensaje_texto):
    """
    Incrementa el contador de mensajes del perfil para ese grupo,
    y registra la marca de tiempo y último mensaje tanto en la relación como en el grupo.
    """
    conn = obtener_conexion()
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # 1. Obtener los IDs correspondientes
        cursor.execute("SELECT id FROM perfiles WHERE nombre_profile = ?", (nombre_profile,))
        res_perfil = cursor.fetchone()
        
        cursor.execute("SELECT id FROM grupos WHERE nombre = ?", (nombre_grupo,))
        res_grupo = cursor.fetchone()
        
        if not res_perfil or not res_grupo:
            # Si el grupo no está registrado en base de datos, lo creamos para no perder la estadística
            if not res_grupo:
                cursor.execute("INSERT OR IGNORE INTO grupos (nombre) VALUES (?)", (nombre_grupo,))
                cursor.execute("SELECT id FROM grupos WHERE nombre = ?", (nombre_grupo,))
                res_grupo = cursor.fetchone()
            
            if not res_perfil:
                # Si el perfil no existe, lo registramos
                cursor.execute("INSERT OR IGNORE INTO perfiles (nombre_profile, nombre_real_whatsapp, personalidad, ia) VALUES (?, ?, ?, ?)",
                               (nombre_profile, f"Temp Profile", "Asistente", "Desactivada"))
                cursor.execute("SELECT id FROM perfiles WHERE nombre_profile = ?", (nombre_profile,))
                res_perfil = cursor.fetchone()

        perfil_id = res_perfil["id"]
        grupo_id = res_grupo["id"]

        # 2. Asegurar que exista la asociación en la tabla relacional
        cursor.execute("""
            INSERT OR IGNORE INTO perfil_grupo (perfil_id, grupo_id, mensajes_enviados)
            VALUES (?, ?, 0)
        """, (perfil_id, grupo_id))

        # 3. Actualizar estadísticas en la tabla relacional
        cursor.execute("""
            UPDATE perfil_grupo
            SET mensajes_enviados = mensajes_enviados + 1,
                ultimo_mensaje_enviado = ?,
                ultimo_envio_fecha = ?
            WHERE perfil_id = ? AND grupo_id = ?
        """, (mensaje_texto, fecha_actual, perfil_id, grupo_id))

        # 4. Actualizar tabla global de grupos
        cursor.execute("""
            UPDATE grupos
            SET ultimo_mensaje = ?,
                ultimo_mensaje_fecha = ?
            WHERE id = ?
        """, (mensaje_texto, fecha_actual, grupo_id))

        conn.commit()
    except Exception as e:
        print(f"[Base de Datos] Error al registrar estadística de mensaje: {e}")
    finally:
        conn.close()

def obtener_estadisticas_globales():
    """
    Retorna un reporte detallado uniendo las tres tablas:
    perfil, grupo, cantidad de mensajes y detalles del último mensaje enviado.
    """
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = """
        SELECT 
            p.nombre_profile,
            p.nombre_real_whatsapp,
            g.nombre AS nombre_grupo,
            pg.mensajes_enviados,
            pg.ultimo_mensaje_enviado,
            pg.ultimo_envio_fecha
        FROM perfil_grupo pg
        JOIN perfiles p ON pg.perfil_id = p.id
        JOIN grupos g ON pg.grupo_id = g.id
        ORDER BY pg.ultimo_envio_fecha DESC, pg.mensajes_enviados DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def obtener_perfil_con_grupos():
    """Retorna una lista con la relación de qué grupos están asociados a qué perfiles"""
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = """
        SELECT 
            p.id AS perfil_id,
            p.nombre_real_whatsapp,
            p.nombre_profile,
            GROUP_CONCAT(g.nombre, ', ') AS grupos_asociados
        FROM perfiles p
        LEFT JOIN perfil_grupo pg ON p.id = pg.perfil_id
        LEFT JOIN grupos g ON pg.grupo_id = g.id
        GROUP BY p.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
