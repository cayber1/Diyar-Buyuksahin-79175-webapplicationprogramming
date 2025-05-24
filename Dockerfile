# Python base image
FROM python:3.11-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli dosyaları kopyala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Django sunucusunu başlat
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]