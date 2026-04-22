import logging
from datetime import datetime
from pathlib import Path

def setup_logger():
    # Persist logs under /app/output so the compose bind mount captures them.
    logger = logging.getLogger('DropboxImageSearcher')
    logger.setLevel(logging.INFO)

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    fh = logging.FileHandler(output_dir / f'app_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log')
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info(f'*** Logger initialized - Session {datetime.now().strftime("%Y-%m-%d_%H-%M-%S")} ***')

    return logger
