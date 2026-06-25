from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String)
    content = Column(String)
    # We add a timestamp so you can sort prompts by newest later!
    created_at = Column(DateTime, default=datetime.datetime.utcnow)