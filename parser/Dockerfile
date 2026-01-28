# 使用官方 Python 3.9 基礎映像
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 安裝必要的 Python 套件
RUN pip install --no-cache-dir \
    flask==2.3.3 \
    flask-cors==4.0.0 \
    influxdb==5.3.1

# 複製 parser.py 到容器中
COPY parser.py /app/

# 暴露 Flask 預設埠號
EXPOSE 5000

# 啟動 Flask 應用
CMD ["python", "parser.py"]
