from google.adk.agents  import Agent, SequentialAgent ,ParallelAgent, LlmAgent
from google.adk.tools import google_search, FunctionTool
from Jarvis.tools.similarity_tool import get_healthcare_similarity
from Jarvis.multi_agent.instructions import get_instructions
from google.adk.models import Gemini





healthcare_google_search = LlmAgent(
    name="healthcare_google_search",
    model=Gemini(model="models/gemini-3-flash-preview"),
    
    static_instruction=get_instructions("healthcare_google_search"),
    
    tools=[google_search]   
)

healthcare_rag = LlmAgent(
    name="healthcare_rag",
    model=Gemini(model="models/gemini-3-flash-preview"),
    
    static_instruction=get_instructions("healthcare_rag"),
    
    tools=[FunctionTool(get_healthcare_similarity)]   
)

healthcare_aggregator = LlmAgent(
    name="healthcare_aggregator",
    model=Gemini(model="models/gemini-3-flash-preview"),
    
    static_instruction=get_instructions("healthcare_aggregator"),
    
)

healthcare_agent_parallel = ParallelAgent(
    name="parallel_data_for_healthcare",

    sub_agents=[healthcare_google_search,healthcare_rag]
)



healthcare_agent = SequentialAgent(
    name="healthcare_agent",
    
    sub_agents=[healthcare_agent_parallel, healthcare_aggregator],
)



# print(get_similarity_healthcare("Cure of diabetis"))