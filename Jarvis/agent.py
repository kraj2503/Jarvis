from google.adk.agents.llm_agent import Agent
from google.adk.models import Gemini
from Jarvis.multi_agent.healthcare_agent import healthcare_agent
from Jarvis.multi_agent.financial_agent import financial_agent

root_agent = Agent(
    name='root_agent',
    model=Gemini(model="models/gemini-3-flash-preview"),

    description='A helpful assistant for user questions.',
    instruction='You are a multi Agent system, your task is to plan and deligate task to further agents and reply back with ansewer',
    # static_instruction=[],
    # before_model_callback=[],
    # after_model_callback=[],
    sub_agents=[healthcare_agent,financial_agent],
    # tools =[]    

)
