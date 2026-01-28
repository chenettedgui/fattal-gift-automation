import pytest

from src.core.driver_factory import create_driver
from src.pages.home_page import HomePage


@pytest.fixture
def driver():
    driver = create_driver()
    yield driver
    driver.quit()


def test_home_page_loads_with_basic_auth(driver):
    home = HomePage(driver).load()

    assert home.is_loaded(), "Home page did not load"
    assert "fattal" in home.current_url.lower()
