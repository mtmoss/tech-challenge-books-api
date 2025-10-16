from typing import List, Optional
from models.book import BookCreate, BookUpdate, BookOut

# Simulação de banco em memória
_BOOKS: List[BookOut] = []
_NEXT_ID: int = 1

def _next_id() -> int:
    global _NEXT_ID
    nid = _NEXT_ID
    _NEXT_ID += 1
    return nid

def seed_basic() -> None:
    """Popular alguns livros para desenvolvimento local."""
    global _BOOKS, _NEXT_ID
    if _BOOKS:  # evita duplicar seeds
        return
    samples = [
        BookOut(id=_next_id(), title="Dom Casmurro", author="Machado de Assis", year=1899, isbn="978-6556403124"),
        BookOut(id=_next_id(), title="A Hora da Estrela", author="Clarice Lispector", year=1977, isbn="978-8520928335"),
    ]
    _BOOKS.extend(samples)

def list_books() -> List[BookOut]:
    return list(_BOOKS)

def get_book(book_id: int) -> Optional[BookOut]:
    return next((b for b in _BOOKS if b.id == book_id), None)

def create_book(data: BookCreate) -> BookOut:
    book = BookOut(id=_next_id(), **data.model_dump())
    _BOOKS.append(book)
    return book

def update_book(book_id: int, patch: BookUpdate) -> Optional[BookOut]:
    book = get_book(book_id)
    if not book:
        return None
    updates = patch.model_dump(exclude_unset=True)
    updated = book.model_copy(update=updates)
    # substituir o registro
    for i, b in enumerate(_BOOKS):
        if b.id == book_id:
            _BOOKS[i] = updated
            break
    return updated

def delete_book(book_id: int) -> bool:
    global _BOOKS
    before = len(_BOOKS)
    _BOOKS = [b for b in _BOOKS if b.id != book_id]
    return len(_BOOKS) < before
