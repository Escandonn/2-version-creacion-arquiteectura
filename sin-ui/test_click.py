from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

def probar_clicks():
    USER_DATA_DIR = r"perfil/profile 1"
    
    print("Iniciando modo de prueba de clicks...")
    with SB(uc=False, headed=True, user_data_dir=USER_DATA_DIR) as sb:
        sb.open("https://web.whatsapp.com/")
        print("Esperando 15s a que cargue WhatsApp...")
        time.sleep(15)
        
        print("\nINSTRUCCIÓN: Por favor, en la ventana de WhatsApp que se abrirá, asegúrate de")
        print("que el grupo que vamos a probar sea VISIBLE en la lista de chats.")
        nombre = input("Ingresa una parte del nombre del grupo para probar: ")
        
        # Opciones de selectores
        xpath_fila = f'//div[@role="row" and .//span[@dir="auto" and contains(@title, "{nombre}") and contains(@class, "x1iyjqo2")]]'
        xpath_span = f'//span[@dir="auto" and contains(@title, "{nombre}") and contains(@class, "x1iyjqo2")]'
        
        while True:
            elementos_fila = sb.driver.find_elements(By.XPATH, xpath_fila)
            elementos_span = sb.driver.find_elements(By.XPATH, xpath_span)
            
            if not elementos_fila or not elementos_span:
                print(f"No se encontró el grupo '{nombre}'. Haz scroll en WhatsApp para que quede a la vista.")
                time.sleep(3)
                continue
            
            el_fila = elementos_fila[0]
            el_span = elementos_span[0]
            
            print(f"\nSe encontró el grupo. Probando estrategias de click...")
            
            estrategias = [
                {"nombre": "1. SeleniumBase sb.click() en la FILA", "func": lambda: sb.click(xpath_fila)},
                {"nombre": "2. SeleniumBase sb.click() en el SPAN", "func": lambda: sb.click(xpath_span)},
                {"nombre": "3. Selenium click() nativo en la FILA", "func": lambda: el_fila.click()},
                {"nombre": "4. Selenium click() nativo en el SPAN", "func": lambda: el_span.click()},
                {"nombre": "5. JS click() en la FILA", "func": lambda: sb.execute_script("arguments[0].click();", el_fila)},
                {"nombre": "6. JS click() en el SPAN", "func": lambda: sb.execute_script("arguments[0].click();", el_span)},
                {"nombre": "7. ActionChains click en la FILA", "func": lambda: ActionChains(sb.driver).move_to_element(el_fila).click().perform()},
                {"nombre": "8. JS Mousedown + Mouseup + Click en la FILA", "func": lambda: sb.execute_script("arguments[0].dispatchEvent(new MouseEvent('mousedown', {bubbles: true})); arguments[0].dispatchEvent(new MouseEvent('mouseup', {bubbles: true})); arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", el_fila)}
            ]
            
            for estrategia in estrategias:
                print(f"\nIntentando: {estrategia['nombre']}")
                try:
                    estrategia['func']()
                    print("-> Ejecutado sin errores en código. Revisa WhatsApp para ver si el chat se abrió.")
                except Exception as e:
                    print(f"-> Error devuelto por Selenium: {e}")
                
                resp = input("¿Se abrió el chat? (s/n/salir): ").lower()
                if resp == 's':
                    print(f"\n¡ÉXITO! La estrategia ganadora es: {estrategia['nombre']}")
                    print("Anota el número de la estrategia para actualizar el código principal.")
                    input("Presiona ENTER para cerrar el navegador y salir...")
                    return
                elif resp == 'salir':
                    return
                print("El chat no se abrió. Intentando la siguiente estrategia...")
                time.sleep(1)

if __name__ == "__main__":
    probar_clicks()
