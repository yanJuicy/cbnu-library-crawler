from requests import get
from bs4 import BeautifulSoup

contents_type = {"": "", "paperback": "(CLASSID:(101%20OR%20102%20OR%20103))"}  # 단행본


def extract_page(page, book_type):
    base_url = "https://cbnul.chungbuk.ac.kr/search/Search.Result.ax"
    response = get(f"{base_url}?f={contents_type[book_type]}&page={page}")

    if response.status_code != 200:
        print("Can't request website")
        return
    else:
        result = []
        soup = BeautifulSoup(response.text, "html.parser")
        books = soup.find("ul", class_="listType01").find_all("li")
        for book in books:
            anchor = book.find("a")
            link = anchor["href"]
            book_id = link.split("cid=")[1]
            result.append(book_id)
        return result
