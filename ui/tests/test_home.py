import allure
import pytest

from ui.pages.home_page import HomePage


@allure.feature("Home Page")
class TestHomePage:
    @allure.title("Loads and logo is visible")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_loads(self, home_page):
        home_page.open()

        assert home_page.is_loaded()

    @allure.title("Navigation links are visible")
    @pytest.mark.ui
    def test_nav_links_visible(self, home_page):
        home_page.open()

        assert home_page.nav_links_visible()

    @allure.title("Footer subscription shows success message")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_subscription_valid_email(self, home_page):
        home_page.open()
        home_page.subscribe("test_portfolio@example.com")

        assert home_page.subscription_success_message()

