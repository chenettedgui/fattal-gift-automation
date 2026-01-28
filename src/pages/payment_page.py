from src.pages.base_page import BasePage

class PaymentPage(BasePage):
    # Payment pages often use iframes / external providers.
    # Keep this page minimal and implement provider-specific logic later.
    def pay_mock(self):
        # TODO: Implement sandbox/mock payment if available
        return self
