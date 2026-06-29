import logging
from pathlib import Path

Log_DIR = Path("logs")
Log_DIR.mkdir(exist_ok = True)

Log_File = Log_DIR / "application.log"

def setup_logging():
    logging.basicConfig(
        level = logging.INFO,
        format = '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        handlers = [
            logging.FileHandler(Log_File),
            logging.StreamHandler(),
        ],
    )