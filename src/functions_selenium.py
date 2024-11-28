import logging
import os
import time

import allure
from allure_commons.types import AttachmentType
from dotenv import load_dotenv
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common import *
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

nodeURL = 'http://localhost:8085'


class Functions:
    def __init__(self, driver=None):
        self.driver = driver
        load_dotenv()  # Cargar variables de entorno desde el archivo .env
        self.backend_url = os.getenv("HEALENIUM_BACKEND_URL")

    def initialize_driver(self, browser_type="chrome", headless=False,
                          use_healenium=False, window_size="1920,1080", healenium_url="http://localhost:7878"):
        if browser_type.lower() == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--start-maximized")
                display = Display(visible=0, size=(800, 600))
                display.start()

            if use_healenium:
                # Configuración para Healenium en Chrome
                healenium_url = "http://localhost:7878"  # Ajusta la URL según tu configuración de Healenium
                self.driver = webdriver.Remote(command_executor=healenium_url, options=options)
            else:
                # Configuración estándar de Chrome
                self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        elif browser_type.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.headless = True

            if use_healenium:
                # Configuración para Healenium en Firefox
                healenium_url = "http://localhost:7878"  # Ajusta la URL según tu configuración de Healenium
                self.driver = webdriver.Remote(command_executor=healenium_url, options=options)
            else:
                # Configuración estándar de Firefox
                self.driver = webdriver.Firefox()

        else:
            raise ValueError("Unsupported browser type. Use 'chrome' or 'firefox'.")

        return self.driver

    def browser(self, link):
        """
        Abre una página web con la URL proporcionada y maximiza la ventana del navegador.

        :param link: URL de la página web a abrir.
        """
        self.driver.get(link)
        time.sleep(5)
        print("Página abierta: " + str(link))

    def maximize(self):
        self.driver.maximize_window()
        time.sleep(3)

    def click_while(self, by, selector_base, timeout=5):

        index = 1
        while True:
            xpath = f"{selector_base}{index}]"
            try:
                WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, xpath))).click()
                logging.info(f"Click en el elemento: {by}={xpath}")
                return True
            except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
                logging.warning(f"Intento fallido para hacer clic en el elemento {by}={xpath}: {str(e)}")
                index += 1
                if index > 10:  # Límite para evitar bucles infinitos
                    logging.error(f"No se encontró un elemento clickable después de {index - 1} intentos.")
                    return False

    def input_text(self, by, selector, text, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.clear()
        element.send_keys(text)
        logging.info(f"Texto '{text}' escrito en el campo {selector}.")

    def click_field(self, by, selector, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)  # Pausa breve antes de hacer clic
        element.click()
        time.sleep(2)  # Pausa breve después del clic para garantizar la carga
        logging.info(f"Click realizado en el elemento -> {selector}")

    def clear_field(self, by, selector, timeout=30):

        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, selector)))
        element.clear()
        logging.info(f"Texto eliminado en el campo -> {selector}")

    def validates(self, by, selector, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, selector)))
        text = element.text
        logging.info(f"Elemento validado. Texto presente en el elemento '{selector}': {text}")

    def upload_file(self, by, selector, file_path):
        element = self.driver.find_element(by, selector)
        element.send_keys(file_path)
        logging.info(f"Archivo cargado en el elemento -> {selector}")

    def scroll_to_element(self, by, selector, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        logging.info(f"Desplazado al elemento -> {selector}")

    def take_screenshot(self, name):
        time.sleep(3)
        allure.attach(self.driver.get_screenshot_as_png(), name=name, attachment_type=AttachmentType.PNG)
        logging.info(f"Captura de pantalla realizada y guardada como '{name}' en el reporte de Allure.")

    def input_text_action_chains(self, by, selector, text):
        action = ActionChains(self.driver)
        element = self.driver.find_element(by, selector)
        action.move_to_element(element).click().perform()  # Asegura que el elemento sea clicado
        action.send_keys(Keys.CONTROL, 'a').send_keys(Keys.BACKSPACE).perform()  # Limpia el campo
        action.send_keys(text).perform()  # Escribe el texto
        logging.info(f"Texto '{text}' ingresado en el campo '{selector}' usando ActionChains.")
        time.sleep(1)  # Pausa breve para asegurar la entrada de texto

    def click_action(self, by, selector, timeout=30):
        action = ActionChains(self.driver)
        element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable((by, selector)))
        action.move_to_element(element).click().perform()
        logging.info(f"Se hizo clic en el elemento -> {selector}")
        time.sleep(1)  # Pausa breve para asegurar que se complete el clic

    def key_up_key_down(self, key):
        action = ActionChains(self.driver)
        action.key_down(key).perform()
        action.key_up(key).perform()
        logging.info(f"Simulación de pulsación y liberación de la tecla '{key}' realizada correctamente.")
        time.sleep(1)

    def input_text_visibility(self, by, selector, text, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        element.send_keys(text)
        logging.info(f"Escribir en el campo {selector} el texto -> {text}")
        time.sleep(1)  # Pausa breve para asegurar que el texto se ingrese correctamente

    def click_field_visibility(self, by, selector, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        element.click()
        logging.info(f"Click sobre el elemento -> {selector}")
        time.sleep(2)  # Pausa breve para asegurar que se complete la acción de clic

    def clear_field_visibility(self, by, selector, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        element.clear()
        logging.info(f"Texto eliminado en el campo -> {selector}")

    def is_element_visible_and_interactable(self, by, selector, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, selector)))
        if element.is_displayed() and element.is_enabled():
            logging.info(
                f"Elemento Validado -> {selector}, Visible: {element.is_displayed()}, Interactuable: {element.is_enabled()}")
            logging.info(f"Texto del elemento: {element.text}")
            return True

    def is_element_visible_and_interactable_v2(self, by, selector, timeout=30):
        element = None
        element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, selector)))

        if element.is_displayed() and element.is_enabled():
            logging.info(
                "Elemento Validado -> {selector}, Visible: {element.is_displayed()}, Interactuable: {element.is_enabled()}")
            return True
        else:
            logging.warning(f"Elemento no visible o no interactuable -> {selector}")
            return False

    def validates_presence(self, tipo, selector):
        element = WebDriverWait(self.driver, timeout=30).until(EC.presence_of_element_located((tipo, selector)))
        print(element.text)
        print("\nElemento Validado -> {}".format(selector))

    def validates_clickable(self, tipo, selector):
        element = WebDriverWait(self.driver, timeout=5).until(EC.element_to_be_clickable((tipo, selector)))
        print(element.text)
        print("\nElemento Validado -> {}".format(selector))

    def validate_without_exception_visibility(self, by, selector, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        logging.info(f"Elemento Validado -> {selector}, Texto: {element.text}")
        return element.text

    def upload_file_visibility(self, by, selector, file_path, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        element.send_keys(file_path)
        logging.info(f"Archivo cargado en el elemento -> {selector}")


    def scroll_to_element_visibility(self, by, selector, timeout=30):
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, selector)))
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        logging.info(f"Desplazando al elemento -> {selector}")

    def switch_to_iframe(self, by, selector):
        element = self.driver.find_element(by, selector)
        self.driver.switch_to.frame(element)
        logging.info(f"Successfully switched to iframe -> {selector}")

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
        logging.info("Cambiado al contenido principal (default content).")


    def new_window(self, link):
        self.driver.execute_script("window.open('about:blank','_blank');")
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        self.driver.get(link)


    def change_windows(self, link):
        window = self.driver.window_handles
        self.driver.switch_to.window(window[1])
        self.driver.get(link)

    def new_windows(self, link):
        self.driver.execute_script("window.open('about:blank','_blank');")
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        self.driver.get(link)
