from typing import Optional
import httpx


class OpenAIProvider:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"

    async def generate_candidate_summary(self, candidate_data: dict) -> str:
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        prompt = f"""
        Based on the following candidate information, provide a brief professional summary for recruitment purposes:
        
        Name: {candidate_data.get('first_name', '')} {candidate_data.get('last_name', '')}
        Email: {candidate_data.get('email', '')}
        Source: {candidate_data.get('source', 'Unknown')}
        
        Provide a concise summary highlighting potential strengths and fit for a professional role.
        Keep it under 150 words.
        """

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 200,
            "temperature": 0.7,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=10.0,
            )
            
            if response.status_code != 200:
                raise Exception(f"OpenAI API error: {response.status_code}")
            
            data = response.json()
            return data["choices"][0]["message"]["content"]
