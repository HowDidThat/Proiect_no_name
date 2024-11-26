import time
from datetime import datetime
from functools import wraps

from .base import BaseAspect, logger


class QuizMonitoringAspect(BaseAspect):
    @classmethod
    def monitor_quiz_operations(cls):
        def aspect(method):
            @wraps(method)
            def wrapper(request, *args, **kwargs):
                start_time = time.time()
                endpoint_name = method.__name__

                try:
                    result = method(request, *args, **kwargs)
                    execution_time = time.time() - start_time

                    service_name = method.__module__.split('.')[-1]
                    metrics = {
                        'service': service_name,
                        'operation': endpoint_name,
                        'execution_time': f"{execution_time:.2f}s",
                        'timestamp': datetime.now().isoformat()
                    }
                    logger.info(f"Operation metrics: {metrics}")
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    logger.error(f"Error in {endpoint_name} after {execution_time:.2f}s: {str(e)}")
                    raise

            return wrapper

        return aspect
