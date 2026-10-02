import allure
from playwright.sync_api import Page

from ui.pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Covers /checkout (order review) and /payment (card form) steps."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # /checkout
        self._delivery_address = page.locator("#address_delivery")
        self._comment = page.locator("textarea.form-control")
        self._place_order_btn = page.locator("a.btn.check_out")
        # /payment
        self._name_on_card = page.locator('input[data-qa="name-on-card"]')
        self._card_number = page.locator('input[data-qa="card-number"]')
        self._cvc = page.locator('input[data-qa="cvc"]')
        self._expiry_month = page.locator('input[data-qa="expiry-month"]')
        self._expiry_year = page.locator('input[data-qa="expiry-year"]')
        self._pay_btn = page.locator('button[data-qa="pay-button"]')
        # /payment_done
        self._order_placed = page.get_by_text("Congratulations! Your order has been confirmed!")

    @allure.step("Get delivery address")
    def get_delivery_address(self) -> str:
        return self._delivery_address.inner_text()

    @allure.step("Place order")
    def place_order(self, comment: str = "") -> None:
        if comment:
            self._comment.fill(comment)
        self._place_order_btn.click()
        self.page.wait_for_load_state("load")

    @allure.step("Fill payment form")
    def fill_payment(
        self,
        name: str,
        card_number: str,
        cvc: str,
        expiry_month: str,
        expiry_year: str,
    ) -> None:
        self._name_on_card.fill(name)
        self._card_number.fill(card_number)
        self._cvc.fill(cvc)
        self._expiry_month.fill(expiry_month)
        self._expiry_year.fill(expiry_year)
        self._pay_btn.click()

    @allure.step("Check order placed message is visible")
    def order_placed_visible(self) -> bool:
        self._order_placed.wait_for(timeout=10000)
        return self._order_placed.is_visible()
