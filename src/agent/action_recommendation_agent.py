from agents import Agent
from agents.tool import function_tool
from config import ACTION_SPACE_PATH
from agent.llm_connection import get_gemini


AGENT_NAME = "action_recommendation_agent"


@function_tool
async def get_action_space() -> str:
    """
    Get information of the available actions from the action space.
    """
    template = None
    with open(ACTION_SPACE_PATH, "r") as f:
        template = f.read()
    return template


action_recommendation_agent = Agent(
    name=AGENT_NAME,
    instructions=f"""
    Your role is to recommend actions based on the context given to you by the controller agent. 
    1. Use tool to retrive the feasible actions from the action space.
    2. Determine which of the actions would be useful.
    3. Output the selected actions and the reason they are useful.
    Do not suggest any actions other than those in the action space. 
    If the action space is not available, return the error message and stop.
    """,
    tools=[get_action_space],
    model=get_gemini(),
)

