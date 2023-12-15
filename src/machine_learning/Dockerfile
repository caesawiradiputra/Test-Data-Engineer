# Dockerfile in app/
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y postgresql-server-dev-all
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "dummy_model.py"]
