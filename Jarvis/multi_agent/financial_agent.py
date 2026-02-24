from google.adk.agents  import Agent, SequentialAgent ,ParallelAgent, LlmAgent
from google.adk.tools import google_search, FunctionTool
from Jarvis.tools.financial_tool import get_financial_similarity
from Jarvis.multi_agent.instructions import get_instructions
from google.adk.models import Gemini





financial_google_search = LlmAgent(
    name="financial_google_search",
    model=Gemini(model="models/gemini-3-flash-preview"),
    
    static_instruction=get_instructions("financial_google_search"),
    
    tools=[google_search]   
)

financial_rag = LlmAgent(
    name="financial_rag",
    model=Gemini(model="models/gemini-3-flash-preview"),
    
    static_instruction=get_instructions("financial_rag"),
    
    tools=[FunctionTool(get_financial_similarity)]   
)

financial_aggregator = LlmAgent(
    name="financial_aggregator",
    model=Gemini(model="models/gemini-3-flash-preview"),
    
    static_instruction=get_instructions("financial_aggregator"),
    
)

financial_agent_parallel = ParallelAgent(
    name="parallel_data_for_financial",

    sub_agents=[financial_google_search,financial_rag]
)



financial_agent = SequentialAgent(
    name="financial_agent",
    
    sub_agents=[financial_agent_parallel, financial_aggregator],
)

