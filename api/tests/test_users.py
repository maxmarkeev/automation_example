import allure
import pytest

from api.models.factories import UserFactory
from api.models.responses import BaseApiResponse, UserDetailResponse


@allure.feature("Create Account")
class TestCreateAccount:

    @allure.title("Creates new user successfully")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_creates_new_user(self, users_service):
        user = UserFactory.build()
        result = users_service.create_account(user)
        users_service.delete_account(user.email, user.password)

        assert isinstance(result, BaseApiResponse)
        assert result.response_code == 201


@allure.feature("Delete Account")
class TestDeleteAccount:
    @allure.title("Removes user successfully")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_removes_user(self, users_service):
        user = UserFactory.build()
        users_service.create_account(user)
        result = users_service.delete_account(user.email, user.password)

        assert result.response_code == 200


@allure.feature("Verify Login")
class TestVerifyLogin:
    @allure.title("Valid credentials return 200")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_valid_credentials(self, users_service, registered_user, soft):
        body = users_service.verify_login(registered_user.email, registered_user.password)

        soft.has_response_code(body, 200)
        soft.message_contains(body, "exists")

    @allure.title("Wrong password returns 404")
    @pytest.mark.api
    def test_wrong_password_returns_404(self, users_service, registered_user):
        body = users_service.verify_login(registered_user.email, "wrong_password_000")

        assert body["responseCode"] == 404

    @allure.title("Missing password returns 400")
    @pytest.mark.api
    def test_missing_password_returns_400(self, users_service, registered_user):
        body = users_service.verify_login_no_password(registered_user.email)

        assert body["responseCode"] == 400


@allure.feature("Update Account")
class TestUpdateAccount:
    @allure.title("Updates user data successfully")
    @pytest.mark.api
    def test_updates_user_data(self, users_service, registered_user):
        updated = registered_user.model_copy(update={"city": "New York", "state": "New York"})
        result = users_service.update_account(updated)

        assert result.response_code == 200


@allure.feature("Get User Detail")
class TestGetUserDetail:
    @allure.title("Returns correct user by email")
    @pytest.mark.api
    def test_returns_correct_user(self, users_service, registered_user, soft):
        result = users_service.get_user_by_email(registered_user.email)

        assert isinstance(result, UserDetailResponse)
        soft.check(result.user.email == registered_user.email, "email should match")
        soft.check(result.user.name == registered_user.name, "name should match")
