import allure

from api.models.responses import BrandsListResponse, ProductsListResponse
from api.services.base_service import BaseService


class ProductsService(BaseService):
    @allure.step("Get all products")
    def get_all_products(self) -> ProductsListResponse:
        wrapper = self._wrap(self._client.get("/api/productsList"))
        self.check_status(wrapper, 200)
        return wrapper.json_wrapper(ProductsListResponse)

    @allure.step("Get all brands")
    def get_all_brands(self) -> BrandsListResponse:
        wrapper = self._wrap(self._client.get("/api/brandsList"))
        self.check_status(wrapper, 200)
        return wrapper.json_wrapper(BrandsListResponse)

    @allure.step("Search product: {query}")
    def search_product(self, query: str) -> ProductsListResponse:
        wrapper = self._wrap(
            self._client.post("/api/searchProduct", data={"search_product": query})
        )
        self.check_status(wrapper, 200)
        return wrapper.json_wrapper(ProductsListResponse)

    @allure.step("Search product without required param")
    def search_product_no_param(self) -> dict:
        # Expected responseCode 400 in body; HTTP status may still be 200.
        wrapper = self._wrap(self._client.post("/api/searchProduct"))
        return wrapper.raw_json()
