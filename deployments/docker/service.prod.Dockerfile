# Используем официальный образ Python 3.12
FROM python:3.12 as base

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    UV_NO_VENV=True \
    UV_PYTHON_INSTALL_DIR="/python" \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON=python3.12 \
    PYTHON_PREFERENCE=system \
    UV_NO_CACHE=True

# Устанавливаем рабочую директорию
WORKDIR /app

# Обновляем pip и устанавливаем uv
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir uv==0.5.3

# Копируем проект в рабочую директорию контейнера
COPY . /app

# Создаем необходимые директории и задаем права
RUN chmod +x /app/scripts/startup.sh \
    && ls -la /app \
    && cat /app/pyproject.toml

# Устанавливаем зависимости проекта
RUN uv sync && uv cache clean

# Меняем владельца директории
RUN chown -R 1001:1001 /app

# Переключаемся на непривилегированного пользователя
USER 1001

