from typing import Dict

itemNameToId: Dict[str, int] = {}
itemIdToName: Dict[int, str] = {}


def item_id(name: str) -> int:
    try:
        # If the value passed in looks like an int, use it as an int...
        item_id = int(name)
        return item_id
    except ValueError:
        pass
    if name not in itemNameToId:
        itemId = len(itemNameToId) + 1
        itemNameToId[name] = itemId
        itemIdToName[itemId] = name
        return itemId
    else:
        return itemNameToId[name]


def item_str(id) -> str:
    name = itemIdToName.get(id)
    if name:
        return name
    return str(name)
