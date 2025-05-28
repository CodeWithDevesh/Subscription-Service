from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    email: EmailStr
    password: str

class UserLogin(UserSignup):
    pass

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
