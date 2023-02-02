import csv


filename = "orders_test.csv"
data = []
with open(filename, 'r', newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    data = list(reader)
    print(data)


with open(filename, 'w', newline='', encoding="utf-8") as csvfile:
    fieldnames = ['user_id', 'file_id', 'plastic_type', 'plastic_color', 'layer_high', 'nozzle_width']

    writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
    writer.writeheader()

    for i in range(1, len(data)):
        writer.writerow(data[i])

    print(f"Order was accepted successfully")
