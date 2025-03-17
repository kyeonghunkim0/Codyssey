import csv

csv_file = open('Mars_Base_Inventory_List.csv', 'r', encoding='utf-8')
try:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        print(row)
finally:
    csv_file.close()