from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    facebook_token = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    groups = relationship("Group", back_populates="user")
    keywords = relationship("Keyword", back_populates="user")
    templates = relationship("Template", back_populates="user")
    leads = relationship("Lead", back_populates="user")

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    facebook_group_id = Column(String)
    name = Column(String)
    is_joined = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="groups")
    leads = relationship("Lead", back_populates="group")

class Keyword(Base):
    __tablename__ = "keywords"
    
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="keywords")

class Template(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    content = Column(Text)
    type = Column(String)  # request/complaint/job_offer
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="templates")

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    facebook_post_id = Column(String)
    content = Column(Text)
    author_id = Column(String)
    post_type = Column(String)
    responded = Column(Boolean, default=False)
    response_template_id = Column(Integer, ForeignKey("templates.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    
    user = relationship("User", back_populates="leads")
    group = relationship("Group", back_populates="leads")
