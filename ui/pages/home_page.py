import allure
from playwright.sync_api import Page

from ui.pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._logo = page.locator(".logo")
        self._nav_signup_login = page.get_by_role("link", name="Signup / Login")
        self._nav_products = page.get_by_role("link", name="Products")
        self._nav_cart = page.get_by_role("link", name="Cart")
        self._nav_contact = page.get_by_role("link", name="Contact us")
        # Site HTML has a typo in the id: "susbscribe_email"
        self._subscription_email = page.locator("#susbscribe_email")
        self._subscription_btn = page.locator("#subscribe")
        self._subscription_success = page.locator("#success-subscribe")
        self._logged_in_label = page.locator("li", has_text="Logged in as")
        self._logout_link = page.get_by_role("link", name="Logout")

    @allure.step("Open home page")
    def open(self) -> "HomePage":
        self.navigate(self.PATH)
        return self

    @allure.step("Check page is loaded")
    def is_loaded(self) -> bool:
        return self._logo.is_visible()

    @allure.step("Check navigation links are visible")
    def nav_links_visible(self) -> bool:
        return (
            self._nav_signup_login.is_visible()
            and self._nav_products.is_visible()
            and self._nav_cart.is_visible()
        )

    @allure.step("Go to Signup / Login")
    def go_to_signup_login(self) -> None:
        self._nav_signup_login.click()

    @allure.step("Go to Products")
    def go_to_products(self) -> None:
        self._nav_products.click()

    @allure.step("Go to Cart")
    def go_to_cart(self) -> None:
        self._nav_cart.click()

    @allure.step("Go to Contact Us")
    def go_to_contact(self) -> None:
        self._nav_contact.click()

    @allure.step("Subscribe with email: {email}")
    def subscribe(self, email: str) -> None:
        self._subscription_email.scroll_into_view_if_needed()
        self._subscription_email.fill(email)
        self._subscription_btn.click()

    @allure.step("Get subscription success message")
    def subscription_success_message(self) -> str:
        self._subscription_success.wait_for()
        return self._subscription_success.inner_text()

    @allure.step("Check user is logged in")
    def is_logged_in(self) -> bool:
        return self._logged_in_label.is_visible()

    @allure.step("Get logged in username")
    def get_logged_in_name(self) -> str:
        text = self._logged_in_label.inner_text()
        return text.replace("Logged in as", "").strip()

    @allure.step("Logout")
    def logout(self) -> None:
        self._logout_link.click()
