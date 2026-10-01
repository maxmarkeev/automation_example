import allure
from playwright.sync_api import Page

from ui.pages.base_page import BasePage


class ContactPage(BasePage):
    PATH = "/contact_us"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._name = page.locator('input[data-qa="name"]')
        self._email = page.locator('input[data-qa="email"]')
        self._subject = page.locator('input[data-qa="subject"]')
        self._message = page.locator('textarea[data-qa="message"]')
        self._submit_btn = page.locator('input[data-qa="submit-button"]')
        self._success_msg = page.locator(".status.alert-success")

    @allure.step("Open contact page")
    def open(self) -> "ContactPage":
        self.navigate(self.PATH)
        return self

    @allure.step("Fill contact form")
    def fill_form(self, name: str, email: str, subject: str, message: str) -> None:
        self._name.fill(name)
        self._email.fill(email)
        self._subject.fill(subject)
        self._message.fill(message)

    @allure.step("Submit contact form")
    def submit(self) -> None:
        # Site shows a JS confirm dialog on submit — accept it automatically.
        self.page.once("dialog", lambda dialog: dialog.accept())
        self._submit_btn.click()

    @allure.step("Check success message is visible")
    def success_visible(self) -> bool:
        self._success_msg.wait_for()
        return self._success_msg.is_visible()
