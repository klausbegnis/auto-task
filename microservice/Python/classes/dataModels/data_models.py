from pydantic import BaseModel

class UserLogin(BaseModel):
    username: str
    password: str

class CreateUser(BaseModel):
    username: str
    password: str
    email: str
