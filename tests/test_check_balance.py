import time

from src.pages.home_page import HomePage
from src.data.test_data import COUPON_CODE


def test_check_balance_button_enabled_after_code(driver):
    assert COUPON_CODE != "", "TEST_COUPON_CODE is missing/empty in .env"

    home = HomePage(driver).load()
    assert home.is_loaded(), "Home page did not load"

    modal = home.open_check_balance_modal()
    assert modal.is_open(), "Balance popup did not open"

    modal.enter_coupon_code(COUPON_CODE)

    typed = modal.value_of(modal.COUPON_INPUT).strip()
    assert typed == COUPON_CODE, f"Typed '{typed}' != ENV '{COUPON_CODE}'"

    assert modal.is_check_button_present(), "Check button not found in modal"
    assert modal.is_check_button_enabled(), "Check button is not enabled after entering coupon code"

    modal.wait_and_click_check(wait_seconds=1.0)

    # optional: keep browser open briefly for debugging
    time.sleep(2)
