from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class ConfirmationPage(BasePage):
    # TODO: Adjust locators to actual DOM
    SUCCESS_TITLE = (By.XPATH, "//*[contains(.,'אישור') or contains(.,'הצלחה') or contains(.,'תודה')]")

    def is_success(self) -> bool:
        return self.is_visible(self.SUCCESS_TITLE)
