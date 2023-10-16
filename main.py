import time

from cbnu.detail_scrap import extract_book
from cbnu.search_scrap import extract_page
from file_io.json_file import json_write

# result = extract_book(3078324)
# print(result)

paperback_max_page = 24965

for page in range(paperback_max_page, paperback_max_page - 5, -1):
    book_ids = extract_page(page=page, book_type="paperback")

    for book_id in book_ids:
        book_info = extract_book(book_id)
        book_meta = book_info["data"]
        book_keywords = book_info["keywords"]
        book_collection = book_info["collection"]
        book_suggestion_list = book_info["suggestion"]

        json_write(file_name="book_meta.json", data=book_meta)

        for book_keyword in book_keywords:
            json_write(file_name="book_keyword.json", data=book_keyword)

        for collection in book_collection:
            json_write(file_name="book_collection.json", data=collection)

        for suggestion in book_suggestion_list:
            json_write(file_name="book_suggestion.json", data=suggestion)

        print(page)
        print(book_meta)
        print(book_keywords)
        print(book_collection)
        print(book_suggestion_list)
        print("////\n////")

        time.sleep(3)

    print("\n\n\n")
