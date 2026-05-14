from seleniumbase import SB
from selenium.webdriver.common.by import By
import time
from ui_selectors import WhatsappSelectors

class WhatsappBot:
    def __init__(self, user_data_dir=r"perfil/profile 1"):
        self.user_data_dir = user_data_dir

    def run(self):
        with SB(
            uc=False,
            headed=True,
            user_data_dir=self.user_data_dir,
        ) as sb:
            self.proceso(sb)

    def proceso(self, sb):
        sb.open("https://web.whatsapp.com/")

        print("ESPERANDO WHATSAPP...")
        time.sleep(15)

        print("\nENTRANDO A GRUPOS...")

        try:
            elementos = sb.driver.find_elements(
                By.XPATH,
                WhatsappSelectors.GRUPOS_BUTTON
            )

            print("ENCONTRADOS:", len(elementos))

            for e in elementos:
                texto = e.text.strip()
                

                if texto == "Grupos":
                    # SCROLL
                    sb.execute_script(
                        "arguments[0].scrollIntoView(true);",
                        e
                    )
                    time.sleep(1)

                    # CLICK DIRECTO
                    sb.execute_script(
                        "arguments[0].click();",
                        e
                    )
                    print("CLICK EN GRUPOS OK")
                    break

            # OBTENER TÍTULOS DE GRUPOS DESPUÉS DE PRESIONAR BOTÓN
            print("\nOBTENIENDO TÍTULOS DE LOS GRUPOS...")
            time.sleep(3) # Esperar a que los grupos carguen en la interfaz

            titulos_elementos = sb.driver.find_elements(By.XPATH, WhatsappSelectors.TITULOS_GRUPOS)
            
            if titulos_elementos:
                print(f"SE ENCONTRARON {len(titulos_elementos)} TÍTULOS DE GRUPOS:")
                for el in titulos_elementos:
                    titulo = el.get_attribute("title")
                    if titulo:
                        print(f" - {titulo}")
            else:
                print("NO SE ENCONTRARON TÍTULOS DE GRUPOS EN PANTALLA")

        except Exception as ex:
            print("ERROR EN EL PROCESO")
            print(ex)

        input("\nENTER PARA SALIR")
