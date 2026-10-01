from __future__ import annotations


class AssertionHelper:
    """Assertion helper available as a pytest fixture called `soft`.

    soft.check()             - soft assertion (collected, raised at teardown)
    soft.has_response_code() - hard assertion on raw API response dict
    soft.message_contains()  - hard assertion on raw API response dict
    soft.has_key()           - hard assertion on raw API response dict
    """

    def __init__(self) -> None:
        self._failures: list[str] = []

    def check(self, condition: bool, message: str) -> AssertionHelper:
        if not condition:
            self._failures.append(message)
        return self

    def assert_all(self) -> None:
        if self._failures:
            n = len(self._failures)
            details = "\n  ".join(self._failures)
            raise AssertionError(f"{n} check(s) failed:\n  {details}")


    def has_response_code(self, body: dict, expected: int) -> AssertionHelper:
        actual = body.get("responseCode")
        assert actual == expected, f"response_code: expected {expected}, got {actual}"
        return self

    def message_contains(self, body: dict, text: str) -> AssertionHelper:
        msg = body.get("message", "")
        assert text.lower() in msg.lower(), (
            f"Expected message to contain '{text}', got: '{msg}'"
        )
        return self

    def has_key(self, body: dict, key: str) -> AssertionHelper:
        assert key in body, f"Response missing key: '{key}'"
        return self

    def __enter__(self) -> AssertionHelper:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.assert_all()


def has_response_code(body: dict, expected: int) -> None:
    actual = body.get("responseCode")
    assert actual == expected, f"responseCode: expected {expected}, got {actual}"


def message_contains(body: dict, text: str) -> None:
    msg = body.get("message", "")
    assert text.lower() in msg.lower(), (
        f"Expected message to contain '{text}', got: '{msg}'"
    )


def has_key(body: dict, key: str) -> None:
    assert key in body, f"Response missing key: '{key}'"


def key_is_not_empty(body: dict, key: str) -> None:
    value = body.get(key)
    assert value, f"Expected '{key}' to be non-empty, got: {value!r}"

