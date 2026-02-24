from google.adk.agents  import LlmAgent
from google.adk.tools import google_search

import instructions

healthcare_agent = LlmAgent(
    name="healthcare_agent",
    static_instruction=instructions.get_instructions("healthcare_agent_instructions"),
    
    tools=[google_search]
    
    
    
    
)