from __future__ import annotations
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional

CSV_PATH = Path(".local_data") / "books.csv"

def _coerce_int(value: Optional[str]) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None

def _coerce_rating(value: Optional[str]) -> Optional[int]:
    return _coerce_int(value)

def load_books() -> List[Dict[str, Any]]:
    """
    Lê o CSV e retorna uma lista de dicionários com tipos coerentes.
    Campos: id(int), title(str), price(str), rating(int|None),
            availability(str|None), category(str|None),
            image_url(str|None), product_url(str|None)
    """
    books: List[Dict[str, Any]] = []

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo CSV não encontrado em {CSV_PATH.resolve()}. "
            "Execute o scraper primeiro."
        )

    with CSV_PATH.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append({
                "id": _coerce_int(row.get("id")),
                "title": row.get("title") or "",
                "price": row.get("price") or "",
                "rating": _coerce_rating(row.get("rating")),
                "availability": row.get("availability") or None,
                "category": row.get("category") or None,
                "image_url": row.get("image_url") or None,
                "product_url": row.get("product_url") or None,
            })
    return books

def get_book_by_id(book_id: int) -> Optional[Dict[str, Any]]:
    """Busca um único livro pelo id (inteiro)."""
    for b in load_books():
        if b["id"] == book_id:
            return b
    return None