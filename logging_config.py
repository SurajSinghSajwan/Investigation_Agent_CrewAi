import logging
import json
from datetime import datetime
from pathlib import Path


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        extra_data = getattr(record, "extra_data", None)
        if isinstance(extra_data, dict):
            payload.update(extra_data)

        return json.dumps(payload)


def setup_logger():
    logger = logging.getLogger("investigation_agent")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(log_dir / "execution.log")
    file_handler.setFormatter(JsonFormatter())

    logger.handlers.clear()
    logger.addHandler(file_handler)

    return logger
