from pydantic import BaseModel, EmailStr, Field, model_validator


class UserRegisterRequest(BaseModel):
    username: str = Field(min_length=8, max_length=20)
    password: str = Field(min_length=8, max_length=20)
    repeat_password: str = Field(min_length=8, max_length=20)
    email: EmailStr

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.repeat_password:
            raise ValueError("Passwords don't match")
        return self


class UserLoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class UserResponse(BaseModel):
    id: int
    username: str
    email: str