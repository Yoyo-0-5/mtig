FROM python:3.11-slim

WORKDIR /app

# 安裝必要的套件
RUN pip install --no-cache-dir paho-mqtt

# 複製腳本
COPY mqtt_test_publisher.py .
COPY mqtt_batch_publisher.py .
COPY test_connection.py .

CMD ["python", "mqtt_test_publisher.py"]
