from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, get_db
from datetime import datetime, timezone

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 2. Define who is allowed to talk to this API
origins = [
    "http://localhost:5173", # Your React app
]

# 3. Add the CORS middleware to your engine
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Only allow requests from the VIP list
    allow_credentials=True,
    allow_methods=["*"],         # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],         # Allow all headers
)

# Define the exact shape of the data
class PromptCreate(BaseModel):
    title: str
    category: str
    content: str

class PromptPinUpdate(BaseModel):
    is_pinned: bool

class PromptRenameUpdate(BaseModel):
    title: str

@app.get("/")
def root():
    return {"message": "The PromptVault Engine is Online"}

@app.get("/api/prompts")
def get_prompts(db: Session = Depends(get_db)):
    response = db.query(models.Prompt).all()
    return response

# Create a POST route to receive new prompts
@app.post("/api/prompts")
def create_prompt(new_prompt: PromptCreate, db: Session = Depends(get_db)):
    if new_prompt.title.strip() == "" or new_prompt.content.strip() == "":
        raise HTTPException(400, "Title and Content cannot be empty!")
    print(f"Received a new prompt: {new_prompt.title}")
    new_db_prompt = models.Prompt(title=new_prompt.title, category=new_prompt.category, content=new_prompt.content)
    db.add(new_db_prompt)
    db.commit()
    db.refresh(new_db_prompt)
    
    return new_db_prompt

# GET one prompt
@app.get("/prompt/{prompt_id}")
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    db_prompt = (
        db.query(models.Prompt)
        .filter(models.Prompt.id == prompt_id)
        .first()
    )

    if not db_prompt:
        raise HTTPException(404, "Prompt ID Not Found!")

    return db_prompt


# PATCH pin status
@app.patch("/prompt/{prompt_id}/pin")
def update_prompt_pin(
    prompt_id: int,
    update: PromptPinUpdate,
    db: Session = Depends(get_db)
):
    db_prompt = (
        db.query(models.Prompt)
        .filter(models.Prompt.id == prompt_id)
        .first()
    )

    if not db_prompt:
        raise HTTPException(404, "Prompt ID Not Found!")

    db_prompt.is_pinned = update.is_pinned

    db.commit()
    db.refresh(db_prompt)

    return db_prompt


# Record prompt opening
@app.post("/prompt/{prompt_id}/open")
def open_prompt(
    prompt_id: int,
    db: Session = Depends(get_db)
):
    db_prompt = (
        db.query(models.Prompt)
        .filter(models.Prompt.id == prompt_id)
        .first()
    )

    if not db_prompt:
        raise HTTPException(404, "Prompt ID Not Found!")

    db_prompt.last_opened_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(db_prompt)

    return db_prompt


# DELETE prompt
@app.delete("/prompt/{prompt_id}")
def delete_prompt(
    prompt_id: int,
    db: Session = Depends(get_db)
):
    db_prompt = (
        db.query(models.Prompt)
        .filter(models.Prompt.id == prompt_id)
        .first()
    )

    if not db_prompt:
        raise HTTPException(404, "Prompt ID Not Found!")

    db.delete(db_prompt)
    db.commit()

    return {"status": "success"}

@app.patch("/prompt/{prompt_id}/rename")
def rename_prompt(
    prompt_id: int,
    update: PromptRenameUpdate,
    db: Session = Depends(get_db)
):
    db_prompt = (
        db.query(models.Prompt)
        .filter(models.Prompt.id == prompt_id)
        .first()
    )

    if not db_prompt:
        raise HTTPException(
            404,
            "Prompt ID Not Found!"
        )

    new_title = update.title.strip()

    if not new_title:
        raise HTTPException(
            400,
            "Prompt title cannot be empty!"
        )

    db_prompt.title = new_title

    db.commit()
    db.refresh(db_prompt)

    return db_prompt