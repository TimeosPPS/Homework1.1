import json
from typing import List, Dict

def get_books(file_path: str = "books.json") -> List[Dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def save_books(db: List[Dict], file_path: str = "books.json") -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(db, file, indent=2, ensure_ascii=False)

def add_book(userId: int, title: str, body: str, file_path: str = "books.json") -> None:
    books = get_books(file_path)
    new_book = {
        "title": title,
        "body": body,
        "id": len(books),
        "userId": userId
    }
    books.append(new_book)
    save_books(books, file_path)

def get_book_id(book_id: int, file_path: str = "books.json") -> Dict:
    books = get_books(file_path)
    for book in books:
        if book["id"] == book_id:
            return book
    return {"error": "Book not found"}
