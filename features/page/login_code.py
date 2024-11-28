import time
from selenium.webdriver.common.by import By
from features.resource.element import elements
from src.functions_selenium import  Functions


class Login(Functions):

        def loginuser(self, email, password):
            xpath = elements.elements
            Functions.click_field(self, By.XPATH, xpath["logIn"][0])
            time.sleep(1)
            Functions.click_field(self, By.XPATH, xpath["logIn"][1])
            time.sleep(1)
            Functions.input_text(self, By.XPATH, xpath["logIn"][2], email)
            time.sleep(1)
            Functions.input_text(self, By.XPATH, xpath["logIn"][3], password)
            time.sleep(1)
            Functions.click_field(self, By.XPATH, xpath["logIn"][4])
            time.sleep(1)
            Functions.click_field(self, By.XPATH, xpath["logIn"][5])
            time.sleep(1)
            Functions.take_screenshot(self, "Inicio Sesion")

