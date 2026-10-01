import allure
from playwright.sync_api import Page

from api.models.requests import UserCreateRequest
from ui.pages.base_page import BasePage


class AccountPage(BasePage):
    """Registration details form at /signup. Reached after start_signup on SignupLoginPage."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self._mr_radio = page.locator('input[type="radio"][value="Mr"]')
        self._mrs_radio = page.locator('input[type="radio"][value="Mrs"]')
        self._password = page.locator('input[data-qa="password"]')
        self._days = page.locator('select[data-qa="days"]')
        self._months = page.locator('select[data-qa="months"]')
        self._years = page.locator('select[data-qa="years"]')
        self._firstname = page.locator('input[data-qa="first_name"]')
        self._lastname = page.locator('input[data-qa="last_name"]')
        self._company = page.locator('input[data-qa="company"]')
        self._address1 = page.locator('input[data-qa="address"]')
        self._address2 = page.locator('input[data-qa="address2"]')
        self._country = page.locator('select[data-qa="country"]')
        self._state = page.locator('input[data-qa="state"]')
        self._city = page.locator('input[data-qa="city"]')
        self._zipcode = page.locator('input[data-qa="zipcode"]')
        self._mobile = page.locator('input[data-qa="mobile_number"]')
        self._create_btn = page.locator('button[data-qa="create-account"]')
        self._account_created_heading = page.get_by_text("Account Created!")

    @allure.step("Fill registration form")
    def fill_registration_form(self, user: UserCreateRequest) -> None:
        if user.title == "Mrs":
            self._mrs_radio.check()
        else:
            self._mr_radio.check()
        self._password.fill(user.password)
        self._days.select_option(user.birth_date)
        self._months.select_option(user.birth_month)
        self._years.select_option(user.birth_year)
        self._firstname.fill(user.firstname)
        self._lastname.fill(user.lastname)
        if user.company:
            self._company.fill(user.company)
        self._address1.fill(user.address1)
        if user.address2:
            self._address2.fill(user.address2)
        self._country.select_option(user.country)
        self._state.fill(user.state)
        self._city.fill(user.city)
        self._zipcode.fill(user.zipcode)
        self._mobile.fill(user.mobile_number)

    @allure.step("Submit registration form")
    def submit(self) -> None:
        self._create_btn.click()

    @allure.step("Check account created message is visible")
    def account_created_visible(self) -> bool:
        return self._account_created_heading.is_visible()
