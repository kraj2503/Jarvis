from fastapi import FastAPI
from jarvis.agent import invoke_root_model
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    