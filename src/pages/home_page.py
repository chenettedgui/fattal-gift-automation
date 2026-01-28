from selenium.webdriver.common.by import By

from src.core.config import (
    BASE_URL,
    BASIC_AUTH_USER,
    BASIC_AUTH_PASSWORD
)
from src.pages.base_page import BasePage
from src.pages.balance_modal import BalanceModal


class HomePage(BasePage):
    URL = BASE_URL

    BODY = (By.TAG_NAME, "body")

    # Button that opens the balance popup (based on class list you provided)
    CHECK_BALANCE_BTN = (
        By.CSS_SELECTOR,
        "button.btn.nav-btn.rounded-3.d-none.d-md-block"
    )

    def load(self):
        if BASIC_AUTH_USER and BASIC_AUTH_PASSWORD:
            return self.open_with_basic_auth(self.URL, BASIC_AUTH_USER, BASIC_AUTH_PASSWORD)
        return self.open(self.URL)

    def is_loaded(self) -> bool:
        return self.is_visible(self.BODY)

    def open_check_balance_modal(self) -> BalanceModal:
        self.click(self.CHECK_BALANCE_BTN)
        return BalanceModal(self.driver)
