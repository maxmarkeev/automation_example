import allure
import pytest

from api.models.factories import ProductSearchFactory
from api.models.responses import BrandsListResponse, ProductsListResponse


@allure.feature("Products List")
class TestProductsList:
    @allure.title("Returns non-empty list")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_returns_non_empty_list(self, products_service):
        result = products_service.get_all_products()

        assert isinstance(result, ProductsListResponse)
        assert len(result.products) > 0

    @allure.title("Each product has required fields")
    @pytest.mark.api
    def test_product_schema_is_valid(self, products_service, soft):
        product = products_service.get_all_products().products[0]

        soft.check(product.id > 0, "id should be positive")
        soft.check(bool(product.name), "name should not be empty")
        soft.check(bool(product.price), "price should not be empty")
        soft.check(bool(product.brand), "brand should not be empty")
        soft.check(bool(product.category.category), "category should not be empty")


@allure.feature("Brands List")
class TestBrandsList:
    @allure.title("Returns non-empty list")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_returns_non_empty_list(self, products_service):
        result = products_service.get_all_brands()

        assert isinstance(result, BrandsListResponse)
        assert len(result.brands) > 0


@allure.feature("Search Product")
class TestSearchProduct:
    @allure.title("Valid query returns results")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_valid_query_returns_results(self, products_service):
        result = products_service.search_product(ProductSearchFactory.valid_query())

        assert isinstance(result, ProductsListResponse)
        assert len(result.products) > 0

    @allure.title("Missing param returns responseCode 400")
    @pytest.mark.api
    def test_missing_param_returns_400(self, products_service):
        # HTTP status may be 200 (site quirk, AUDIT.md risk #1).
        body = products_service.search_product_no_param()

        assert body["responseCode"] == 400
        assert "missing" in body.get("message", "").lower()
