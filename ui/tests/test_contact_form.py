import allure
import pytest


@allure.feature("Contact Form")
class TestContactForm:
    @allure.title("Valid submission shows success message")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_valid_submission(self, contact_page):
        contact_page.open()
        contact_page.fill_form(
            name="Test User",
            email="test@example.com",
            subject="Portfolio test",
            message="This is an automated test message.",
        )
        contact_page.submit()

        assert contact_page.success_visible()

    @allure.title("Form is accessible from home page")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_accessible_from_home(self, home_page, contact_page):
        home_page.open()
        home_page.go_to_contact()

        assert contact_page.page.url.endswith("/contact_us")
