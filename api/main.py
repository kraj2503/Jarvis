from fastapi import FastAPI

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

@app.post("/users")
def create_user(user: UserCreate):
    return user