from helpers.getActiveProducts import main as get_active_products
from rules.criterion_loader import CriterionLoader
from models.file_record import FileRecord
from clients.dropbox_client import DropboxClient
from helpers.logger import setup_logger
from dotenv import load_dotenv
import csv
import re
import os

if __name__ == "__main__":

    load_dotenv()

    print(os.getenv("DROPBOX_KEY"))
    if not os.path.exists("resources/active_products.csv"):
        get_active_products()

    logger = setup_logger()
    criterion_loader = CriterionLoader("config/criteria.json", logger=logger)
    dropbox_client = DropboxClient(token=os.getenv("DROPBOX_KEY"), logger=logger)

    with open("resources/active_products.csv", mode='r') as csv_file:
        product_names = csv.DictReader(csv_file)
        for product in product_names:
            re_pattern = re.compile(r'\b' + re.escape(product['Name']) + r'\b', re.IGNORECASE)
            matches = dropbox_client.search_files(product['Name'])

            for match in matches:
                metadata = dropbox_client.get_file_metadata(match.metadata.id)
                if metadata is None:
                    continue

                if not re_pattern.search(metadata.name):
                    continue

                if dropbox_client.is_folder(metadata):
                    continue
                
                file_record = FileRecord(
                    name=metadata.name,
                    path=metadata.path_display,
                    size=metadata.size,
                    modified_time=metadata.server_modified,
                    extension=os.path.splitext(metadata.name)[1].lstrip(".").lower(),
                    metadata={
                        "id": metadata.id,
                        "client_modified": metadata.client_modified,
                        "rev": metadata.rev,
                    }
                )

                if criterion_loader.verify_criteria(file_record):
                    if os.getenv("TESTMODE") == "1":
                        logger.info(f"File {file_record.name} passed all criteria and would be moved to /FullSize Images/")
                    else:
                        dropbox_client.move_file(file_record.path, f"/FullSize Images/{file_record.name}")
        
                    break
        
