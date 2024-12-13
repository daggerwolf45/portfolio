import json


def truncate(text: str, size: int) -> str:
    if len(text) < size:
        return text
    else:
        return text[:size-3] + '...'


def dump_json(data):
    return json.dumps(
        data,
        skipkeys=True,
        indent=None,
        separators=(',', ':'),
        default=None)


def seek_and_parse(data, depth: int):
    if depth == 0:
        return dump_json(data)
    else:
        depth -= 1
        if isinstance(data, dict):
            items = {}
            for key, value in data.items():
                items[key] = seek_and_parse(value, depth)

            return items
        else:  # Assuming list
            items = []
            for item in data:
                items.append(seek_and_parse(item, depth))

            return items

