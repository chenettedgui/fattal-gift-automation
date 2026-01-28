from urllib.parse import urlparse

from src.core.config import TIMEOUT
from src.core.waits import wait_visible, wait_clickable, wait_present


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url: str):
        self.driver.get(url)
        return self

    def open_with_basic_auth(self, url: str, username: str, password: str):
        parsed = urlparse(url)

        auth_url = (
            f"{parsed.scheme}://{username}:{password}@"
            f"{parsed.netloc}{parsed.path or ''}"
        )
        if parsed.query:
            auth_url += f"?{parsed.query}"
        if parsed.fragment:
            auth_url += f"#{parsed.fragment}"

        self.driver.get(auth_url)
        return self

    def click(self, locator):
        wait_clickable(self.driver, locator, TIMEOUT).click()
        return self

    def click_present(self, locator):
        """Click element even if Selenium doesn't classify it as 'clickable' (useful for div/a buttons)."""
        el = wait_present(self.driver, locator, TIMEOUT)
        el.click()
        return self

    def type(self, locator, text: str, clear: bool = True):
        el = wait_visible(self.driver, locator, TIMEOUT)
        try:
            el.click()
        except Exception:
            pass

        if clear:
            try:
                el.clear()
            except Exception:
                # fallback to JS clear
                self.driver.execute_script("arguments[0].value = '';", el)

        el.send_keys(text)
        return self

    def set_value_js(self, locator, value: str):
        """
        JS fallback: sets value and triggers input/change events
        (important when UI enables buttons only after events).
        """
        el = wait_present(self.driver, locator, TIMEOUT)
        self.driver.execute_script(
            """
            const el = arguments[0];
            const val = arguments[1];
            el.focus();
            el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            el,
            value
        )
        return self

    def find(self, locator):
        return wait_visible(self.driver, locator, TIMEOUT)

    def find_present(self, locator):
        return wait_present(self.driver, locator, TIMEOUT)

    def text_of(self, locator) -> str:
        return wait_visible(self.driver, locator, TIMEOUT).text

    def attr(self, locator, name: str):
        el = wait_present(self.driver, locator, TIMEOUT)
        return el.get_attribute(name)

    def value_of(self, locator) -> str:
        return self.attr(locator, "value") or ""

    def is_visible(self, locator) -> bool:
        try:
            wait_visible(self.driver, locator, TIMEOUT)
            return True
        except Exception:
            return False

    def is_present(self, locator) -> bool:
        try:
            wait_present(self.driver, locator, TIMEOUT)
            return True
        except Exception:
            return False

    def is_enabled(self, locator) -> bool:
        el = wait_present(self.driver, locator, TIMEOUT)
        return el.is_enabled()

    @property
    def current_url(self) -> str:
        return self.driver.current_url
