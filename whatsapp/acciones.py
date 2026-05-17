import time
from selenium.webdriver.common.by import By
from selectores.ui_selectors import WhatsappSelectors

def entrar_a_grupos(sb):
    """Busca y hace clic en la pestaña de 'Grupos'"""
    try:
        elementos = sb.driver.find_elements(
            By.XPATH,
            WhatsappSelectors.GRUPOS_BUTTON
        )
        for e in elementos:
            if e.text.strip() == "Grupos":
                sb.execute_script("arguments[0].scrollIntoView(true);", e)
                time.sleep(1)
                sb.execute_script("arguments[0].click();", e)
                return True
    except Exception as e:
        print(f"Error al entrar a grupos: {e}")
    return False

def entrar_a_chat(sb, nombre_grupo):
    """Busca un grupo específico y entra a él"""
    selector = WhatsappSelectors.GRUPO_ESPECIFICO.format(nombre_grupo)
    
    try:
        pane_side = sb.driver.find_element(By.ID, "pane-side")
    except Exception:
        return False, "No se encontró el contenedor de chats."

    encontrado = False
    max_intentos = 30
    intentos = 0
    last_scroll_top = -1

    while intentos < max_intentos:
        elementos = sb.driver.find_elements(By.XPATH, selector)
        if elementos:
            el = elementos[0]
            sb.execute_script("arguments[0].scrollIntoView({block: 'center'});", el)
            time.sleep(1)
            
            estrategias = [
                lambda: sb.click(selector),
                lambda: el.click(),
                lambda: sb.execute_script("arguments[0].dispatchEvent(new MouseEvent('mousedown', {bubbles: true})); arguments[0].dispatchEvent(new MouseEvent('mouseup', {bubbles: true})); arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));", el),
                lambda: sb.execute_script("arguments[0].click();", el)
            ]
            
            chat_abierto = False
            for click_func in estrategias:
                try:
                    click_func()
                    time.sleep(1.5)
                    if sb.driver.find_elements(By.XPATH, WhatsappSelectors.CHAT_INPUT):
                        chat_abierto = True
                        break
                except Exception:
                    pass
                    
            if chat_abierto:
                return True, "Chat abierto exitosamente"
            else:
                return False, "Se encontró pero no se pudo hacer click."
            
        else:
            current_scroll = sb.execute_script("return arguments[0].scrollTop;", pane_side)
            if current_scroll == last_scroll_top:
                return False, "Se llegó al final de la lista."
            last_scroll_top = current_scroll
            
            sb.execute_script("arguments[0].scrollTop += 600;", pane_side)
            time.sleep(1)
            intentos += 1
            
    return False, "No se encontró el grupo."

def escribir_y_enviar_mensaje(sb, texto, nombre_grupo=None):
    """Escribe un texto y presiona enviar"""
    # Intentamos primero el selector específico del grupo, si no, el genérico
    selectores_caja = [
        WhatsappSelectors.CHAT_INPUT_GRUPO.format(nombre_grupo) if nombre_grupo else "",
        WhatsappSelectors.CHAT_INPUT,
        '//div[@role="textbox" and @contenteditable="true"]'
    ]
    
    chat_box = None
    for selector in selectores_caja:
        if not selector: continue
        inputs = sb.driver.find_elements(By.XPATH, selector)
        if inputs:
            chat_box = inputs[0]
            break
            
    if not chat_box:
        return False, "No se encontró la caja de texto."
        
    try:
        chat_box.click()
        time.sleep(0.5)
        chat_box.send_keys(texto)
        time.sleep(1)
        
        # Enviar
        botones = sb.driver.find_elements(By.XPATH, WhatsappSelectors.SEND_BUTTON)
        if not botones:
            botones = sb.driver.find_elements(By.XPATH, WhatsappSelectors.SEND_BUTTON_ICON)
            
        if botones:
            botones[0].click()
            return True, "Mensaje enviado."
        else:
            return False, "No se encontró el botón de enviar."
    except Exception as e:
        return False, f"Error enviando mensaje: {e}"
