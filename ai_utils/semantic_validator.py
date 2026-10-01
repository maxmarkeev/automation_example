import json
import os

from anthropic import Anthropic


class SemanticValidator:
    """Checks if an API response makes semantic sense for a given behavior."""

    _PROMPT = (
        "Expected behavior: {expected}\n"
        "Actual response: {response}\n\n"
        'Does the response match the expected behavior? Reply with JSON only: {{"valid": true/false, "reason": "..."}}'
    )

    def __init__(self) -> None:
        self._client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def validate(self, expected_behavior: str, actual_response: dict) -> tuple[bool, str]:
        """Returns (is_valid, reason)."""
        msg = self._client.messages.create(
            model="claude-opus-4-6",
            max_tokens=256,
            messages=[
                {"role": "user","content": self._PROMPT.format(
                    expected=expected_behavior,
                    response=json.dumps(actual_response))}
            ]
        )
        result = json.loads(msg.content[0].text)
        return result["valid"], result["reason"]

