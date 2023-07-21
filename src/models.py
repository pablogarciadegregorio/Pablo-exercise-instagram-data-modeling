import os
import sys
import enum
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Enum
from sqlalchemy.orm import relationship, declarative_base, backref
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()


followers = Table("followers",          # HAY QUE IMPORTAR ARRIBA TABLE Y BACKREF
    Base.metadata,
    Column("user_from_id", Integer, ForeignKey('user.id'), primary_key=True), 
    Column("user_to_id", Integer, ForeignKey('user.id'), primary_key=True)
)

class MediaType(enum.Enum):
    VIDEO = 1
    IMAGE = 2
    CAROUSEL = 3
 
class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname =  Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    followers = relationship( "Follower", secondary= followers, lazy='subquery', backref=backref('users', lazy=True))
    post = relationship("Post", backref="user", lazy=True)
    comment = relationship("Comment", backref="user", lazy=True)

class Follower(Base):
    __tablename__ = 'follower'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = id = Column(Integer, primary_key=True)
    
# AQUI YA NO HACE FALTA PONER LAS user_from_id y user_to_id porque estan en la tabla pivote follower
  
    

class Comment(Base):
    __tablename__ = 'comment'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id =  Column(Integer, ForeignKey("user.id"),nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)

class Post(Base):
    __tablename__ = 'post'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"),nullable=False)
    media = relationship("Media", backref="post", lazy=True)
    comment = relationship("Comment", backref="post", lazy=True)
    


class Media(Base):
    __tablename__ = 'media'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    type = Column("type", Enum(MediaType))
    url =  Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
   




## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
