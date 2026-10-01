import allure
from playwright.sync_api import Page

from ui.pages.base_page import BasePage


class CartPage(BasePage):
    PATH = "/view_cart"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._rows = page.locator("#cart_info_table tbody tr")
        self._proceed_btn = page.locator("a.btn.check_out")
        self._empty_cart_msg = page.locator("#empty_cart")

    @allure.step("Open cart page")
    def open(self) -> "CartPage":
        self.navigate(self.PATH)
        return self

    @allure.step("Get cart product count")
    def get_product_count(self) -> int:
        return self._rows.count()

    @allure.step("Get product name (index {index})")
    def get_product_name(self, index: int = 0) -> str:
        return self._rows.nth(index).locator(".cart_description h4 a").inner_text()

    @allure.step("Get product price (index {index})")
    def get_product_price(self, index: int = 0) -> str:
        return self._rows.nth(index).locator(".cart_price p").inner_text()

    @allure.step("Remove product from cart (index {index})")
    def remove_product(self, index: int = 0) -> None:
        row = self._rows.nth(index)
        row.locator(".cart_quantity_delete").click()
        row.wait_for(state="hidden")

    @allure.step("Check cart is empty")
    def is_empty(self) -> bool:
        return self._rows.count() == 0

    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self) -> None:
        self._proceed_btn.click()
