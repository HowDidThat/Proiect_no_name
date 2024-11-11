import logging
from functools import wraps

def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Executing {func.__name__}")
        result = func(*args, **kwargs)
        logging.info(f"Finished {func.__name__}")
        return result
    return wrapper
