import allure
from playwright.sync_api import Page

from ui.pages.base_page import BasePage


class ProductsPage(BasePage):
    PATH = "/products"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._search_input = page.locator("#search_product")
        self._search_btn = page.locator("#submit_search")
        self._product_cards = page.locator(".features_items .productinfo")
        self._add_to_cart_btns = page.locator(".features_items .productinfo .add-to-cart")
        # Post-add-to-cart modal
        self._modal_continue = page.locator("button.close-modal")
        self._modal_view_cart = page.locator("a.view_cart")
        # Sidebar filters
        self._category_links = page.locator("#accordian .panel-body ul li a")
        self._brand_links = page.locator(".brands_products .brands-name li a")

    @allure.step("Open products page")
    def open(self) -> "ProductsPage":
        self.navigate(self.PATH)
        return self

    @allure.step("Get product count")
    def get_product_count(self) -> int:
        return self._product_cards.count()

    @allure.step("Search product: {query}")
    def search(self, query: str) -> None:
        self._search_input.fill(query)
        self._search_btn.click()

    @allure.step("Add product to cart (index {index})")
    def add_product_to_cart(self, index: int = 0) -> None:
        self._add_to_cart_btns.nth(index).click()
        self._modal_continue.wait_for()

    @allure.step("Continue shopping from modal")
    def continue_shopping(self) -> None:
        self._modal_continue.click()

    @allure.step("View cart from modal")
    def go_to_cart_from_modal(self) -> None:
        self._modal_view_cart.click()

    @allure.step("Filter by category: {name}")
    def filter_by_category(self, name: str) -> None:
        self._category_links.filter(has_text=name).first.click()

    @allure.step("Filter by brand: {name}")
    def filter_by_brand(self, name: str) -> None:
        self._brand_links.filter(has_text=name).first.click()
