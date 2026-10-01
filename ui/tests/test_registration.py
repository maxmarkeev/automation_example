import allure
import pytest

from api.configs.config import load_config
from api.connections.client import BaseClient
from api.models.factories import UserFactory
from api.services.users_service import UsersService
from ui.pages.account_page import AccountPage
from ui.pages.signup_login_page import SignupLoginPage


@allure.feature("Registration")
class TestRegistration:
    @allure.title("New user registers successfully")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_new_user_registers(self, signup_login_page, account_page):
        user = UserFactory.build()

        signup_login_page.open()
        signup_login_page.start_signup(user.name, user.email)
        account_page.fill_registration_form(user)
        account_page.submit()

        assert account_page.account_created_visible()

        UsersService(BaseClient(load_config())).delete_account(user.email, user.password)

    @allure.title("Existing email shows error message")
    @pytest.mark.ui
    def test_existing_email_shows_error(self, signup_login_page, registered_user_api):
        signup_login_page.open()
        signup_login_page.start_signup("Any Name", registered_user_api.email)

        assert signup_login_page.signup_error_visible()
