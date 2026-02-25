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
from google.genai.types import Content, Part
import httpx
import asyncio

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


async def main(user_id:str,session_id:str,query:str):
    
    session = await session_service.get_session(
        app_name=APP_NAME, user_id=user_id, session_id=session_id
    )
    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=user_id, session_id=session_id
        )

    user_content = Content(
        role="user", parts=[Part(text=query)]
    )

    
    final_response = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_content
        
        ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response= event.content.parts[0].text
    
    return final_response;


if __name__ =="__main__":
    asyncio.run(main("userId","session_id","tell me about a2a in adk"))
         
