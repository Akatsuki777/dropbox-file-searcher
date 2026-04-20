import csv
import sys
import os

FILE_LOCATION = "resources/wc_products.csv"

if __name__ == "__main__":

    if len(sys.argv) > 1:
        FILE_LOCATION = sys.argv[1]

    with open(FILE_LOCATION, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        active_products = [row for row in csv_reader if row['Attribute 1 visible'] == '1']
    
    save_location = os.path.join(os.path.dirname(FILE_LOCATION), "active_products.csv")

    with open(save_location, mode='w', newline='') as csv_file:
        fieldnames = active_products[0].keys()
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(active_products)