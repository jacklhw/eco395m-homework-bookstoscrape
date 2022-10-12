from common import get_soup


def extract_price(price_str):
    """Extracts the price form the string in the product description as a float."""

    return float(
        "".join([char for char in price_str if char.isnumeric() or char == "."])
    )


def extract_stock(stock_str):
    """Extracts the count form the string in the product description as an int."""

    return int("".join([char for char in stock_str if char.isnumeric()]))


def get_category(soup):
    """Extracts the category from the BeautifulSoup instance representing a book page as a string."""

    breadcrumb_tag = soup.find_all("ul", class_="breadcrumb")[0]
    a_tags = breadcrumb_tag.find_all("a")

    return a_tags[-1].text


def get_title(soup):
    """Extracts the title from the BeautifulSoup instance representing a book page as a string."""

    product_main_tag = soup.find_all("div", class_="product_main")[0]

    return product_main_tag.h1.text


def get_description(soup):
    """Extracts the description from the BeautifulSoup instance representing a book page as a string."""
    product_main_tag = soup.find_all("article", class_="product_page")[0]
    ptags = product_main_tag.find_all("p", recursive=False)
    if not ptags:
        return None

    return ptags[0].text


def get_product_information(soup):
    """Extracts the product information from the BeautifulSoup instance representing a book page as a dict."""

    upc_idx = 0
    price_idx = 2
    stock_idx = 5

    tabletag = soup.find_all("table", class_="table")[0]
    trtags = tabletag.find_all("tr")
    return {
        "upc": trtags[upc_idx].td.text,
        "price_gbp": extract_price(trtags[price_idx].td.text),
        "stock": extract_stock(trtags[stock_idx].td.text),
        }


def scrape_book(book_url):
    """Extracts all information from a book page and returns a dict."""

    soup = get_soup(book_url)

    return {
        "title": get_title(soup),
        "category": get_category(soup),
        "description": get_description(soup),
        **get_product_information(soup),
    }


def scrape_books(book_urls):
    """Extracts all information from a list of book page and returns a list of dicts."""
    books = []
    for book_url in book_urls:
        try:
            book = scrape_book(book_url)
            books.append(book)
        except Exception as e:
            print("f*A error has occured scraping book {book_url}")
            print(e)
    return books


if __name__ == "__main__":

    # code for testing

    # set up fixtures for testing

    book_url = "http://books.toscrape.com/catalogue/the-secret-of-dreadwillow-carse_944/index.html"
    book_url_no_description = "http://books.toscrape.com/catalogue/the-bridge-to-consciousness-im-writing-the-bridge-between-science-and-our-old-and-new-beliefs_840/index.html"

    soup = get_soup(book_url)
    soup_no_description = get_soup(book_url_no_description)

    # test extract_price

    assert extract_price("£56.13") == 56.13

    # test extract_stock

    assert extract_stock("In stock (16 available)") == 16

    # test get_category

    assert get_category(soup) == "Childrens"

    # test get_title

    assert get_title(soup) == "The Secret of Dreadwillow Carse"

    # test get_description

    assert get_description(soup) is not None
    assert get_description(soup_no_description) is None

    # test get_product_information

    product_information = get_product_information(soup)

    assert set(product_information.keys()) == {"upc", "price_gbp", "stock"}

    assert product_information == {
        "upc": "b5ea0b5dabed25a8",
        "price_gbp": 56.13,
        "stock": 16,
    }

    # test scrape_book

    book = scrape_book(book_url)
    book_no_description = scrape_book(book_url_no_description)

    expected_keys = {"title", "category", "description", "upc", "price_gbp", "stock"}

    assert set(book.keys()) == expected_keys
    assert set(book_no_description.keys()) == expected_keys
