from google.adk.agents.llm_agent import Agent
from google.adk.models import Gemini


root_agent = Agent(
    model=Gemini(model="Gemini 1.5 Flash-8B"),
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    static_instruction=[],
    before_model_callback=[],
    after_model_callback=[],
    sub_agents=[],
    tools =[]    

)
