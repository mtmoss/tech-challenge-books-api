from __future__ import annotations
import sys
import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = OUTPUT_DIR / "books.csv"

def fetch(url: str) -> BeautifulSoup:
    """Baixa uma URL e retorna o BeautifulSoup do HTML."""
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "lxml")

def main() -> int:
    print("[scrape] Baixando página inicial…", BASE_URL)
    soup = fetch(BASE_URL)

    # Checagem simples: existe o container de livros?
    grid = soup.select("section div ol.row li")
    print(f"[scrape] Itens detectados na home: {len(grid)} (esperado: > 0)")

    # Apenas cria o CSV com cabeçalho (vamos popular no 5.2)
    if not CSV_PATH.exists():
        with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["id","title","price","rating","availability","category","image_url","product_url"])
        print(f"[scrape] CSV criado: {CSV_PATH.resolve()}")

    return 0

if __name__ == "__main__":
    sys.exit(main())