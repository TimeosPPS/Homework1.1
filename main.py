from typing import List

from fastapi import FastAPI, HTTPException, status
import uvicorn

from models import BooksModelResponse, BooksModel
import data

app = FastAPI()

@app.get("/books", status_code=status.HTTP_202_ACCEPTED, response_model=List[BooksModelResponse])
async def get_books():
    return data.get_books()

@app.post("/add_book/", status_code=status.HTTP_202_ACCEPTED, response_model=List[BooksModelResponse])
async def add_book(book: BooksModel):
    data.add_book(book.userId, book.title, book.body)
    return data.get_books()

@app.get("/books/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=BooksModelResponse)
async def get_book_by_id(id: int):
    book = data.get_book_id(id)
    if "error" in book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)