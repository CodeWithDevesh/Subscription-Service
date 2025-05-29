from pydantic import BaseModel, EmailStr


class UserSignup(BaseModel):
    email: EmailStr
    password: str


class UserLogin(UserSignup):
    pass


class TokenData(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenResponse(BaseModel):
    ok: bool = True
    message: str = "Token generated successfully"
    data: TokenData


class UserDetail(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool = False

    class Config:
        from_attributes = True


class User_Response(BaseModel):
    ok: bool = True
    message: str = "User retrieved successfully"
    data: UserDetail
