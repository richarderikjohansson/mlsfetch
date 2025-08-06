import logging
from datetime import datetime
from pathlib import Path


def get_runtime_logger() -> logging.Logger:
    logger = logging.getLogger("runtime_logger")
    if not logger.hasHandlers():  # Prevent adding handlers multiple times
        logger.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_format = logging.Formatter("[%(levelname)s] %(message)s")
        console_handler.setFormatter(console_format)

        logger.addHandler(console_handler)
        logger.propagate = False
    return logger


def get_download_logger(savedir: str) -> logging.Logger:
    now = datetime.now()
    datestr = now.strftime("%Y-%m-%d_%H:%M:%S")
    logger = logging.getLogger("download_logger")
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        logdir = Path(f"{savedir}/log")
        logname = f"{datestr}.log"

        if not logdir.exists():
            logdir.mkdir()

        file_handler = logging.FileHandler(logdir / logname)
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter("%(asctime)s - %(message)s")
        file_handler.setFormatter(file_format)

        logger.addHandler(file_handler)
        logger.propagate = False
    return logger
