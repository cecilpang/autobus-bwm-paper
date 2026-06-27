import asyncio
from agents import gen_trace_id, trace
from agent.agent_session import WorkflowContext, AgentSession
from agent.controller_agent import AGENT_NAME, controller_agent

"""
Task 1: Identify potentially savable churns.
"""

async def main():

        task_instruction = """
            Reduce the overall churn rate of subscribers by 2%. 
            Target no more than 2000 subscribers and total monthly revuenue must not decline by more than $20000
        """

        agent_session = AgentSession(AGENT_NAME, WorkflowContext(), controller_agent)
        r = await agent_session.run(task_instruction)
        print(r)

if __name__ == "__main__":
    asyncio.run(main())