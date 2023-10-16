import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from driver.selenium_driver import init_selenium_browser

meta_english_mapper = {
    "자료유형 :": "type",
    "서명 / 저자 :": "title",
    "발행사항 :": "issues",
    "ISBN :": "isbn",
}


def get_book_meta(soup, book_data):
    book_detail = soup.find_all("div", class_="detailMargin")[0]

    # 썸네일
    thumbnail_td = book_detail.find("td", id="detailMetaThumbnail")
    thumbnail_img = thumbnail_td.find("img")
    if thumbnail_img:
        thumbnail_url = thumbnail_img["src"]
        book_data["img"] = thumbnail_url

    # 데이터
    data_td = book_detail.find("td", id="detailMetaData")
    data_section = data_td.find("tbody", id="metaDataBody")
    datas = data_section.find_all("tr")
    for data in datas:
        data_head = data.find("td", class_="detailHead").text.strip()
        data_body = data.find("td", class_="detailBody").text.strip()

        if data_head in meta_english_mapper:
            data_head_english = meta_english_mapper[data_head.strip()]
            book_data[data_head_english] = data_body

        if data_head == "서명 / 저자 :":
            title_author = data_body.split("/")
            book_data["title"] = title_author[0].strip()
            if len(title_author) > 1:
                book_data["author"] = title_author[1].strip()

        if data_head == "키워드 :":  # 키워드 테이블에 저장
            keywords = data_body.split(",")
            for keyword in keywords:
                book_data["keyword"].append(keyword.strip())

    return book_data


def get_collection_paperback(soup, book_id):
    search_detail = soup.find("div", id="searchDetailInner")
    divs = search_detail.find_all("div", recursive=False)

    book_collection = []

    library_list = re.findall(r"itmdtl_info[0-9][0-9]", str(divs))
    for library_id in library_list:
        collection = soup.find("div", id=library_id)
        library = collection.find("div", class_="itemBranch").text
        locations = collection.find("tbody").find_all("tr")
        for location in locations:
            location_data = location.find_all("td")
            location_data = [tag.text.strip() for tag in location_data]
            if len(location_data) < 8:  # 기증자 행 제거
                continue

            collection_data = {
                "book_id": book_id,
                "library": library,
                "register_number": location_data[1],
                "call_number": location_data[3],
            }

            book_collection.append(collection_data)

    return book_collection


def get_suggest_list(soup, book_id):
    book_suggestion_list = []
    suggest_box = soup.find("div", id="content_suggest_box")
    if suggest_box:
        suggest_table = suggest_box.find("tbody")
        if suggest_table:
            suggestion_list = suggest_table.find_all("tr")
            for suggestion in suggestion_list:
                href = suggestion.find("a")["href"]
                cid = href.split("cid=")[1]
                book_suggestion_list.append(
                    {"book_id": book_id, "suggest_book_id": cid}
                )
    return book_suggestion_list


def extract_book(book_id):
    base_url = "https://cbnul.chungbuk.ac.kr/search/DetailView.ax"
    final_url = f"{base_url}?cid={book_id}"

    browser = init_selenium_browser()
    browser.get(final_url)
    # browser.implicitly_wait(10)
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#itmdtl_info01"))
        )
    except:
        pass

    try:
        WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#itmdtl_info02"))
        )
    except:
        pass

    try:
        WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#itmdtl_info03"))
        )
    except:
        pass

    try:
        WebDriverWait(browser, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#itmdtl_info04"))
        )
    except:
        pass

    WebDriverWait(browser, 4).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#content_suggest_box"))
    )

    soup = BeautifulSoup(browser.page_source, "html.parser")

    book_meta = {
        "book_id": book_id,
        "img": "",
        "type": "",
        "title": "",
        "author": "",
        "issues": "",
        "isbn": "",
        "keyword": [],
    }
    book_meta = get_book_meta(soup, book_meta)

    book_keywords = book_meta["keyword"]
    book_keywords = [
        {"book_id": book_id, "keyword": keyword} for keyword in book_keywords
    ]
    del book_meta["keyword"]

    book_collection = []
    if "단행본" in book_meta["type"]:  # 단행본
        book_collection = get_collection_paperback(soup, book_id)

    book_suggestion = get_suggest_list(soup, book_id)

    return {
        "data": book_meta,
        "keywords": book_keywords,
        "collection": book_collection,
        "suggestion": book_suggestion,
    }
