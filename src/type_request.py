import csv
import json
import logging
import os
from datetime import datetime

import allure
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def handle_request_exception(e, response):
    """Maneja las excepciones de las solicitudes HTTP"""
    response_type = "error"
    response_data = None
    status_code = None
    response_body = None

    logger.error(f"----->>> Error in request: {e}")

    if isinstance(e, requests.exceptions.HTTPError):
        status_code = response.status_code  # Capturar el código de estado
        logger.error(f"----->>> Status code: {status_code}")
        response_body = response.content.decode('utf-8')
        response_data = response_body  # Asignar el contenido de la respuesta como response_data

    return {
        "response_type": response_type,
        "response_data": response_data,
        "status_code": status_code,
        "response_body": response_body  # Incluir el código de estado en el diccionario de retorno
    }

class Apis:
    def __init__(self, initial_id=1):
        self.current_id = initial_id

    @staticmethod
    def read_json(nombre_archivo):
        """Lee datos de un archivo JSON"""
        ruta_principal = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_json = os.path.join(ruta_principal, 'data', nombre_archivo)
        try:
            with open(ruta_json, 'r') as archivo:
                datos = json.load(archivo)
            return datos
        except FileNotFoundError:
            logger.error(f"El archivo '{nombre_archivo}' no fue encontrado en la carpeta 'data'.")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar el archivo JSON: {str(e)}")
            return None

    @staticmethod
    def get_request_form_data(url, headers=None, data=None):
        """Realiza una solicitud GET y obtiene los datos en formato de formulario"""
        response = None
        try:
            response = requests.get(url, headers=headers, data=data)
            response.raise_for_status()
            json_data = response.json()
            response_type = "success"
            response_body_request = response.content.decode('utf-8')
            status_code_request = response.status_code  # Capturar el status code de la respuesta
            return {"response_type": response_type,
                    "response_data": json_data,
                    'response_body_request': response_body_request,
                    'status_code_request': status_code_request,
                    "response": response}
        except requests.exceptions.RequestException as e:
            return handle_request_exception(e, response)

    @staticmethod
    def post_request(url, headers=None, data=None, json_data=None):
        """Realiza una solicitud POST con los datos proporcionados"""
        try:
            response = requests.post(url, headers=headers, data=data, json=json_data)
            response.raise_for_status()
            json_data = response.json()
            response_type = "success"
            status_code_ = response.status_code  # Capturar el status code de la respuesta
            response_body_request = response.content.decode('utf-8')
            return {
                "response_type": response_type,
                "response_data": json_data,
                "response_body": response_body_request,
                "status_code": status_code_
            }
        except requests.exceptions.RequestException as e:
            return handle_request_exception(e, response)

    @staticmethod
    def upload_file(url, headers=None, file_path=None):
        """Sube un archivo usando una solicitud POST"""
        try:
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(url, headers=headers, files=files)
                response.raise_for_status()
                response_type = "success"
                response_body_request = response.content.decode('utf-8')
                return {
                    "response_type": response_type,
                    "response_body_request": response_body_request,
                    "response": response
                }
        except requests.exceptions.RequestException as e:
            return handle_request_exception(e, response)

    @staticmethod
    def take_screenshot(driver, name):
        """Captura una imagen de la página web actual y la adjunta al reporte de Allure"""
        try:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
            logger.info(f"Captura de pantalla realizada y guardada como '{name}' en el reporte de Allure.")
        except Exception as ex:
            logger.error(f"Error al capturar la pantalla. Detalles: {ex}")
            raise

    @staticmethod
    def create_document(doc_name, column_name, by, selector, timeout=5):
        """Crea un documento CSV y escribe el contenido de un elemento en él."""
        try:
            ruta_principal = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ruta_json = os.path.join(ruta_principal, 'data', doc_name)
            element_text = Apis.get_request_form_data(selector, by, timeout)
            cleaned_value = element_text.replace('"', '').replace('\n', '')

            file_exists = os.path.exists(ruta_json)
            with open(ruta_json, 'a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [column_name]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()
                writer.writerow({column_name: cleaned_value})

            logger.info(f"Valor '{cleaned_value}' escrito en el documento '{doc_name}.csv', columna: {column_name}")

        except Exception as ex:
            logger.error(f"Error al crear o escribir en el documento '{doc_name}.csv'. Detalles: {ex}")
            raise

    @staticmethod
    def validate_json(expected_data, response_data):
        """Valida los datos esperados en la respuesta JSON"""
        def validate_fields(expected_datas, data, parent_key=""):
            for key, expected_type in expected_datas.items():
                if isinstance(expected_type, dict):
                    if key in data:
                        validate_fields(expected_type, data[key], parent_key=f"{parent_key}.{key}")
                    else:
                        logger.warning(f"Campo '{parent_key}.{key}' no encontrado en response_data")
                else:
                    if key in data:
                        value = data[key]
                        if expected_type is type(None):
                            if value is None or value.lower() >= "null":
                                logger.info(f"Campo '{parent_key}.{key}' validado")
                            else:
                                logger.warning(f"Campo '{parent_key}.{key}' no tiene el tipo de dato esperado: {expected_type.__name__}")
                        elif isinstance(value, expected_type):
                            logger.info(f"Campo '{parent_key}.{key}' validado")
                        else:
                            logger.warning(f"Campo '{parent_key}.{key}' no tiene el tipo de dato esperado: {expected_type.__name__}")
                    else:
                        logger.warning(f"Campo '{parent_key}.{key}' no encontrado en response_data")

        if isinstance(response_data, dict):
            validate_fields(expected_data, response_data)
        else:
            logger.warning("El JSON no es un diccionario válido.")

    @staticmethod
    def addreport(response_bodys):
        """Adjunta el cuerpo de la respuesta al reporte de Allure"""
        allure.attach(response_bodys, "Response Body", allure.attachment_type.TEXT)

    @staticmethod
    def dateformat():
        """Devuelve la fecha y hora actual en formato YYYY-MM-DD HH:MM:SS"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
