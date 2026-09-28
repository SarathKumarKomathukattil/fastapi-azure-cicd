from fastapi import FastAPI,status
from fastapi.exceptions import HTTPException
from typing import Optional
from pydantic import BaseModel


books = [
    {
        "id": 1,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "publish_date": "1988-01-01"
    },
    {
        "id": 2,
        "title": "The God of Small Things",
        "author": "Arundhati Roy",
        "publish_date": "1997-04-04"
    },
    {
        "id": 3,
        "title": "The White Tiger",
        "author": "Aravind Adiga",
        "publish_date": "2008-01-01"
    },
    {
        "id": 4,
        "title": "The Palace of Illusions",
        "author": "Chitra Banerjee Divakaruni",
        "publish_date": "2008-02-12"
    }
]

app = FastAPI()

class Book(BaseModel):
    id:int
    title:str
    author:str
    publish_date:str

#GET
@app.get("/book")
def get_book():
    return books

@app.get("/book/{book_id}")
def find_book(book_id:int):
    for book in books:
        if book["id"] == book_id:
            return book
      
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Book not found!')

#POST
@app.post("/book")
def create_book(book:Book):
    new_book =book.model_dump() #model_dump() coverts pydantic object to normal python dictionary
    books.append(new_book)
    return new_book

#PUT

class BookUpdate(BaseModel):
    title:str
    author:str
    publish_date:str

@app.put("/book/{book_id}")
def update_record(book_update:BookUpdate,book_id:int):
    for book in books:
        if book['id']==book_id:
            book['title'] = book_update.title
            book['author'] = book_update.author
            book['publish_date'] = book_update.publish_date
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Content not found!')


#DELETE
@app.delete("/book/{book_id}")
def delete_data(book_id:int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {"message":"Book deleted"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Content not found!')