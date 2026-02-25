from google.adk.agents.llm_agent import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from homer.multi_agent import room_automation_agent
from dotenv import load_dotenv
load_dotenv()

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Home automation Agent',
    instruction='You are an home automation agent your task is to do the home automation as asked and reply back to user when task is completed',
    sub_agents=[room_automation_agent]
)


app = to_a2a(root_agent)
