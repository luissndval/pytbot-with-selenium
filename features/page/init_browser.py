import os
import time

import yaml
from dotenv import load_dotenv

from src.functions_selenium import Functions  # Asegúrate de que esta función está definida correctamente


class Browser:
    def __init__(self):
        # Cargar las configuraciones desde el archivo .env
        load_dotenv()  # Carga las variables de entorno desde el archivo .env

    def start_browser(self, ambiente, link):
        try:
            # Construir la ruta del archivo YAML dinámicamente
            yaml_path = os.path.join("features", "resource", "config", "config.yaml")

            # Cargar configuración desde el archivo YAML
            with open(yaml_path, "r") as file:
                config = yaml.safe_load(file)

            # Obtener el tipo de navegador del YAML
            browser_config = config.get("browser", {})
            browser_type = browser_config.get("type", "chrome")
            headless = browser_config.get("headless", False)

            window_size = browser_config.get("window_size", "1920,1080")
            use_healenium = browser_config.get("use_healenium", False)
            healenium_url = browser_config.get("healenium_url", "http://localhost:7878")

            # Inicializar el navegador con el tipo dinámico
            Functions.initialize_driver(
                self,
                browser_type=browser_type,
                headless=headless,
                window_size=window_size,
                use_healenium=use_healenium,
                healenium_url=healenium_url
            )
            Functions.browser(self, link)
            time.sleep(5)
            Functions.maximize(self)
        except Exception as e:
            print("Error:", e)
            raise
