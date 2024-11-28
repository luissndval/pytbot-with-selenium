import yaml
import json
import csv
import logging
import os
from dotenv import load_dotenv
from selenium.common import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class ReadAndCreateDoc:

    def read_configuration(ruta_archivo):
        """
        Lee un archivo de configuración y devuelve su contenido como un diccionario.

        :param ruta_archivo: La ruta del archivo de configuración.
        :return: Un diccionario con el contenido del archivo de configuración.
        """
        ext = os.path.splitext(ruta_archivo)[1].lower()

        if ext == '.yaml' or ext == '.yml':
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                config = yaml.safe_load(archivo)
        elif ext == '.json':
            with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                config = json.load(archivo)
        elif ext == '.env':
            load_dotenv(ruta_archivo)
            config = {key: os.getenv(key) for key in os.environ}
        else:
            raise ValueError('Formato de archivo no soportado: {}'.format(ext))

        return config

    def create_document(self, doc_name, column_name, by, selector, timeout=5):
        try:
            # Ruta del archivo CSV
            current_path = os.path.abspath(__file__)
            parent_path = os.path.dirname(os.path.dirname(current_path))
            txt_path = os.path.join(parent_path, 'txt')
            csv_path = os.path.join(txt_path, f'{doc_name}.csv')

            # Obtener el valor del elemento
            element_text = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, selector))).text
            cleaned_value = element_text.replace('"', '').replace('\n', '')

            # Verificar si el archivo CSV existe o no
            file_exists = os.path.exists(csv_path)
            with open(csv_path, 'a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [column_name]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Si el archivo no existe, escribir el encabezado
                if not file_exists:
                    writer.writeheader()

                writer.writerow({column_name: cleaned_value})

            logging.info(f"Valor '{cleaned_value}' escrito en el documento '{doc_name}.csv', columna: {column_name}")

        except NoSuchElementException as ex:
            logging.error(
                f"Error: No se encontró el elemento con el selector '{selector}' de tipo: '{by}'. Detalles: {ex}")
            raise
        except Exception as ex:
            logging.error(f"Error desconocido al crear o escribir en el documento '{doc_name}.csv'. Detalles: {ex}")
            raise