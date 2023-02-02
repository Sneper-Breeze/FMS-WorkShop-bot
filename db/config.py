import json


def get_values():
    filename = "db/order_config.json"
    with open(filename, "r", encoding="utf-8") as jsonfile:
        data = json.load(jsonfile)

    return data


async def delete_plastic_color(value: str):
    filename = "db/order_config.json"
    data = get_values()
    try:
        data["plastic_colors"].remove(value)
    except ValueError:
        pass
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile)

    print(f"plastic color: {value} is deleted")


async def delete_plastic_type(value: str):
    filename = "db/order_config.json"
    data = get_values()
    try:
        data["plastic_types"].remove(value)
    except ValueError:
        pass
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile)

    print(f"plastic type: {value} is deleted")


async def delete_layer_high(value: float):
    filename = "db/order_config.json"
    data = get_values()
    try:
        data["layer_highs"].remove(float(value))
    except ValueError:
        print('error')
        return
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile)

    print(f"layer high: {value} is deleted")


async def delete_nozzle_width(value: float):
    filename = "db/order_config.json"
    data = get_values()
    try:
        data["nozzle_widths"].remove(float(value))
    except ValueError:
        print('error')
        return
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile)

    print(f"nozzle width: {value} is deleted")


async def insert_plastic_color(value: str):
    filename = "db/order_config.json"
    data = get_values()
    data["plastic_colors"].append(value)
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile)

    print(f"plastic color: {value} is appended")


async def insert_plastic_type(value: str):
    filename = "db/order_config.json"
    data = get_values()
    data["plastic_types"].append(value)
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile)

    print(f"plastic type: {value} is appended")


async def insert_layer_high(value: float):
    filename = "db/order_config.json"
    data = get_values()
    data["layer_highs"].append(value)
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile)

    print(f"layer high: {value} is appended")


async def insert_nozzle_width(value: float):
    filename = "db/order_config.json"
    data = get_values()
    data["nozzle_widths"].append(value)
    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile)

    print(f"nozzle width: {value} is appended")