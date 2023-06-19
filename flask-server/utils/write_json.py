from io import TextIOWrapper


def write_json(outfile: TextIOWrapper, dicts: list[dict]) -> None:
    import json

    data = json.load(outfile)
    if data:
        outfile.seek(0)
        json.dump(dicts, outfile, indent=4)
        outfile.truncate()
    else:
        outfile.write(json.dumps(dicts, indent=4))
