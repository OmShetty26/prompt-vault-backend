from pydantic import BaseModel, ConfigDict, Field

class PromptCreate(BaseModel):
    title: str
    category: str
    content: str

class PromptPinUpdate(BaseModel):
    is_pinned: bool

class PromptRenameUpdate(BaseModel):
    title: str

class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=30,
        pattern=r"^[A-Za-z0-9_]+$"
    )

    password: str = Field(
        min_length=12
    )

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str
    password: str

