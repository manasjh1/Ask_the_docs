import os
from groq import Groq
from backend.app.config import settings

class GroqLLM:
    def __init__(self):
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not set")

        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Answer only using the given context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=25000,
        )
        return response.choices[0].message.content.strip()
