import json

from ollama import chat

from config import OLLAMA_MODEL
from prompts import SYSTEM_PROMPT


class LLM:

    def __init__(self):
        self.model = OLLAMA_MODEL

    def process(self, command: str) -> dict:
        """
        Sends the user's command to Ollama and
        returns the parsed JSON response.
        """

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": command
                }
            ]
        )

        result = response["message"]["content"].strip()

        # Extract JSON safely
        start = result.find("{")
        end = result.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("No valid JSON returned by the LLM.")

        result = result[start:end]

        return json.loads(result)
