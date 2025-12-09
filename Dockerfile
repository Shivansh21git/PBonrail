# Use a stable Python image
FROM python:3.10-slim

# Prevent .pyc creation and improve logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install required system packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# ⚠️ DO NOT run collectstatic during build in Railway
# Django settings will fail because DATABASE_URL is not present yet.
# Instead: let Railway run collectstatic via Release Phase.
# RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Gunicorn command
CMD ["bash", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn backend.wsgi:application --bind 0.0.0.0:8000"]

