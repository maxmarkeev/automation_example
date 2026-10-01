from __future__ import annotations

from typing import TypeVar, Type

import requests as _requests
from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T", bound=BaseModel)


class BaseApiResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    response_code: int = Field(validation_alias="responseCode")
    message: str = ""


class ErrorResponse(BaseApiResponse):
    pass


class ResponseWrapper:
    def __init__(self, response: _requests.Response) -> None:
        self._response = response

    @property
    def http_status(self) -> int:
        return self._response.status_code

    def json_wrapper(self, model: Type[T]) -> T:
        return model.model_validate(self._response.json())

    def raw_json(self) -> dict:
        return self._response.json()


# --- Product domain ---

class UserType(BaseModel):
    usertype: str


class Category(BaseModel):
    usertype: UserType
    category: str


class Product(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: int
    name: str
    price: str
    brand: str
    category: Category


class Brand(BaseModel):
    id: int
    brand: str


class ProductsListResponse(BaseApiResponse):
    products: list[Product] = Field(default_factory=list)


class BrandsListResponse(BaseApiResponse):
    brands: list[Brand] = Field(default_factory=list)


# --- User domain ---

class UserDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: int
    name: str
    email: str
    title: str = ""
    birth_day: str = ""
    birth_month: str = ""
    birth_year: str = ""
    first_name: str = ""
    last_name: str = ""
    company: str = ""
    address1: str = ""
    address2: str = ""
    country: str = ""
    state: str = ""
    city: str = ""
    zipcode: str = ""


class UserDetailResponse(BaseApiResponse):
    user: UserDetail
