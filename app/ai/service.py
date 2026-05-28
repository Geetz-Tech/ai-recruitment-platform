from ..core.config import settings
from .mock_provider import MockAIProvider
from .openai_provider import OpenAIProvider


class AIService:
    def __init__(self):
        if settings.ai_provider == "openai":
            self.provider = OpenAIProvider(
                api_key=settings.openai_api_key,
                model=settings.openai_model,
            )
        else:
            self.provider = MockAIProvider()

    async def generate_candidate_summary(self, candidate_data: dict) -> str:
        if settings.ai_provider == "openai":
            return await self.provider.generate_candidate_summary(candidate_data)
        else:
            return self.provider.generate_candidate_summary(candidate_data)


ai_service = AIService()
