from fastapi import FastAPI
from jarvis.agent import invoke_root_model

app=FastAPI()

@app.get("/")
def read_root():
    return {'Hello':'World'};


@app.get("/users/{id}")
def get_user(id: int):
    return {"id": id}


from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    age: int

class Query_call(BaseModel):
    user_id:str
    session_id:str
    query:str



@app.post("/users")
def create_user(user: UserCreate):
    return user

@app.post("/invoke")
async def call_model(query_call: Query_call):
    print(query_call)
    
    res = await invoke_root_model(
        
        user_id=query_call.user_id,
        session_id=query_call.session_id,
        query=query_call.query,
    )
    return res
    