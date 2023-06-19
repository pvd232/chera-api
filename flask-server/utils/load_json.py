def load_json(filename) -> dict:
    import json

    with open(filename) as file:
        jsn = json.load(file)
        file.close()
        return jsn
