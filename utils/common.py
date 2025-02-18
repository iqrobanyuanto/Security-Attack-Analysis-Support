import logging


logging.basicConfig(level=logging.INFO)

def log_Info(msg: str):
    logger = logging.getLogger(">> ")
    logger.info(msg)

def log_error(location:str, msg: str):
    logger = logging.getLogger(f"[{location}]")
    logger.error(msg)