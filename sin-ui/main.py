from seleniumbase import SB
from selenium.webdriver.common.by import By
import time


USER_DATA_DIR = r"perfil/profile 1"

with SB(
    uc=False,
    headed=True,
    user_data_dir=USER_DATA_DIR,
) as sb:

    sb.open("https://web.whatsapp.com/")

    print("ESPERANDO WHATSAPP...")
    time.sleep(25)

    print("\nENTRANDO A GRUPOS...")

    try:

        elementos = sb.driver.find_elements(
            By.XPATH,
            '//span[text()="Grupos"]'
        )

        print("ENCONTRADOS:", len(elementos))

        for e in elementos:

            texto = e.text.strip()

            print("TEXTO:", texto)

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

    except Exception as ex:

        print("ERROR ENTRANDO A GRUPOS")
        print(ex)

    input("\nENTER PARA SALIR")