from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class VoucherPage(BasePage):
    # TODO: Adjust locators to actual DOM
    AMOUNT_INPUT = (By.CSS_SELECTOR, "input[type='number'], input[name*='amount']")
    NEXT_BTN = (By.XPATH, "//button[contains(.,'המשך') or contains(.,'להמשך')]")

    def set_amount(self, amount: int):
        self.type(self.AMOUNT_INPUT, str(amount))
        return self

    def next(self):
        self.click(self.NEXT_BTN)
        return self
