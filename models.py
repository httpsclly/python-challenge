from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)

    topics = relationship("Topic", back_populates="owner")
    messages = relationship("Message", back_populates="owner")


class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    # Relacionamento com User e Message
    owner = relationship("User", back_populates="topics")
    messages = relationship("Message", back_populates="topic")


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

    # Relacionamento com User e Topic
    owner = relationship("User", back_populates="messages")
    topic = relationship("Topic", back_populates="messages")