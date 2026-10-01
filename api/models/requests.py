from pydantic import BaseModel


class SearchProductRequest(BaseModel):
    search_product: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserCreateRequest(BaseModel):
    name: str
    email: str
    password: str
    title: str = "Mr"
    birth_date: str = "1"
    birth_month: str = "1"
    birth_year: str = "1990"
    firstname: str
    lastname: str
    company: str | None = None
    address1: str
    address2: str | None = None
    country: str = "United States"
    zipcode: str
    state: str
    city: str
    mobile_number: str
