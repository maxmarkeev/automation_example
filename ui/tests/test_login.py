import allure
import pytest

from ui.pages.home_page import HomePage
from ui.pages.signup_login_page import SignupLoginPage


@allure.feature("Login / Logout")
class TestLogin:
    @allure.title("Valid credentials show logged in state")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_valid_credentials(self, signup_login_page, home_page, registered_user_api):
        signup_login_page.open()
        signup_login_page.login(registered_user_api.email, registered_user_api.password)

        assert home_page.is_logged_in()

    @allure.title("Logged in username matches registered name")
    @pytest.mark.ui
    def test_logged_in_name_matches(self, signup_login_page, home_page, registered_user_api):
        signup_login_page.open()
        signup_login_page.login(registered_user_api.email, registered_user_api.password)

        assert registered_user_api.name in home_page.get_logged_in_name()

    @allure.title("Wrong password shows error message")
    @pytest.mark.ui
    def test_wrong_password_shows_error(self, signup_login_page, registered_user_api):
        signup_login_page.open()
        signup_login_page.login(registered_user_api.email, "wrong_password_000")

        assert signup_login_page.login_error_visible()

    @allure.title("Logout redirects to login page")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_logout(self, signup_login_page, home_page, registered_user_api):
        signup_login_page.open()
        signup_login_page.login(registered_user_api.email, registered_user_api.password)
        home_page.logout()

        assert "/login" in home_page.page.url

