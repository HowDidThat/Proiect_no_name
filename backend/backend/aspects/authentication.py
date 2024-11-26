from functools import wraps

from .base import BaseAspect, logger


class AuthenticationAspect(BaseAspect):
    @classmethod
    def audit_auth(cls):
        def aspect(method):
            @wraps(method)
            def wrapper(*args, **kwargs):
                request = cls.get_request_from_args(args)

                if not request:
                    logger.error("No request object found")
                    raise ValueError("Request object required")

                try:
                    user_id = getattr(request.user, 'id', 'anonymous')
                    endpoint = method.__name__

                    logger.info(f"Access attempt - User: {user_id} | Endpoint: {endpoint}")
                    result = method(*args, **kwargs)
                    logger.info(f"Success - User: {user_id} | Endpoint: {endpoint}")

                    return result
                except Exception as e:
                    logger.warning(f"Failed - Endpoint: {endpoint} | Error: {str(e)}")
                    raise

            return wrapper

        return aspect
