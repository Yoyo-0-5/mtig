# 🚀 MQTT 測試資料發布器 - 快速使用指南

## 📋 目錄結構

```
mqtt_publisher/
├── mqtt_test_publisher.py      # 持續發布測試資料
├── mqtt_batch_publisher.py     # 批量/歷史資料發布
├── test_connection.py          # 連接測試腳本
├── Dockerfile                  # Docker 配置
├── requirements.txt            # Python 依賴
├── start.sh                    # 快速啟動腳本
└── README.md                   # 詳細文檔
```

## ⚡ 快速開始

### 1️⃣ 測試連接
```bash
sudo docker run --rm --network mtig_backend \
  -e MQTT_BROKER=mtig_mosquitto \
  mqtt-publisher python test_connection.py
```

### 2️⃣ 批量發布測試（100 條消息）
```bash
sudo docker run --rm --network mtig_backend \
  -e MQTT_BROKER=mtig_mosquitto \
  mqtt-publisher python mqtt_batch_publisher.py \
  --mode batch --messages 100 --rate 20 --devices 5
```

### 3️⃣ 持續發布測試（模擬真實場景）
```bash
sudo docker run --rm --network mtig_backend \
  -e MQTT_BROKER=mtig_mosquitto \
  mqtt-publisher python mqtt_test_publisher.py
```
按 Ctrl+C 停止

### 4️⃣ 填充歷史資料（24 小時）
```bash
sudo docker run --rm --network mtig_backend \
  -e MQTT_BROKER=mtig_mosquitto \
  mqtt-publisher python mqtt_batch_publisher.py \
  --mode historical --hours 24 --interval 5 --devices 10
```

## 🎯 常用測試場景

### 📊 小規模測試（驗證流程）
```bash
# 發送 100 條消息，速率 10 msg/s
sudo docker run --rm --network mtig_backend \
  -e MQTT_BROKER=mtig_mosquitto \
  mqtt-publisher python mqtt_batch_publisher.py \
  --mode batch --messages 100 --rate 10
```

### 🔥 中規模測試（性能測試）
```bash
# 發送 1000 條消息，速率 50 msg/s
sudo docker run --rm --network mtig_backend \
  -e MQTT_BROKER=mtig_mosquitto \
  mqtt-publisher python mqtt_batch_publisher.py \
  --mode batch --messages 1000 --rate 50
```

### 🚀 大規模測試（壓力測試）
```bash
# 發送 10000 條消息，速率 200 msg/s
sudo docker run --rm --network mtig_backend \
  -e MQTT_BROKER=mtig_mosquitto \
  mqtt-publisher python mqtt_batch_publisher.py \
  --mode batch --messages 10000 --rate 200 --devices 20
```

### 📅 填充歷史資料（視覺化準備）
```bash
# 填充 7 天歷史資料，每 15 分鐘一個資料點
sudo docker run --rm --network mtig_backend \
  -e MQTT_BROKER=mtig_mosquitto \
  mqtt-publisher python mqtt_batch_publisher.py \
  --mode historical --hours 168 --interval 15 --devices 10
```

## 🔍 監控和驗證

### 查看 MQTT 日誌
```bash
# 即時查看 mosquitto 日誌
sudo docker logs -f mtig_mosquitto

# 或查看日誌檔案
tail -f /home/yoyo/mtig/mosquitto/log/mosquitto.log
```

### 查看 Telegraf 日誌
```bash
# 確認資料是否被 telegraf 接收
sudo docker logs -f mtig_telegraf
```

### 查看 InfluxDB 資料
```bash
# 進入 InfluxDB 容器
sudo docker exec -it mtig_influxdb influx

# 在 InfluxDB shell 中執行：
USE metrics
SELECT COUNT(*) FROM mqtt_consumer
SELECT * FROM mqtt_consumer ORDER BY time DESC LIMIT 10
```

