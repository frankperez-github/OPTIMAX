FROM python:3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --default-timeout=100 --upgrade pip && \
    pip install --default-timeout=100 --no-cache-dir -r requirements.txt


COPY . .

CMD ["python3", "main.py", "problem.json"]
