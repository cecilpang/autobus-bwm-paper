import asyncio
from agent.agent_session import WorkflowContext, AgentSession
from agent.planner_agent import AGENT_NAME, planner_agent
from agents import set_tracing_disabled 

"""
Task: Recommend churn reduction campaign.
"""

async def main():
        # Do not send tracing data to OpenAI
        set_tracing_disabled(True)

        task_instruction = """
            Reduce the overall churn rate of subscribers by 2%. 
            Target no more than 2000 subscribers and total monthly revuenue must not decline by more than $20000
        """

        agent_session = AgentSession(AGENT_NAME, WorkflowContext(), planner_agent)
        r = await agent_session.run(task_instruction)
        print(r)

if __name__ == "__main__":
    asyncio.run(main())