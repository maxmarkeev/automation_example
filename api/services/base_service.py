import requests

from api.connections.client import BaseClient
from api.models.responses import ResponseWrapper


class BaseService:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    @staticmethod
    def _wrap(response: requests.Response) -> ResponseWrapper:
        return ResponseWrapper(response)

    @staticmethod
    def check_status(wrapper: ResponseWrapper, expected: int) -> None:
        # This site often returns HTTP 200 even for errors.
        # Actual status lives in responseCode field (see AUDIT.md risk #1).
        body = wrapper.raw_json()
        actual = body.get("responseCode")
        assert actual == expected, (
            f"responseCode mismatch: expected {expected}, got {actual} "
            f"(HTTP {wrapper.http_status})"
        )
