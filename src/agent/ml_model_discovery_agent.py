from agents import Agent
from agents.tool import function_tool
from config import ML_MODELS_REGISTRY_PATH
from agent.llm_connection import get_gemini


AGENT_NAME = "ml_model_discovery_agent"


@function_tool
async def get_ml_models_info_from_registry() -> str:
    """
    Get information of the available ML models from the model registry.
    """
    template = None
    with open(ML_MODELS_REGISTRY_PATH, "r") as f:
        template = f.read()
    return template


ml_model_discovery_agent = Agent(
    name=AGENT_NAME,
    instructions=f"""
    Your role is to select machine learning (ML) models from the model registry 
    that can be used to plan actions that lead to the outcomes specified in the user prompt. 
    1. Use tool to retrive the names and descriptions of machine learning (ML) models from the model registry.
    2. Determine which of the ML models in the model registry would be useful.
    3. Output all the info found in the model registry.
    Do not suggest any models other than those in the registry. If the registry is not available, return the error message and stop.
    """,
    tools=[get_ml_models_info_from_registry],
    model=get_gemini(),
)

