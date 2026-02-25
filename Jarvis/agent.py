from google.adk.agents.llm_agent import LlmAgent
from google.adk.models import Gemini
from Jarvis.multi_agent.healthcare_agent import healthcare_agent
from Jarvis.multi_agent.financial_agent import financial_agent
from google.adk.sessions import database_session_service
from google.adk.sessions import InMemorySessionService
from Jarvis.tools.memory_tool import read_memory, write_memory
from Jarvis.instructions import get_instructions
from google.genai import types
# from google.adk.agents.remote_a2a_agent import PREV_AGENT_CARD_WELL_KNOWN_PATH,
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.runners import Runner
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
# from google.adk.runners import Runner
import httpx


APP_NAME = "Jarvis"
# USER_ID = "mem_user"
MODEL = "gemini-3-flash-preview" 



# InMemorySessionService stores conversations in RAM (temporary)
session_service = InMemorySessionService()  #Will migrate to redis later    

REMOTE_URL="http://localhost:8001"
AGENT_CARD=f"{REMOTE_URL}{AGENT_CARD_WELL_KNOWN_PATH}"


print(f"\n\n\n AGENT CARD URL--  {AGENT_CARD} \n\n\n\n")


home_automation_remote_agent = RemoteA2aAgent(
    name="Home_automation_agent",
    description="Agent handles all the home automation tasks...",
    httpx_client=httpx.AsyncClient(base_url=REMOTE_URL),
    agent_card=AGENT_CARD
)



root_agent = LlmAgent(
    name='root_agent',
    model=Gemini(model="models/gemini-3-pro-preview"),

    description='A helpful assistant for user questions.',
    instruction=get_instructions("root_agent"),
    # static_instruction=[],
    # before_model_callback=[write_memory],
    # after_model_callback=[read_memory],
    sub_agents=[healthcare_agent,financial_agent,home_automation_remote_agent],
    #session_service=session_service,
    # generate_content_config=types.GenerateContentConfig(
    #     safety_settings=[
    #         types.SafetySetting(  # avoid false alarm about rolling dice.
    #             category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    #             threshold=types.HarmBlockThreshold.OFF,
    #         ),
    #     ]  
    # )
)

runner = Runner(app_name="Jarvis", agent=root_agent,session_service=session_service)
