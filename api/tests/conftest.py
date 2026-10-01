from collections.abc import Generator

import pytest

from api.configs.config import load_config
from api.connections.client import BaseClient
from api.models.factories import UserFactory
from api.models.requests import UserCreateRequest
from api.services.products_service import ProductsService
from api.services.users_service import UsersService


@pytest.fixture(scope="session")
def api_client() -> BaseClient:
    return BaseClient(load_config())


@pytest.fixture(scope="session")
def products_service(api_client: BaseClient) -> ProductsService:
    return ProductsService(api_client)


@pytest.fixture(scope="session")
def users_service(api_client: BaseClient) -> UsersService:
    return UsersService(api_client)


@pytest.fixture
def registered_user(users_service: UsersService) -> Generator[UserCreateRequest, None, None]:
    user = UserFactory.build()
    users_service.create_account(user)
    yield user
    users_service.delete_account(user.email, user.password)
