import csv
import sys
import os

FILE_LOCATION = "resources/wc_products.csv"


def main(file_location=FILE_LOCATION):
    with open(file_location, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        active_products = [row for row in csv_reader if row['Attribute 1 visible'] == '1']

    save_location = os.path.join(os.path.dirname(file_location), "active_products.csv")

    with open(save_location, mode='w', newline='') as csv_file:
        fieldnames = active_products[0].keys()
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(active_products)


if __name__ == "__main__":

    file_location = FILE_LOCATION

    if len(sys.argv) > 1:
        file_location = sys.argv[1]

    main(file_location)
