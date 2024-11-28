import os
import yaml
from src.functions_selenium import Functions


def after_scenario(context, scenario):
    # Capturar pantalla si el escenario falla
    if scenario.status == "failed":
        screenshot_name = f"{scenario.name.replace(' ', '_')}.png"
        screenshot_path = os.path.join("reports", "screenshots", screenshot_name)
        context.driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved as {screenshot_path}")

    # Cerrar el navegador
    context.driver.quit()
