from agents import Agent
from agent.llm_connection import get_gemini
from agent.ml_model_discovery_agent import ml_model_discovery_agent
from agent.action_recommendation_agent import action_recommendation_agent


AGENT_NAME = "controller_agent"


controller_agent = Agent(
    name=AGENT_NAME,
    instructions=f"""
    Your role is to recommend a campaign based on the user prompt.  
    1. Use agent as tool to get info of useful machine learning (ML) models from the model registry.
    2. Based on the result of step 1, use agent as tool to obtain feasible actions.
    3. Based on the results of step 1 and 2, recommend a campaign.
    If step 1 or 2 returns no results, do not recommend anything and stop.
    """,
    tools=[ml_model_discovery_agent.as_tool(
            tool_name="ml_model_discovery_agent",
            tool_description="Find Machine Learning models in the model registry that are useful based on the user prompt.",
        ),
        action_recommendation_agent.as_tool(
            tool_name="action_recommendation_agent",
            tool_description="Recommend feasible actions from the action space based on the user prompt."
        )],
    model=get_gemini(),
)

