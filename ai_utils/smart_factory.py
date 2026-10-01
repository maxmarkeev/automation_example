import json
import os

from anthropic import Anthropic


class SmartFactory:
    """Generates edge case test data via Claude instead of hand-crafting them."""

    _PROMPT = (
        "Generate {count} edge case test inputs for: {description}. "
        "Cover boundary values, special characters, empty strings, max length. "
        "Return a JSON array of objects only, no explanation."
    )

    def __init__(self) -> None:
        self._client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def generate_edge_cases(self, description: str, count: int = 5) -> list[dict]:
        response = self._client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": self._PROMPT.format(count=count, description=description),
                }
            ],
        )
        return json.loads(response.content[0].text)
