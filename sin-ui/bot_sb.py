from seleniumbase import SB
from selenium.webdriver.common.by import By
import time
from ui_selectors import WhatsappSelectors

class WhatsappBot:
    def __init__(self, user_data_dir=r"perfil/profile 1"):
        self.user_data_dir = user_data_dir
        self.sb = None

    def run(self):
        with SB(
            uc=False,
            headed=True,
            user_data_dir=self.user_data_dir,
        ) as sb:
            self.sb = sb
            self.sb.open("https://web.whatsapp.com/")

            print("ESPERANDO WHATSAPP...")
            time.sleep(15)  # Tiempo de espera inicial para que cargue la interfaz
            
            self.iniciar_menu_interactivo()

    def iniciar_menu_interactivo(self):
        """Muestra un menú por consola para probar cada función paso a paso"""
        while True:
            print("\n--- MENÚ WHATSAPP BOT ---")
            print("1. Entrar a pestaña Grupos")
            print("2. Imprimir títulos de grupos disponibles")
            print("3. Entrar a un chat de grupo")
            print("4. Enviar un mensaje")
            print("5. Salir")
            
            opcion = input("Elige una opción: ")
            
            try:
                if opcion == "1":
                    self.entrar_a_grupos()
                elif opcion == "2":
                    self.obtener_titulos_grupos()
                elif opcion == "3":
                    nombre = input("Ingresa el título (o parte de él) del grupo: ")
                    self.entrar_a_chat(nombre)
                elif opcion == "4":
                    texto = input("Ingresa el mensaje a enviar: ")
                    self.escribir_y_enviar_mensaje(texto)
                elif opcion == "5":
                    print("Saliendo...")
                    break
                else:
                    print("Opción inválida.")
            except Exception as ex:
                print(f"ERROR: {ex}")

    def entrar_a_grupos(self):
        """Busca y hace clic en la pestaña de 'Grupos'"""
        print("\nENTRANDO A GRUPOS...")
        
        elementos = self.sb.driver.find_elements(
            By.XPATH,
            WhatsappSelectors.GRUPOS_BUTTON
        )

        for e in elementos:
            if e.text.strip() == "Grupos":
                self.sb.execute_script("arguments[0].scrollIntoView(true);", e)
                time.sleep(1)
                self.sb.execute_script("arguments[0].click();", e)
                print("Click en pestaña Grupos realizado.")
                return
        print("No se encontró el botón de Grupos.")

    def obtener_titulos_grupos(self):
        """Extrae e imprime los títulos de los grupos mostrados en pantalla"""
        print("\nOBTENIENDO TÍTULOS DE LOS GRUPOS...")
        time.sleep(2) # Esperar a que los grupos carguen en la interfaz

        titulos_elementos = self.sb.driver.find_elements(
            By.XPATH, 
            WhatsappSelectors.TITULOS_GRUPOS
        )
        
        if titulos_elementos:
            print(f"SE ENCONTRARON {len(titulos_elementos)} TÍTULOS:")
            for el in titulos_elementos:
                titulo = el.get_attribute("title")
                if titulo:
                    print(f" - {titulo}")
        else:
            print("NO SE ENCONTRARON TÍTULOS DE GRUPOS EN PANTALLA")

    def entrar_a_chat(self, nombre_grupo):
        """Busca un grupo específico en la lista actual, haciendo scroll mediante un ciclo hasta encontrarlo"""
        print(f"\nBuscando grupo: '{nombre_grupo}'...")
        selector = WhatsappSelectors.GRUPO_ESPECIFICO.format(nombre_grupo)
        
        # Obtenemos el panel lateral donde están los chats para poder hacerle scroll
        try:
            pane_side = self.sb.driver.find_element(By.ID, "pane-side")
        except Exception:
            print("No se encontró el contenedor de chats. Asegúrate de haber entrado a Grupos primero.")
            return

        encontrado = False
        max_intentos = 30
        intentos = 0
        last_scroll_top = -1

        while intentos < max_intentos:
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
                    print(f"Se ha entrado al chat del grupo: {nombre_grupo}")
                else:
                    print(f"Se encontró el grupo pero los clicks parecen no haber abierto el chat.")
                
                encontrado = True
                break
            else:
                # Comprobamos si el scroll avanzó o llegó al final
                current_scroll = self.sb.execute_script("return arguments[0].scrollTop;", pane_side)
                if current_scroll == last_scroll_top:
                    print("Se llegó al final de la lista de chats. No hay más grupos para cargar.")
                    break
                last_scroll_top = current_scroll
                
                # Si no está, hacemos scroll hacia abajo en el panel y esperamos a que cargue
                self.sb.execute_script("arguments[0].scrollTop += 600;", pane_side)
                time.sleep(1)
                intentos += 1
                print(f"Haciendo scroll... (intento {intentos}/{max_intentos})")
                
        if not encontrado:
            print(f"No se encontró el grupo '{nombre_grupo}' tras recorrer la lista.")

    def escribir_y_enviar_mensaje(self, texto):
        """Escribe un texto en la barra de chat actual y presiona enviar"""
        print("\nEscribiendo mensaje...")
        
        # 1. Escribir texto
        inputs = self.sb.driver.find_elements(By.XPATH, WhatsappSelectors.CHAT_INPUT)
        if not inputs:
            print("No se encontró la barra de texto. ¿Estás dentro de un chat?")
            return
            
        chat_box = inputs[0]
        # Hacemos click en la caja de texto
        chat_box.click()
        time.sleep(0.5)
        # Enviamos el texto
        chat_box.send_keys(texto)
        time.sleep(1)
        
        # 2. Presionar el botón de enviar
        print("Presionando botón enviar...")
        botones = self.sb.driver.find_elements(By.XPATH, WhatsappSelectors.SEND_BUTTON)
        if botones:
            botones[0].click()
            print("¡Mensaje enviado exitosamente!")
        else:
            print("No se encontró el botón de enviar. A veces WhatsApp solo lo muestra si hay texto válido escrito.")
