from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class ProductListPage(BasePage):
    # TODO: Adjust locators to actual DOM
    FIRST_PRODUCT = (By.CSS_SELECTOR, "[data-testid='product-card'], .product-card")

    def open_first_product(self):
        self.click(self.FIRST_PRODUCT)
        return self
