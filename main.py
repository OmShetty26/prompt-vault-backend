from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, get_db

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
    
    return {'status': "Success", 'data': new_db_prompt}

# GET route to return data for a specific prompt id
@app.get("/prompt/{prompt_id}")
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    response = db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()
    return response

# PUT route to modify exisiting data for a specific prompt id
@app.put("/prompt/{prompt_id}")
def modify_prompt(prompt_id: int, updated_prompt: PromptCreate, db: Session = Depends(get_db)):
    db_prompt = db.query(models.Prompt).filter(models.Prompt.id == prompt_id).first()
    if db_prompt:
        db_prompt.title = updated_prompt.title
        db_prompt.category = updated_prompt.category
        db_prompt.content = updated_prompt.content
        db.commit()
        db.refresh(db_prompt)
        return db_prompt
    else:
        raise HTTPException(404, "Prompt ID Not Found!")
    

