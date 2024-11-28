from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from features.resource.element import elements
from src.functions_selenium import  Functions


class buy(Functions):

    def Shipping(self):
        Functions.click_while(self, By.XPATH, elements["Shipping"][0])
        Functions.input_text(self, By.XPATH, elements["Shipping"][1],"Valor 1")
        Functions.input_text(self, By.XPATH, elements["Shipping"][2], "Valor 2")
        Functions.input_text(self, By.XPATH, elements["Shipping"][3], "1406")
        Functions.input_text(self, By.XPATH, elements["Shipping"][4], "1150163632")
        Functions.click_field(self,By.XPATH,elements["Shipping"][5])
        Functions.key_up_key_down(self,Keys.DOWN)
        Functions.key_up_key_down(self, Keys.ENTER)
        Functions.click_while(self, By.XPATH, elements["Shipping"][6])
        Functions.take_screenshot(self, "Info Shipping")

    def Select_Shipping_Price(self):
        Functions.click_while(self, By.XPATH, elements["Select_Shipping_Price"][0])
        Functions.take_screenshot(self, "Info Shipping")
        Functions.click_while(self, By.XPATH, elements["Shipping"][6])


    def Payment(self):
        Functions.take_screenshot(self, "Info Shipping")
        Functions.click_while(self, By.XPATH, elements["Shipping"][6])

    def OrderReview(self):
        Functions.take_screenshot(self, "OrderReview")
        Functions.click_while(self, By.XPATH, elements["Payment"][0])
