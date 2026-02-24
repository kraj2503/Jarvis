from google.adk.agents  import Agent
from google.adk.tools import google_search
from Jarvis.tools.healthcare_tool import get_healthcare_similarity
from Jarvis.multi_agent.instructions import get_instructions
from google.adk.models import Gemini



healthcare_agent_google = Agent(
    name="healthcare_agent",
    model=Gemini(model="models/gemini-3-flash-preview"),


    static_instruction=get_instructions("healthcare_agent"),
    
    tools=[google_search]   
)

healthcare_agent = Agent(
    name="healthcare_agent",
    model=Gemini(model="models/gemini-3-flash-preview"),


    static_instruction=get_instructions("healthcare_agent"),
    sub_agents=[healthcare_agent_google],
    tools=[get_healthcare_similarity]   
)



# print(get_similarity_healthcare("Cure of diabetis"))