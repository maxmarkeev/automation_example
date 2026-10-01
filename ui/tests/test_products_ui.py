import allure
import pytest

from ui.pages.products_page import ProductsPage


@allure.feature("Products Page")
class TestProductsPage:
    @allure.title("Loads with non-empty product list")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_loads_with_products(self, products_page):
        products_page.open()

        assert products_page.get_product_count() > 0

    @allure.title("Search by valid query returns results")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_search_returns_results(self, products_page):
        products_page.open()
        products_page.search("top")

        assert products_page.get_product_count() > 0

    @allure.title("Filter by category shows results")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_filter_by_category(self, products_page):
        products_page.open()
        products_page.filter_by_category("Dress")

        assert products_page.get_product_count() > 0

    @allure.title("Filter by brand shows results")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_filter_by_brand(self, products_page):
        products_page.open()
        products_page.filter_by_brand("Polo")

        assert products_page.get_product_count() > 0
