from helpers.getActiveProducts import main as get_active_products
from rules.criterion_loader import CriterionLoader
from models.file_record import FileRecord
from clients.dropbox_client import DropboxClient
from helpers.logger import setup_logger
from dotenv import load_dotenv
import csv
import re
import os
import sys

if __name__ == "__main__":

    load_dotenv()

    dropbox_key = os.getenv("DROPBOX_KEY")
    move_path = os.getenv("MOVE_PATH")

    if not os.path.exists("resources/active_files.csv"):
        raise FileNotFoundError("Active files file not found inside resources/active_files.csv. Please generate the file.")

    logger = setup_logger()
    criterion_loader = CriterionLoader("config/criteria.json", logger=logger)
    dropbox_client = DropboxClient(token=dropbox_key, logger=logger)

    with open("resources/active_files.csv", mode='r') as csv_file:
        file_names = csv.DictReader(csv_file)
        for file_name in file_names:
            re_pattern = re.compile(r'\b' + re.escape(file_name['Name']) + r'\b', re.IGNORECASE)
            matches = dropbox_client.search_files(file_name['Name'])

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
                        logger.info(f"File {file_record.name} passed all criteria and would be moved to {move_path}/")
                    else:
                        dropbox_client.move_file(file_record.path, f"{move_path}/{file_record.name}")
        
                    break
        
