import os
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled

def get_gemini() -> OpenAIChatCompletionsModel: 

    GEMINI_API_KEY_ENV = "GEMINI_API_KEY"
    GEMINI_BASE_URL = os.getenv(
        "GEMINI_BASE_URL",
        "https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    LLM = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    AGENT_NAME = "ml_model_discovery_agent"


    def _get_gemini_api_key() -> str:
        api_key = os.getenv(GEMINI_API_KEY_ENV)
        if not api_key:
            raise RuntimeError(
                f"Set {GEMINI_API_KEY_ENV} before importing {__name__}; "
                "the Gemini OpenAI-compatible endpoint must not use OPENAI_API_KEY."
            )
        return api_key


    if not os.getenv("OPENAI_API_KEY"):
        set_tracing_disabled(disabled=True)

    gemini_client = AsyncOpenAI(
        api_key=_get_gemini_api_key(),
        base_url=GEMINI_BASE_URL,
    )

    gemini_model = OpenAIChatCompletionsModel(
        model=LLM,
        openai_client=gemini_client,
    )

    return gemini_model
