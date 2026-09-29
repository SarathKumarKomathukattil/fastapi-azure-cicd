from fastapi import FastAPI,Depends
from pydantic import BaseModel
from sqlalchemy.orm import session
from database import get_db
import model 


app = FastAPI()

class BookStore(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str


@app.post("/books")
def create_book(book:BookStore,db:session=Depends(get_db)):
    new_book = model.Book(      ##copying data from API object to database object
        id = book.id,
        title = book.title,
        author = book.author,
        publish_date = book.publish_date
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/books")
def get_book(db:session=Depends(get_db)):
    books = db.query(model.Book).all()
    return books




