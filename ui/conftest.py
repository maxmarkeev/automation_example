import os
from collections.abc import Generator

import allure
import pytest
from playwright.sync_api import Page

from api.configs.config import load_config
from api.connections.client import BaseClient
from api.models.factories import UserFactory
from api.models.requests import UserCreateRequest
from api.services.users_service import UsersService
from ui.pages.account_page import AccountPage
from ui.pages.cart_page import CartPage
from ui.pages.checkout_page import CheckoutPage
from ui.pages.contact_page import ContactPage
from ui.pages.home_page import HomePage
from ui.pages.products_page import ProductsPage
from ui.pages.signup_login_page import SignupLoginPage


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    # Headless in CI.
    return {**browser_type_launch_args, "headless": os.environ.get("CI") == "true"}


@pytest.fixture(scope="session")
def base_url() -> str:
    return load_config().base_url


@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def signup_login_page(page: Page) -> SignupLoginPage:
    return SignupLoginPage(page)


@pytest.fixture
def account_page(page: Page) -> AccountPage:
    return AccountPage(page)


@pytest.fixture
def products_page(page: Page) -> ProductsPage:
    return ProductsPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def contact_page(page: Page) -> ContactPage:
    return ContactPage(page)


@pytest.fixture(scope="module")
def registered_user_api() -> Generator[UserCreateRequest, None, None]:
    client = BaseClient(load_config())
    service = UsersService(client)
    user = UserFactory.build()
    service.create_account(user)
    yield user
    service.delete_account(user.email, user.password)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page: Page | None = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="failure screenshot",
                attachment_type=allure.attachment_type.PNG,
            )

