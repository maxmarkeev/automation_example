import allure

from api.models.requests import UserCreateRequest
from api.models.responses import BaseApiResponse, UserDetailResponse
from api.services.base_service import BaseService


class UsersService(BaseService):
    @allure.step("Verify login: {email}")
    def verify_login(self, email: str, password: str) -> dict:
        wrapper = self._wrap(
            self._client.post("/api/verifyLogin", data={"email": email, "password": password})
        )
        return wrapper.raw_json()

    @allure.step("Verify login without password")
    def verify_login_no_password(self, email: str) -> dict:
        wrapper = self._wrap(
            self._client.post("/api/verifyLogin", data={"email": email})
        )
        return wrapper.raw_json()

    @allure.step("Create account")
    def create_account(self, request: UserCreateRequest) -> BaseApiResponse:
        wrapper = self._wrap(
            self._client.post(
                "/api/createAccount",
                data=request.model_dump(exclude_none=True),
            )
        )
        self.check_status(wrapper, 201)
        return wrapper.json_wrapper(BaseApiResponse)

    @allure.step("Delete account: {email}")
    def delete_account(self, email: str, password: str) -> BaseApiResponse:
        wrapper = self._wrap(
            self._client.delete(
                "/api/deleteAccount",
                data={"email": email, "password": password},
            )
        )
        self.check_status(wrapper, 200)
        return wrapper.json_wrapper(BaseApiResponse)

    @allure.step("Update account")
    def update_account(self, request: UserCreateRequest) -> BaseApiResponse:
        wrapper = self._wrap(
            self._client.put(
                "/api/updateAccount",
                data=request.model_dump(exclude_none=True),
            )
        )
        self.check_status(wrapper, 200)
        return wrapper.json_wrapper(BaseApiResponse)

    @allure.step("Get user by email: {email}")
    def get_user_by_email(self, email: str) -> UserDetailResponse:
        wrapper = self._wrap(
            self._client.get("/api/getUserDetailByEmail", params={"email": email})
        )
        self.check_status(wrapper, 200)
        return wrapper.json_wrapper(UserDetailResponse)
