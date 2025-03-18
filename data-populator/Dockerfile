FROM python:3.10-slim

# Install required dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev

WORKDIR /app

COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "populate_db.py"]
