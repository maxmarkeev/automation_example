from uuid import uuid4

from faker import Faker

from api.models.requests import UserCreateRequest

_fake = Faker()


class ProductSearchFactory:
    @staticmethod
    def valid_query() -> str:
        # "jeans" and "skirt" return 0 results on this site - confirmed empirically.
        return _fake.random_element(["top", "dress", "shirt"])

    @staticmethod
    def empty_query() -> str:
        return ""


class PaymentFactory:
    @staticmethod
    def build() -> dict:
        return {
            "name": _fake.name(),
            "card_number": "4111111111111111",
            "cvc": _fake.numerify("###"),
            "expiry_month": _fake.numerify("##"),
            "expiry_year": "2027",
        }


class UserFactory:
    @staticmethod
    def build() -> UserCreateRequest:
        first = _fake.first_name()
        last = _fake.last_name()
        return UserCreateRequest(
            name=f"{first} {last}",
            email=f"qa_{uuid4().hex[:8]}@test.com",
            password=_fake.password(length=12, special_chars=False),
            title=_fake.random_element(["Mr", "Mrs"]),
            birth_date=str(_fake.random_int(1, 28)),
            birth_month=str(_fake.random_int(1, 12)),
            birth_year=str(_fake.random_int(1970, 2000)),
            firstname=first,
            lastname=last,
            address1=_fake.street_address(),
            country="United States",
            zipcode=_fake.zipcode(),
            state=_fake.state(),
            city=_fake.city(),
            mobile_number=_fake.numerify("##########"),
        )
