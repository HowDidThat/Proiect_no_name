import logging
from functools import wraps
import time

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print(f"Execution time for {func.__name__}: {elapsed_time:.2f} seconds")
        return result
    return wrapper


def clean_and_validate_data(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = kwargs.get('payload')
        if data:
            symptoms = [s.lower().replace(' ', '_') for s in data.symptoms]
            data.symptoms = symptoms
        print("Clean and validate data decorator")
        print(f"Cleaned data: {data}")
        return func(*args, **kwargs)
    return wrapper
