import csv


async def is_registered(user_id: int) -> bool:
    filename = "db/users.csv"
    with open(filename, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        for user in reader:
            if int(user['user_id']) == user_id:
                return True

    return False


async def get_user_by_id(user_id: int) -> str:
    filename = "db/users.csv"
    with open(filename, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')

        for user in reader:
            if int(user['user_id']) == user_id:
                return user['first_name'] + ' ' + user['last_name']

    return None


async def insert_user(values: dict) -> None:
    filename = "db/users.csv"
    with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['user_id', 'first_name', 'last_name']

        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writerow(values)

    print(f"{values['user_id']} is registered")


async def insert_order(values: dict) -> None:
    filename = "db/orders.csv"
    with open(filename, 'a', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['user_id', 'file_id', 'plastic_type', 'plastic_color', 'layer_high', 'nozzle_width']

        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writerow(values)

    print(f"Order was accepted successfully")


async def get_first_order() -> dict:
    filename = "db/orders.csv"
    with open(filename, 'r', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['user_id', 'file_id', 'plastic_type', 'plastic_color', 'layer_high', 'nozzle_width']
    
        reader = csv.DictReader(csvfile, delimiter=';')
        return list(reader)[0]


async def delete_order_first() -> None:
    filename = "db/orders.csv"
    data = []
    with open(filename, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = list(reader)

    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['user_id', 'file_id', 'plastic_type', 'plastic_color', 'layer_high', 'nozzle_width']

        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()

        for i in range(1, len(data)):
            writer.writerow(data[i])

    print(f"Order first was deleted successfully")


async def delete_order_by_file_id(file_id: str) -> None:
    filename = "db/orders.csv"
    data = []
    with open(filename, 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = list(reader)

    with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['user_id', 'file_id', 'plastic_type', 'plastic_color', 'layer_high', 'nozzle_width']

        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()

        for i in range(len(data)):
            if data[i]['file_id'] != file_id:
                writer.writerow(data[i])

    print(f"Order with file id: {file_id} was deleted successfully")
