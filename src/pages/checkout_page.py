from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class CheckoutPage(BasePage):
    # TODO: Adjust locators to actual DOM
    BUYER_NAME = (By.CSS_SELECTOR, "input[name*='buyer'], input[placeholder*='שם']")
    BUYER_EMAIL = (By.CSS_SELECTOR, "input[type='email']")
    BUYER_PHONE = (By.CSS_SELECTOR, "input[type='tel'], input[placeholder*='טלפון']")
    CONTINUE_TO_PAYMENT = (By.XPATH, "//button[contains(.,'לתשלום') or contains(.,'המשך')]")

    def fill_buyer_details(self, name: str, email: str, phone: str):
        self.type(self.BUYER_NAME, name)
        self.type(self.BUYER_EMAIL, email)
        self.type(self.BUYER_PHONE, phone)
        return self

    def continue_to_payment(self):
        self.click(self.CONTINUE_TO_PAYMENT)
        return self
