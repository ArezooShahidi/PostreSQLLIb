from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship # create python object links
from .database import Base # the engine made in database module

class Author(Base):
    """the python code making ou class to database table for author"""
    __tablename__ = "authors"  # table name iin postgres
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship("Book", back_populates="author") # show the relationship of book table

class Book(Base):
    """the python code making ou class to database table for book"""
    __tablename__ = "books"  # table name iin postgres
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("authors.id")) # foreign key - connection to author table
    author = relationship("Author", back_populates="books") #