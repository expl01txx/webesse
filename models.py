from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    login: str
    tokens: int
    admin: int
    esse_checks: int

class UserInDB(User):
    passwd: str
