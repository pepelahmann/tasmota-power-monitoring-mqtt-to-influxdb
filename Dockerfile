FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir paho-mqtt influxdb-client

CMD ["python", "main.py"]
