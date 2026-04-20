import logging
from datetime import datetime

def setup_logger():
    #Create a logger
    logger = logging.getLogger('DropboxImageSearcher')
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(f'app_{datetime.now().strftime("%Y-%m-%d")}.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info(f'*** Logger initialized - Session {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ***')

    return logger
