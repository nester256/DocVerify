import logging
from contextvars import ContextVar

import yaml

# Чтение конфигурации логирования
with open("conf/logging.conf.yml", "r") as f:
    LOGGING_CONFIG = yaml.full_load(f)


import json


class ConsoleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "logger_name": record.name,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        # Добавить correlation_id, если доступен
        try:
            log_record["correlation_id"] = correlation_id_ctx.get()
        except LookupError:
            log_record["correlation_id"] = None  # type: ignore

        # Добавить информацию об ошибке, если она есть
        if record.exc_info:
            log_record["error"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


# Контекст для correlation_id
correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id_ctx")

# Создание логгера
logger = logging.getLogger("doc-verify")
logger.setLevel(logging.INFO)

# Обработчик для вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Настройка JSON форматирования
formatter = ConsoleFormatter()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
