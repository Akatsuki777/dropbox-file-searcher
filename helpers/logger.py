import logging
from datetime import datetime
from pathlib import Path

def setup_logger():
    # Persist logs under /app/output so the compose bind mount captures them.
    logger = logging.getLogger('DropboxImageSearcher')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    session_id = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")

    for handler in list(logger.handlers):
        if isinstance(handler, logging.FileHandler):
            logger.removeHandler(handler)
            handler.close()

    fh = logging.FileHandler(output_dir / f"app_{session_id}.log")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logger.info(f'*** Logger initialized - Session {session_id} ***')

    return logger
