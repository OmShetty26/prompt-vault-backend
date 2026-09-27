from pydantic import BaseModel, ConfigDict

class PromptCreate(BaseModel):
    title: str
    category: str
    content: str

class PromptPinUpdate(BaseModel):
    is_pinned: bool

class PromptRenameUpdate(BaseModel):
    title: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

