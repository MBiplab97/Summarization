import ollama
import os

class SummarizerService:

    def __init__(self, model: str = "llama3.2-vision"):
        self.model = model
        self.client = ollama.Client()

    async def summarize(self, text: str):
        """Summarize text using Ollama Python client"""
        
        prompt = f"""Summarize the following document in 5-10 sentences:

                    {text}

                    Summary:"""

        try:
            response = self.client.generate(model=self.model, prompt=prompt)
            return response.get("response", "No summary generated")
        
        except ConnectionError:
            return f"❌ Error: Could not connect to Ollama. Make sure Ollama is running with: ollama serve"
        except Exception as e:
            return f"❌ Error summarizing text: {str(e)}"