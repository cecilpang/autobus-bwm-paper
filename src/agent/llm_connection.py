import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled

def get_gemini() -> OpenAIChatCompletionsModel: 

    GEMINI_BASE_URL = os.getenv(
        "GEMINI_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    LLM = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    def _get_gemini_api_key() -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("Missing Gemini API key. Set GEMINI_API_KEY in .env ")
        return api_key

    gemini_client = AsyncOpenAI(
        api_key=_get_gemini_api_key(),
        base_url=GEMINI_BASE_URL,
    )

    gemini_model = OpenAIChatCompletionsModel(
        model=LLM,
        openai_client=gemini_client,
    )

    return gemini_model
