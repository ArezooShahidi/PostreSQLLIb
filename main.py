from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.models import Author, Book
from pydantic import BaseModel, ConfigDict
from typing import List

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library CRUD API", version="1.0")

# Pydantic schemas (for request/response)
class AuthorCreate(BaseModel):
    """creating the author by just getting the name from user"""
    name: str

class AuthorResponse(BaseModel):
    """The response that shows when user request responed for creating author"""
    id: int
    name: str
    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)

class BookCreate(BaseModel):
    """creating the author by getting the book title and book author id
        the author id is the foreign key to the author class
    """
    title: str
    author_id: int

class BookResponse(BaseModel):
    """The respose thaat shows when user request respond for creating book"""
    id: int
    title: str
    author_id: int  # foreign key to author
    author_name: str
    # class Config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)

# ---------- AUTHOR CRUD ----------
@app.post("/authors/", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """Creating new author when it doesn't exists"""
    db_author = Author(name=author.name)
    db.add(db_author)  # stage the new author
    db.commit()  # save to DB
    db.refresh(db_author)  # the auto generate id back
    return db_author

@app.get("/authors/", response_model=List[AuthorResponse])
def read_authors(db: Session = Depends(get_db)):
    """Read authors (show the database)"""
    return db.query(Author).all()  # return databse

@app.get("/authors/{author_id}", response_model=AuthorResponse)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """Read the author by it's id"""
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(404, "Author not found")  # error of not existence of author for read
    return author

@app.put("/authors/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    """Update the author by specyfying the auther id"""
    db_author = db.get(Author, author_id)
    if not db_author:  # check for author existence
        raise HTTPException(404, "Author not found")  # error of not existence of author for update
    db_author.name = author.name
    db.commit()  # save to DB
    db.refresh(db_author) # auto generate the id back
    return db_author

@app.delete("/authors/{author_id}", response_model=dict)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Delete the author by the id (Delete the specific row of the author)"""
    author = db.get(Author, author_id) # ask author id
    if not author:
        raise HTTPException(404, "Author not found")   # error of not existence of author for delete
    db.delete(author)  # delete the author
    db.commit()  # save to DB
    return {"message": "Author deleted"}

# ---------- BOOK CRUD ----------
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Creating the Book with foreign key of author"""
    author = db.get(Author, book.author_id)
    if not author:
        raise HTTPException(404, "Author not found")

    db_book = Book(title=book.title, author_id=book.author_id)
    db.add(db_book)
    try:
        db.commit()
        db.refresh(db_book)
    except IntegrityError:
        raise HTTPException(400, "Invalid author_id")

    db_book = Book(title=book.title, author_id=book.author_id)
    db.add(db_book) # stage the new book
    db.commit()  # save to DB
    db.refresh(db_book)   # auto geenerate the id back
    return {
        "id": db_book.id,
        "title": db_book.title,
        "author_id": db_book.author_id,
        "author_name": db_book.author.name
    }

@app.get("/books/", response_model=List[BookResponse])
def read_books(db: Session = Depends(get_db)):
    """Read the book (show whole databse)"""
    books = db.query(Book).all() # get the whole book query
    return [{"id": b.id, "title": b.title, "author_id": b.author_id, "author_name": b.author.name} for b in books]

@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    """Show the specific book by the book id"""
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Book not found") # error of not existence of book for read
    return {"id": book.id, "title": book.title, "author_id": book.author_id, "author_name": book.author.name}

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    """Update the book by its id"""
    db_book = db.get(Book, book_id)
    if not db_book:
        raise HTTPException(404, "Book not found") # error of not existence of book for update
    db_book.title = book.title
    db_book.author_id = book.author_id
    db.commit() # save to DB
    db.refresh(db_book) # auto generate book id
    return {"id": db_book.id, "title": db_book.title, "author_id": db_book.author_id, "author_name": db_book.author.name}

@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete the book by the id (Delete the specific row of the book)"""
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Book not found") # error of not existence of book for delete
    db.delete(book)
    db.commit() # save to DB
    return {"message": "Book deleted"}