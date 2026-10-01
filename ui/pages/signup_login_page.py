import allure
from playwright.sync_api import Page

from ui.pages.base_page import BasePage


class SignupLoginPage(BasePage):
    PATH = "/login"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._login_email = page.locator('input[data-qa="login-email"]')
        self._login_password = page.locator('input[data-qa="login-password"]')
        self._login_btn = page.locator('button[data-qa="login-button"]')
        self._login_error = page.locator("p", has_text="Your email or password is incorrect")

        self._signup_name = page.locator('input[data-qa="signup-name"]')
        self._signup_email = page.locator('input[data-qa="signup-email"]')
        self._signup_btn = page.locator('button[data-qa="signup-button"]')
        self._signup_error = page.locator("p", has_text="Email Address already exist")

    @allure.step("Open login page")
    def open(self) -> "SignupLoginPage":
        self.navigate(self.PATH)
        return self

    @allure.step("Login with email: {email}")
    def login(self, email: str, password: str) -> None:
        self._login_email.fill(email)
        self._login_password.fill(password)
        self._login_btn.click()

    @allure.step("Start signup for: {name}")
    def start_signup(self, name: str, email: str) -> None:
        self._signup_name.fill(name)
        self._signup_email.fill(email)
        self._signup_btn.click()

    @allure.step("Check login error is visible")
    def login_error_visible(self) -> bool:
        return self._login_error.is_visible()

    @allure.step("Check signup error is visible")
    def signup_error_visible(self) -> bool:
        return self._signup_error.is_visible()
