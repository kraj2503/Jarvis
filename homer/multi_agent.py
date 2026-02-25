from google.adk.agents import LlmAgent

def home_automation(query:str):
    return "The task has been completed successfully";


# def home_automation_agent()

room_automation_agent = LlmAgent(
 model='gemini-2.5-flash',
    name='home_automation_agent',
    description="room automation Agent",
    instruction='You need to do the task and reply back when done',
    tools=[home_automation]

)