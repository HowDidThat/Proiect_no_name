from functools import wraps
from http import HTTPStatus

from django.core.cache import cache
from ninja.responses import Response

from .base import BaseAspect, logger


class RateLimitingAspect(BaseAspect):
    RATE_LIMITS = {
        'register': {'max_requests': 3000, 'window': 3600},
        'login': {'max_requests': 5000, 'window': 300},
        'quiz_creation': {'max_requests': 20000, 'window': 7200},
        'quiz_submission': {'max_requests': 50000, 'window': 1800},
        'default': {'max_requests': 15000, 'window': 3600}
    }

    @classmethod
    def limit_rate(cls, endpoint_type='default'):
        def aspect(method):
            @wraps(method)
            def wrapper(request, *args, **kwargs):
                limits = cls.RATE_LIMITS.get(
                    endpoint_type,
                    cls.RATE_LIMITS['default']
                )

                identifier = getattr(request.user, 'id', request.get_host())
                endpoint = method.__name__
                rate_key = f"rate_limit_{identifier}_{endpoint}"

                request_count = cache.get(rate_key, 0)
                if request_count >= limits['max_requests']:
                    logger.warning(f"Rate limit exceeded - Identifier: {identifier}")

                    time_window_minutes = limits['window'] // 60

                    return Response(
                        {"detail": f"Too many requests. Please try again in {time_window_minutes} minutes."},
                        status=HTTPStatus.TOO_MANY_REQUESTS
                    )

                cache.set(rate_key, request_count + 1, timeout=limits['window'])
                return method(request, *args, **kwargs)

            return wrapper

        return aspect
