from selenium.webdriver.common.by import By
import time

from src.pages.base_page import BasePage


class BalanceModal(BasePage):
    # Coupon input field
    COUPON_INPUT = (
        By.CSS_SELECTOR,
        ".form-control.text-center.fs--18.rounded-1.mb-3"
    )

    # "Check" button by ID (most stable)
    CHECK_BUTTON = (
        By.ID,
        "checkRemainingBtn"
    )

    def is_open(self) -> bool:
        return self.is_visible(self.COUPON_INPUT)

    def enter_coupon_code(self, code: str):
        # 1) normal typing
        self.type(self.COUPON_INPUT, code)

        # 2) verify value, fallback to JS
        current = self.value_of(self.COUPON_INPUT).strip()
        if not current:
            self.set_value_js(self.COUPON_INPUT, code)

        return self

    def is_check_button_present(self) -> bool:
        return self.is_present(self.CHECK_BUTTON)

    def is_check_button_enabled(self) -> bool:
        if not self.is_present(self.CHECK_BUTTON):
            return False

        disabled_attr = self.attr(self.CHECK_BUTTON, "disabled")
        aria_disabled = self.attr(self.CHECK_BUTTON, "aria-disabled")

        if disabled_attr is not None:
            return False
        if aria_disabled is not None and aria_disabled.lower() == "true":
            return False

        return self.is_enabled(self.CHECK_BUTTON)

    def wait_and_click_check(self, wait_seconds: float = 1.0):
        time.sleep(wait_seconds)
        self.click_present(self.CHECK_BUTTON)
        return self
