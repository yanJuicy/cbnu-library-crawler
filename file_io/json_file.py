import json


def json_write(file_name, data):
    file_path = f"./{file_name}"

    try:
        with open(file_name, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
    except:
        json_data = {"data": []}

    json_data["data"].append(data)

    with open(file_path, "w", encoding="utf-8") as outfile:
        json.dump(json_data, outfile, indent=1, ensure_ascii=False)
