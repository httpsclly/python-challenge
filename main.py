from fastapi import FastAPI, HTTPException, Depends, status 
from pydantic import BaseModel 
from typing import Annotated 
import models 
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List, Dict, Optional

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class TopicBase(BaseModel):
    title: str
    category: str

class TopicCreate(TopicBase):
    user_id: int
    pass

class Topic(TopicBase):
    id: int
    user_id: int  
    created_at: str  

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str
    topic_id: int
    user_id: int

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    created_at: str  

    class Config:
        orm_mode = True

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated [Session, Depends(get_db)]

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Endpoints para tópicos
@app.post("/topics/", response_model=Topic, status_code=status.HTTP_201_CREATED)
def create_topic(topic: TopicCreate, db: Session = Depends(get_db)):
    db_topic = models.Topic(**topic.dict(), user_id=topic.user_id)  # Use o ID do usuário apropriado
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

@app.get("/topics/", response_model=List[Topic])
def get_topics(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    topics = db.query(models.Topic).offset(skip).limit(limit).all()
    return topics

# Endpoints para mensagens
@app.post("/messages/", response_model=Message, status_code=status.HTTP_201_CREATED)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = models.Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@app.get("/messages/", response_model=List[Message])
def get_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    messages = db.query(models.Message).offset(skip).limit(limit).all()
    return messages