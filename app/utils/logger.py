import logging
import sys

def get_logger(name: str = "app", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.propagate = False
    return logger

# Example usage:
# logger = get_logger(__name__)
# logger.info("Logger initialized.")