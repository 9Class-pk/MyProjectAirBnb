FROM python:3.13-slim

# Корневая рабочая директория контейнера
WORKDIR /app

# Копируем только содержимое внутренней папки Django
COPY hotel_bnb/ /app

# Устанавливаем зависимости
COPY req.txt /app/
RUN pip install --no-cache-dir -r req.txt

# Переменные окружения
ENV DJANGO_SETTINGS_MODULE=hotel_bnb.settings
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["gunicorn", "hotel_bnb.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
