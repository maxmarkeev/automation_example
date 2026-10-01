import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    base_url: str
    timeout: int


def load_config() -> Config:
    return Config(
        base_url=os.environ.get("BASE_URL", "https://automationexercise.com"),
        timeout=int(os.environ.get("REQUEST_TIMEOUT", "30")),
    )
