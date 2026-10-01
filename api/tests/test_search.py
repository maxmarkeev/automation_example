import allure
import pytest

from api.models.responses import ProductsListResponse

VALID_QUERIES = ["top", "dress", "shirt"]


@allure.feature("Search Product")
class TestSearchProduct:


    @allure.title("Returns results for query: {query}")
    @pytest.mark.smoke
    @pytest.mark.api
    @pytest.mark.parametrize("query", VALID_QUERIES)
    def test_returns_results_for_query(self, products_service, query, soft):
        result = products_service.search_product(query)

        soft.check(isinstance(result, ProductsListResponse), "response type mismatch")
        soft.check(result.response_code == 200, f"expected 200, got {result.response_code}")
        soft.check(len(result.products) > 0, f"no results for query '{query}'")

    @allure.title("Search is case-insensitive: {query}")
    @pytest.mark.regression
    @pytest.mark.api
    @pytest.mark.parametrize("query", ["TOP", "Dress", "SHIRT"])
    def test_case_insensitive(self, products_service, query):
        lower = products_service.search_product(query.lower())
        mixed = products_service.search_product(query)

        assert len(lower.products) == len(mixed.products)
