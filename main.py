from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from uuid import UUID, uuid4


app = FastAPI()

class Book(BaseModel):
    id: UUID 
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)
    rating: float = Field(gt=0, lt=5)
    
BOOKS = []

@app.get('/')
async def get_books():
    return BOOKS

@app.post('/')
async def create_book(book: Book):
    book.id = uuid4()
    BOOKS.append(book)
    return book

@app.put('/{book_id}')
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for b in BOOKS:
        if b.id == book_id:
            BOOKS[counter] = book
            return BOOKS[counter]
        counter += 1
    raise HTTPException(status_code=status.HTTP_404, detail="Book not found")

@app.delete('/{book_id}')
async def delete_book(book_id: UUID):
    counter = 0
    for b in BOOKS:
        if b.id == book_id:
            del BOOKS[counter]
            return {"message": "Book deleted successfully"}
        counter += 1
    raise HTTPException(status_code=status.HTTP_404, detail="Book not found")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)