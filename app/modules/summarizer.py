import openai
import os

class SummarizerService:

    async def summarize(self, text: str):

        prompt = f"""
        Summarize the following document in 5-10 sentences:

        {text}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["choices"][0]["message"]["content"]