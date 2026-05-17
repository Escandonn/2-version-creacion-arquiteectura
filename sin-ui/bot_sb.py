from seleniumbase import SB
from selenium.webdriver.common.by import By
import time
import threading
from ui_selectors import WhatsappSelectors

class WhatsappBot:
    def __init__(self, navegador="chrome", user_data_dir=r"perfiles/chrome/Profile 1"):
        self.navegador = navegador
        self.user_data_dir = user_data_dir
        self.sb = None
        self.is_running = True
        self.ready = False
        self.lock = threading.Lock()

    def run(self):
        # Usamos uc=False para garantizar la máxima estabilidad con perfiles Chrome en este sistema
        with SB(
            browser=self.navegador,
            uc=False,
            headed=True,
            user_data_dir=self.user_data_dir,
        ) as sb:
            self.sb = sb
            self.sb.open("https://web.whatsapp.com/")

            print(f"[{self.user_data_dir}] ESPERANDO WHATSAPP...")
            time.sleep(15)
            self.ready = True
            print(f"[{self.user_data_dir}] LISTO PARA COMANDOS.")
            
            # Mantener la sesión viva
            while self.is_running:
                time.sleep(1)

    # ELIMINADO: iniciar_menu_interactivo para evitar bloqueos en consola

    def entrar_a_grupos(self):
        """Busca y hace clic en la pestaña de 'Grupos'"""
        if not self.ready:
            print(f"[{self.user_data_dir}] Error: El bot aún no está listo.")
            return
        
        with self.lock:
            print(f"\n[{self.user_data_dir}] ENTRANDO A GRUPOS...")
            
            selectores_grupos = [
                '//span[text()="Grupos"]',
                '//span[contains(text(), "Grupos")]',
                '//button[.//span[contains(text(), "Grupos")]]',
                '//div[@role="button" and .//span[contains(text(), "Grupos")]]',
                '//span[@title="Grupos"]'
            ]
            
            try:
                elemento_grupos = None
                for sel in selectores_grupos:
                    try:
                        elementos = self.sb.driver.find_elements(By.XPATH, sel)
                        for e in elementos:
                            txt = e.text.strip().lower()
                            title = e.get_attribute("title")
                            title_str = title.lower() if title else ""
                            if "grupos" in txt or "grupos" in title_str:
                                elemento_grupos = e
                                break
                        if elemento_grupos:
                            break
                    except Exception:
                        pass

                if elemento_grupos:
                    self.sb.execute_script("arguments[0].scrollIntoView(true);", elemento_grupos)
                    time.sleep(1)
                    
                    # Intentar clic nativo o clic por JS
                    try:
                        elemento_grupos.click()
                    except Exception:
                        self.sb.execute_script("arguments[0].click();", elemento_grupos)
                    
                    print(f"[{self.user_data_dir}] Click en pestaña Grupos realizado.")
                    return
                print(f"[{self.user_data_dir}] No se encontró el botón de Grupos.")
            except Exception as e:
                print(f"[{self.user_data_dir}] Error al entrar a grupos: {e}")

    def obtener_titulos_grupos(self):
        """Extrae e imprime los títulos de los grupos mostrados en pantalla"""
        if not self.ready:
            print(f"[{self.user_data_dir}] Error: El bot aún no está listo.")
            return

        with self.lock:
            print(f"\n[{self.user_data_dir}] OBTENIENDO TÍTULOS DE LOS GRUPOS...")
            time.sleep(2) # Esperar a que los grupos carguen en la interfaz

            try:
                titulos_elementos = self.sb.driver.find_elements(
                    By.XPATH, 
                    WhatsappSelectors.TITULOS_GRUPOS
                )
                
                if titulos_elementos:
                    print(f"[{self.user_data_dir}] SE ENCONTRARON {len(titulos_elementos)} TÍTULOS:")
                    for el in titulos_elementos:
                        titulo = el.get_attribute("title")
                        if titulo:
                            print(f" - {titulo}")
                else:
                    print(f"[{self.user_data_dir}] NO SE ENCONTRARON TÍTULOS DE GRUPOS EN PANTALLA")
            except Exception as e:
                print(f"[{self.user_data_dir}] Error al obtener títulos: {e}")

    def entrar_a_chat(self, nombre_grupo):
        """Busca un grupo específico en la lista actual, haciendo scroll mediante un ciclo hasta encontrarlo"""
        if not self.ready:
            print(f"[{self.user_data_dir}] Error: El bot aún no está listo.")
            return

        with self.lock:
            print(f"\n[{self.user_data_dir}] Buscando grupo: '{nombre_grupo}'...")
            selector = WhatsappSelectors.GRUPO_ESPECIFICO.format(nombre_grupo)
            
            # Obtenemos el panel lateral donde están los chats para poder hacerle scroll
            try:
                pane_side = self.sb.driver.find_element(By.ID, "pane-side")
            except Exception:
                print(f"[{self.user_data_dir}] No se encontró el contenedor de chats. Asegúrate de haber entrado a Grupos primero.")
                return

            encontrado = False
            max_intentos = 30
            intentos = 0
            last_scroll_top = -1

            while intentos < max_intentos:
                try:
                    elementos = self.sb.driver.find_elements(By.XPATH, selector)
                    if elementos:
                        el = elementos[0]
                        # Hacemos scroll pero centrando el elemento para que no quede oculto detrás de la barra superior fija de WhatsApp
                        self.sb.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
                        time.sleep(1)
                        
                        # Intentamos diferentes métodos de click hasta que detectemos que el chat se ha abierto (aparece la barra de texto)
                        estrategias = [
                            lambda: self.sb.click(selector),
                            lambda: el.click(),
                            lambda: self.sb.execute_script("arguments[0].dispatchEvent(new MouseEvent('mousedown', {bubbles: true})); arguments[0].dispatchEvent(new MouseEvent('mouseup', {bubbles: true})); arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", el),
                            lambda: self.sb.execute_script("arguments[0].click();", el)
                        ]
                        
                        chat_abierto = False
                        for click_func in estrategias:
                            try:
                                click_func()
                                time.sleep(1.5) # Esperamos a que cargue el chat
                                # Si encontramos la barra de escribir mensaje, el click funcionó
                                if self.sb.driver.find_elements(By.XPATH, WhatsappSelectors.CHAT_INPUT):
                                    chat_abierto = True
                                    break
                            except Exception:
                                pass
                                
                        if chat_abierto:
                            print(f"[{self.user_data_dir}] Se ha entrado al chat del grupo: {nombre_grupo}")
                        else:
                            print(f"[{self.user_data_dir}] Se encontró el grupo pero los clicks parecen no haber abierto el chat.")
                        
                        encontrado = True
                        break
                    else:
                        # Comprobamos si el scroll avanzó o llegó al final
                        current_scroll = self.sb.execute_script("return arguments[0].scrollTop;", pane_side)
                        if current_scroll == last_scroll_top:
                            print(f"[{self.user_data_dir}] Se llegó al final de la lista de chats. No hay más grupos para cargar.")
                            break
                        last_scroll_top = current_scroll
                        
                        # Si no está, hacemos scroll hacia abajo en el panel y esperamos a que cargue
                        self.sb.execute_script("arguments[0].scrollTop += 600;", pane_side)
                        time.sleep(1)
                        intentos += 1
                        print(f"[{self.user_data_dir}] Haciendo scroll... (intento {intentos}/{max_intentos})")
                except Exception as e:
                    print(f"[{self.user_data_dir}] Error en búsqueda de chat: {e}")
                    break
                    
            if not encontrado:
                print(f"[{self.user_data_dir}] No se encontró el grupo '{nombre_grupo}' tras recorrer la lista.")

    def escribir_y_enviar_mensaje(self, texto):
        """Escribe un texto en la barra de chat actual y presiona enviar"""
        if not self.ready:
            print(f"[{self.user_data_dir}] Error: El bot aún no está listo.")
            return

        with self.lock:
            print(f"\n[{self.user_data_dir}] Escribiendo mensaje...")
            
            try:
                # 1. Buscar y escribir en la caja de texto probando múltiples selectores estables de test_click.py
                selectores_caja = [
                    '//div[@data-testid="conversation-compose-box-input" and @contenteditable="true"]',
                    '//div[@data-testid="conversation-compose-box-input"]',
                    '//div[@role="textbox" and @contenteditable="true" and contains(@aria-label, "Escribir un mensaje")]',
                    '//div[contains(@class, "copyable-text") and contains(@class, "selectable-text") and @contenteditable="true"]'
                ]
                
                chat_box = None
                for sel in selectores_caja:
                    try:
                        elementos = self.sb.driver.find_elements(By.XPATH, sel)
                        if elementos and elementos[0].is_displayed():
                            chat_box = elementos[0]
                            break
                    except Exception:
                        pass
                
                if not chat_box:
                    print(f"[{self.user_data_dir}] No se encontró la barra de texto con ningún selector.")
                    return
                
                # Escribimos el mensaje
                chat_box.click()
                time.sleep(0.5)
                chat_box.send_keys(texto)
                time.sleep(1)
                
                # 2. Presionar el botón de enviar probando múltiples selectores estables de test_click.py
                print(f"[{self.user_data_dir}] Presionando botón enviar...")
                selectores_enviar = [
                    '//button[@aria-label="Enviar"]',
                    '//button[@data-tab="11" and @aria-label="Enviar"]',
                    '//span[@data-icon="wds-ic-send-filled"]',
                    '//span[@data-testid="wds-ic-send-filled"]',
                    '//span[@data-icon="send"]'
                ]
                
                btn_enviar = None
                for sel_env in selectores_enviar:
                    try:
                        elementos = self.sb.driver.find_elements(By.XPATH, sel_env)
                        if elementos and elementos[0].is_displayed():
                            btn_enviar = elementos[0]
                            break
                    except Exception:
                        pass
                
                if btn_enviar:
                    btn_enviar.click()
                    print(f"[{self.user_data_dir}] ¡Mensaje enviado exitosamente!")
                else:
                    # Alternativa: presionar Enter directamente en el chat box
                    try:
                        from selenium.webdriver.common.keys import Keys
                        chat_box.send_keys(Keys.ENTER)
                        print(f"[{self.user_data_dir}] No se encontró el botón de enviar, se intentó enviar presionado la tecla ENTER.")
                    except Exception as ex:
                        print(f"[{self.user_data_dir}] Falló tanto el botón de enviar como el envío por ENTER: {ex}")
            except Exception as e:
                print(f"[{self.user_data_dir}] Error al escribir/enviar mensaje: {e}")
