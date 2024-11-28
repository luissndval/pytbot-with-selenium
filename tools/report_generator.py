import json
import os
import subprocess
from datetime import datetime

from fpdf import FPDF


def run_allure_report(allure_results_path, allure_report_path):
    """
    Ejecuta el comando Allure para generar el informe.
    """
    command = f"allure generate {allure_results_path} --clean -o {allure_report_path}"
    try:
        subprocess.run(command, shell=True, check=True)
        print("Allure report generado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al generar el reporte de Allure: {e}")
        raise


def extract_allure_data(allure_report_path):
    """
    Extrae datos relevantes del informe Allure generado.
    """
    summary_file = os.path.join(allure_report_path, "widgets", "summary.json")
    if not os.path.exists(summary_file):
        raise FileNotFoundError(f"No se encontró el archivo de resumen: {summary_file}")

    with open(summary_file, "r") as file:
        summary_data = json.load(file)

    # Extraer datos del resumen
    executed_cases = summary_data["statistic"]["total"]
    passed_cases = summary_data["statistic"]["passed"]
    failed_cases = summary_data["statistic"]["failed"]
    url = os.path.abspath(allure_report_path)  # Ruta del reporte generado
    set_data = "Datos del set de pruebas usados"  # Personalízalo según sea necesario

    return {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "executed_cases": executed_cases,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "url": url,
        "set_data": set_data,
    }


def extract_test_case_details(allure_results_path):
    """
    Extrae los nombres de los casos de prueba, parámetros y duración desde los archivos JSON de Allure.
    Calcula también el tiempo total de ejecución.
    """
    test_cases = []
    total_duration = 0  # Para acumular el tiempo total de ejecución

    # Recorremos todos los archivos en la carpeta allure-results
    for file_name in os.listdir(allure_results_path):
        if file_name.endswith(".json"):  # Solo archivos JSON
            file_path = os.path.join(allure_results_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                # Extraer el nombre del caso de prueba
                test_case_name = data.get("name", "Nombre no disponible")
                status = data.get("status", "Estado no disponible")

                # Extraer parámetros
                parameters = data.get("parameters", [])
                param_list = [f"- {param['name']}: {param['value']}" for param in parameters]

                # Calcular duración (si los datos están disponibles)
                start_time = data.get("start")
                stop_time = data.get("stop")
                duration = (stop_time - start_time) / 1000 if start_time and stop_time else 0  # Duración en segundos
                total_duration += duration

                test_cases.append({
                    "name": test_case_name,
                    "status": status,
                    "parameters": "\n    ".join(param_list) if param_list else "Sin parámetros",
                    "duration": f"{duration:.2f} segundos" if duration > 0 else "No disponible"
                })

    return test_cases, total_duration


def create_pdf_report_with_test_cases(data, test_cases, total_duration, output_path="report.pdf"):
    """
    Genera un informe PDF con datos como nombres, estados, parámetros, duración y tiempo total de ejecución.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título del informe
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Reporte de Casos de Prueba", ln=True, align="C")
    pdf.ln(10)

    # Resumen general
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt=f"Fecha: {data['date']}", ln=True)
    pdf.cell(0, 10, txt=f"Casos de Prueba Ejecutados: {data['executed_cases']}", ln=True)
    pdf.cell(0, 10, txt=f"Casos Exitosos: {data['passed_cases']}", ln=True)
    pdf.cell(0, 10, txt=f"Casos Fallidos: {data['failed_cases']}", ln=True)
    pdf.cell(0, 10, txt=f"Tiempo Total de Ejecución: {total_duration:.2f} segundos", ln=True)
    pdf.ln(10)

    # Detalle de los casos de prueba
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(0, 10, txt="Detalle de Casos de Prueba:", ln=True)
    pdf.set_font("Arial", size=12)

    for test_case in test_cases:
        pdf.set_font("Arial", style="B", size=12)
        # Nombre, estado y duración del caso
        pdf.cell(0, 10, txt=f"- {test_case['name']} ({test_case['status']})", ln=True)
        pdf.set_font("Arial", style="", size=12)
        pdf.cell(0, 10, txt=f"  Duración: {test_case['duration']}", ln=True)
        # Parámetros del caso (si existen)
        pdf.set_x(20)
        pdf.multi_cell(0, 10, txt=f"    {test_case['parameters']}", align="L")

    # Guardar el PDF
    pdf.output(output_path)
    print(f"Reporte PDF generado en: {output_path}")


def main():
    # Rutas de los directorios
    allure_results_path = "allure-results"  # Carpeta donde se guardan los resultados de Allure
    allure_report_path = "allure-report"  # Carpeta donde se generará el informe Allure
    pdf_output_path = "allure_report.pdf"  # Nombre del archivo PDF

    # Ejecutar el comando para generar el reporte Allure
    run_allure_report(allure_results_path, allure_report_path)

    # Extraer datos del resumen
    data = extract_allure_data(allure_report_path)

    # Extraer detalles de los casos de prueba y calcular el tiempo total
    test_cases, total_duration = extract_test_case_details(allure_results_path)

    # Crear el PDF con los datos extraídos
    create_pdf_report_with_test_cases(data, test_cases, total_duration, output_path=pdf_output_path)


if __name__ == "__main__":
    main()
