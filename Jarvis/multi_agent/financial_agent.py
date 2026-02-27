from google.adk.agents  import Agent, SequentialAgent ,ParallelAgent, LlmAgent
from google.adk.tools import google_search, FunctionTool
from  jarvis.tools.similarity_tool import get_financial_similarity
from  jarvis.instructions import get_instructions
from google.adk.models import Gemini


model=Gemini(model="models/gemini-3-flash-preview")


financial_intent_router = LlmAgent(
    name="financial_intent_router",
    model=model,
    
    static_instruction=get_instructions("financial_intent_router"),
)

financial_google_search = LlmAgent(
    name="financial_google_search",
    model=model,
    
    static_instruction=get_instructions("financial_google_search"),
    
    tools=[google_search]   
)

financial_rag = LlmAgent(
    name="financial_rag",
    model=model,
    
    static_instruction=get_instructions("financial_rag"),
    
    tools=[FunctionTool(get_financial_similarity)]   
)

financial_aggregator = LlmAgent(
    name="financial_aggregator",
    model=model,
    
    static_instruction=get_instructions("financial_aggregator"),
    
)

financial_agent_parallel = ParallelAgent(
    name="parallel_data_for_financial",

    sub_agents=[financial_google_search,financial_rag]
)



financial_agent = SequentialAgent(
    name="financial_agent",
    
    sub_agents=[financial_intent_router,financial_agent_parallel, financial_aggregator],
)

