from __future__ import annotations
import sys
import csv
from pathlib import Path
from typing import Iterable, Tuple, Dict, Any, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
OUTPUT_DIR = Path(".local_data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = OUTPUT_DIR / "books.csv"

def fetch(url: str) -> BeautifulSoup:
    """Baixa uma URL e retorna um BeautifulSoup do HTML (parser lxml)."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")

def abs_url(base: str, link: str) -> str:
    """Constrói URL absoluta a partir de base + link relativo."""
    return urljoin(base, link)

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5
}

def parse_rating(article_tag: BeautifulSoup) -> Optional[int]:
    """Lê a classe CSS 'star-rating X' e converte para número (1-5)."""
    rating_tag = article_tag.select_one("p.star-rating")
    if not rating_tag:
        return None
    # classes do tipo ['star-rating', 'Three']
    classes = rating_tag.get("class", [])
    for cls in classes:
        if cls in RATING_MAP:
            return RATING_MAP[cls]
    return None

def parse_price(article_tag: BeautifulSoup) -> Optional[str]:
    price_tag = article_tag.select_one("p.price_color")
    return price_tag.text.strip() if price_tag else None

def parse_availability(article_tag: BeautifulSoup) -> Optional[str]:
    avail_tag = article_tag.select_one("p.instock.availability")
    if not avail_tag:
        return None
    # .text inclui quebras/espacos – normaliza:
    text = " ".join(avail_tag.text.split())
    return text

def parse_title_and_links(article_tag: BeautifulSoup) -> Tuple[str, str, str]:
    """
    Retorna (title, product_url_abs, image_url_abs)
    """
    # product link e title
    a = article_tag.select_one("h3 a")
    title = a.get("title", "").strip()
    product_rel = a.get("href", "")
    product_url = abs_url(BASE_URL, product_rel)

    # imagem
    img = article_tag.select_one("div.image_container img")
    img_rel = img.get("src", "") if img else ""
    # no site as imagens começam com "../../"
    image_url = abs_url(BASE_URL, img_rel)

    return title, product_url, image_url

def iter_books_in_listing(listing_url: str, category_name: str) -> Iterable[Dict[str, Any]]:
    """
    Percorre uma página de listagem (e segue paginação "next"),
    produzindo dicionários com campos do livro.
    """
    url = listing_url
    while True:
        soup = fetch(url)
        articles = soup.select("section div ol.row li article.product_pod")
        for art in articles:
            title, product_url, image_url = parse_title_and_links(art)
            price = parse_price(art)
            rating = parse_rating(art)
            availability = parse_availability(art)

            yield {
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "category": category_name,
                "image_url": image_url,
                "product_url": product_url,
            }

        # paginação: link "li.next a"
        next_a = soup.select_one("li.next a")
        if not next_a:
            break
        next_href = next_a.get("href", "")
        url = abs_url(url, next_href)  # atenção: base é a página atual

def get_categories() -> Iterable[Tuple[str, str]]:
    """
    Retorna (category_name, category_url_abs) para cada categoria.
    """
    soup = fetch(BASE_URL)
    # menu lateral
    links = soup.select("div.side_categories ul li ul li a")
    for a in links:
        name = " ".join(a.text.split())
        href = a.get("href", "")
        url = abs_url(BASE_URL, href)
        yield name, url

CSV_HEADERS = [
    "id", "title", "price", "rating",
    "availability", "category", "image_url", "product_url"
]

def write_csv(rows: Iterable[Dict[str, Any]], csv_path: Path) -> int:
    """
    Escreve linhas no CSV, adicionando um id incremental.
    Retorna a contagem de linhas escritas.
    """
    count = 0
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for i, row in enumerate(rows, start=1):
            out = {"id": i, **row}
            writer.writerow(out)
            count += 1
    return count

def scrape_all() -> int:
    """
    Percorre todas as categorias e páginas, gerando dicionários de livros.
    Escreve o CSV completo e retorna o total de livros.
    """
    def generator():
        for cat_name, cat_url in get_categories():
            for book in iter_books_in_listing(cat_url, cat_name):
                yield book

    total = write_csv(generator(), CSV_PATH)
    return total

def main() -> int:
    print("[scrape] Iniciando scraping completo…")
    total = scrape_all()
    print(f"[scrape] Concluído. Livros coletados: {total}")
    print(f"[scrape] CSV salvo em: {CSV_PATH.resolve()}")
    return 0

if __name__ == "__main__":
    sys.exit(main())