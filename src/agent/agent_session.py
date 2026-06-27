from dataclasses import dataclass
from typing import List, Dict, Any
import json
from agents import Agent, Runner, SQLiteSession


@dataclass
class WorkflowContext:
    def __init__(self, state: Dict[str, Any] = None):
        self.state = state if state else {}


class AgentSession:
    def __init__(self, session_name:str, agent_context:WorkflowContext, starting_agent:Agent[WorkflowContext]):
        self.session = SQLiteSession(session_name)
        self.agent_context = agent_context
        self.starting_agent = starting_agent

    async def run(self, message:str) -> List[str]:
        msg = json.dumps({"role": "user", "content": message})
        run_result = await Runner.run(
            session=self.session, context=self.agent_context, starting_agent=self.starting_agent, input=msg)

        return run_result.final_output