### 測試 Parser API
```bash
# 查詢所有設備資料
curl http://localhost:5000/api/all_data

# 查詢特定設備歷史
curl http://localhost:5000/api/history/1
```

## 📊 測試資料格式

發布的資料包含以下欄位：

| 欄位 | 類型 | 說明 | 範圍 |
|------|------|------|------|
| id | string | 設備 ID | "1", "2", ... |
| name | string | 設備名稱 | "Plant_1", "Plant_2", ... |
| ph | float | pH 值 | 5.5 - 8.0 |
| moisture | float | 土壤濕度 % | 20.0 - 80.0 |
| co2 | float | CO2 濃度 ppm | 300.0 - 1000.0 |
| o2 | float | O2 濃度 % | 18.0 - 22.0 |
| nh3 | float | NH3 濃度 ppm | 0.0 - 10.0 |
| h2s | float | H2S 濃度 ppm | 0.0 - 5.0 |
| temp | float | 溫度 °C | 18.0 - 35.0 |
| humidity | float | 濕度 % | 30.0 - 90.0 |
| timestamp | string | 時間戳 | ISO 8601 格式 |

## 🛠️ 參數完整清單

### mqtt_batch_publisher.py

```
--mode          發布模式 [batch|historical] (預設: batch)
--messages      批量模式：消息總數 (預設: 1000)
--devices       模擬設備數量 (預設: 10)
--rate          批量模式：每秒發送速率 (預設: 100)
--hours         歷史模式：往前追溯小時數 (預設: 24)
--interval      歷史模式：資料間隔分鐘數 (預設: 5)
--broker        MQTT Broker 地址 (可用環境變數 MQTT_BROKER)
```

### 環境變數

```
MQTT_BROKER     MQTT Broker 地址 (預設: localhost)
MQTT_PORT       MQTT 埠號 (預設: 1883)
MQTT_TOPIC      MQTT 主題 (預設: app055/data)
```

## 💡 提示和技巧

### 後台運行持續測試
```bash
# 使用 -d 在背景運行
sudo docker run -d --name mqtt-test \
  --network mtig_backend \
  -e MQTT_BROKER=mtig_mosquitto \
  mqtt-publisher python mqtt_test_publisher.py

# 查看日誌
sudo docker logs -f mqtt-test

# 停止測試
sudo docker stop mqtt-test
sudo docker rm mqtt-test
```

### 自訂發送間隔
編輯 `mqtt_test_publisher.py` 第 18 行：
```python
PUBLISH_INTERVAL = 0.5  # 改為 0.1 = 更快, 1.0 = 更慢
```

### 客製化資料範圍
編輯 `mqtt_batch_publisher.py` 或 `mqtt_test_publisher.py` 中的 `generate_sensor_data` 函數。

## ❓ 常見問題

### Q: 連接失敗怎麼辦？
A: 確認：
1. mosquitto 容器是否運行：`sudo docker ps | grep mosquitto`
2. 網路是否正確：使用 `mtig_backend` 網路
3. 環境變數是否設置：`-e MQTT_BROKER=mtig_mosquitto`

### Q: 資料沒有寫入 InfluxDB？
A: 檢查：
1. telegraf 是否運行且無錯誤
2. telegraf 配置的 topic 是否正確 (app055/data)
3. InfluxDB 連接是否正常

### Q: 如何提高發送速率？
A: 
- 使用 `--rate` 參數增加速率
- 注意：過高的速率可能導致系統無法處理

### Q: 如何測試系統極限？
A: 逐步增加發送速率，同時監控：
```bash
# 監控系統資源
htop

# 監控 Docker 容器
sudo docker stats
```

## 📚 更多資訊

詳細文檔請參閱：[README.md](README.md)

## 📞 支援

如遇問題，請檢查：
1. Docker 容器狀態：`sudo docker ps -a`
2. 容器日誌：`sudo docker logs <container_name>`
3. 網路連接：`sudo docker network inspect mtig_backend`
