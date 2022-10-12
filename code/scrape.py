import os
import json
import csv

from scrape_pages import scrape_all_pages
from scrape_books import scrape_books


def scrape():
    """Scrape everything and return a list of books."""
    
    bookurl = scrape_all_pages()
    books = scrape_books(bookurl)
    return books


def write_books_to_csv(books, path):
    with open(CSV_PATH, "w+", encoding="utf-8") as file:
        dict_writer = csv.DictWriter(
            file,
            fieldnames=[
                "upc",
                "title",
                "category",
                "description",
                "price_gbp",
                "stock",
            ],
        )
        dict_writer.writeheader()
        dict_writer.writerows(books)




def write_books_to_jsonl(books, path):

    with open(JSONL_PATH, "w+", encoding="utf-8") as file:
        for book in books:
            file.write(json.dumps(book) + "\n")


if __name__ == "__main__":

    BASE_DIR = "artifacts"
    CSV_PATH = os.path.join(BASE_DIR, "results.csv")
    JSONL_PATH = os.path.join(BASE_DIR, "results.jsonl")

    os.makedirs(BASE_DIR, exist_ok=True)

    books = scrape()

    write_books_to_csv(books, CSV_PATH)
    write_books_to_jsonl(books, JSONL_PATH)
