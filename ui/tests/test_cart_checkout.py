import allure
import pytest

from api.models.factories import PaymentFactory
from ui.pages.cart_page import CartPage
from ui.pages.checkout_page import CheckoutPage
from ui.pages.products_page import ProductsPage
from ui.pages.signup_login_page import SignupLoginPage


@allure.feature("Cart")
class TestCart:
    @allure.title("Add product to cart - appears in cart")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_add_product(self, products_page, cart_page):
        products_page.open()
        products_page.add_product_to_cart(index=0)
        products_page.go_to_cart_from_modal()

        assert cart_page.get_product_count() > 0

    @allure.title("Remove product leaves cart empty")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_remove_product(self, products_page, cart_page):
        products_page.open()
        products_page.add_product_to_cart(index=0)
        products_page.go_to_cart_from_modal()
        cart_page.remove_product(index=0)

        assert cart_page.is_empty()


@allure.feature("Checkout")
class TestCheckout:
    @allure.title("Registered user completes full checkout flow")
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_full_checkout_flow(self, signup_login_page, products_page, cart_page, checkout_page, registered_user_api):
        payment = PaymentFactory.build()

        signup_login_page.open()
        signup_login_page.login(registered_user_api.email, registered_user_api.password)

        products_page.open()
        products_page.add_product_to_cart(index=0)
        products_page.go_to_cart_from_modal()

        cart_page.proceed_to_checkout()

        checkout_page.place_order()
        checkout_page.fill_payment(
            name=payment["name"],
            card_number=payment["card_number"],
            cvc=payment["cvc"],
            expiry_month=payment["expiry_month"],
            expiry_year=payment["expiry_year"],
        )

        assert checkout_page.order_placed_visible()

    @allure.title("Checkout shows correct delivery address")
    @pytest.mark.regression
    @pytest.mark.ui
    def test_delivery_address(self, signup_login_page, products_page, cart_page, checkout_page, registered_user_api):
        signup_login_page.open()
        signup_login_page.login(registered_user_api.email, registered_user_api.password)

        products_page.open()
        products_page.add_product_to_cart(index=0)
        products_page.go_to_cart_from_modal()

        cart_page.proceed_to_checkout()

        assert registered_user_api.firstname in checkout_page.get_delivery_address()

