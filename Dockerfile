FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY newsletter.py .

# Default: run once immediately (Railway Cron will call this container daily)
CMD ["python", "newsletter.py"]
