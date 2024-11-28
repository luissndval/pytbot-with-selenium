import time
from selenium.webdriver.common.by import By
from features.resource.element.elements import elements
from src.functions_selenium import Functions

class addProduct(Functions):
    def addProduct(self):
        Functions.click_while(self, By.XPATH, elements["addProduct"][0])
        Functions.take_screenshot(self, "Visualizacion de Productos.")
        Functions.click_field(self, By.XPATH, elements["addProduct"][1])
        Functions.click_field(self, By.XPATH, elements["addProduct"][2])
        Functions.click_while(self, By.XPATH, elements["addProduct"][3])
        Functions.take_screenshot(self, "add to cart")
        time.sleep(2)
