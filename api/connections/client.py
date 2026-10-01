import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from api.configs.config import Config


class BaseClient:
    def __init__(self, config: Config) -> None:
        self._config = config
        self._session = self._build_session()

    def _build_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self._config.base_url}{path}"
        with allure.step(f"{method.upper()} {path}"):
            response = self._session.request(
                method, url, timeout=self._config.timeout, **kwargs
            )
            allure.attach(
                response.text,
                name="response body",
                attachment_type=allure.attachment_type.TEXT,
            )
        return response

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self._request("PUT", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._request("DELETE", path, **kwargs)
