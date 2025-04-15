FROM python:3.12 as base

# Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/code \
    UV_NO_VENV=True \
    UV_PYTHON_INSTALL_DIR="/python" \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON=python3.12 \
    PYTHON_PREFERENCE=system \
    UV_NO_CACHE=True

WORKDIR /code

# Обновляем pip и устанавливаем uv
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir uv==0.5.3

# Копируем зависимость и устанавливаем их
COPY pyproject.toml /code/
RUN uv sync && uv cache clean

# Создаём директории для кеша и логов с корректными правами
#RUN #mkdir -p /code/.cache /code/logs && chmod -R 777 /code

# Меняем владельца директории на пользователя с UID 1001
RUN chown -R 1001:1001 /code

# Переключаемся на непривилегированного пользователя
USER 1001

