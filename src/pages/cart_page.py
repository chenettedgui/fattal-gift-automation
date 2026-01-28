from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class CartPage(BasePage):
    # TODO: Adjust locators to actual DOM
    CHECKOUT_BTN = (By.XPATH, "//button[contains(.,'לתשלום') or contains(.,'המשך')]")

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BTN)
        return self
