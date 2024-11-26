import logging
from typing import Any

logging.basicConfig(
    filename='medical_quiz.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseAspect:
    @staticmethod
    def get_request_from_args(args) -> Any:
        return args[0] if args else None
