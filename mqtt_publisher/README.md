# MQTT 測試資料發布器

用於向 mosquitto 發布大量 JSON 測試資料以測試 InfluxDB 性能。

## 📁 檔案說明

- `mqtt_test_publisher.py` - 持續發布測試資料（模擬真實場景）
- `mqtt_batch_publisher.py` - 批量發布/歷史資料填充
- `Dockerfile` - Docker 容器配置

## 🚀 使用方式

### 快速開始（推薦）

#### 使用快速啟動腳本
```bash
cd /home/yoyo/mtig/mqtt_publisher
./start.sh
```
互動式選單讓你輕鬆選擇測試模式！

### 方式一：直接在宿主機執行

#### 1. 測試連接
```bash
# 先測試 MQTT 連接是否正常
python3 test_connection.py
```

#### 2. 安裝依賴
```bash
pip3 install -r requirements.txt
# 或
pip3 install paho-mqtt
```

#### 2. 持續發布測試資料
```bash
python mqtt_test_publisher.py
```
- 預設每 0.5 秒發布一條資料
- 模擬 10 個設備輪流發送
- 按 Ctrl+C 停止

#### 3. 批量發布資料
```bash
# 快速發送 1000 條消息
python mqtt_batch_publisher.py --mode batch --messages 1000 --rate 100

# 發送 5000 條消息，速率 200 msg/s
python mqtt_batch_publisher.py --mode batch --messages 5000 --rate 200 --devices 20

# 填充 24 小時歷史資料（每 5 分鐘一個資料點）
python mqtt_batch_publisher.py --mode historical --hours 24 --interval 5 --devices 10

# 填充 7 天歷史資料（每 15 分鐘一個資料點）
python mqtt_batch_publisher.py --mode historical --hours 168 --interval 15 --devices 5
```

### 方式二：使用 Docker 運行

#### 1. 構建映像
```bash
cd /home/yoyo/mtig/mqtt_publisher
docker build -t mqtt-publisher .
```

#### 2. 運行容器（持續發布）
```bash
docker run --rm --network mtig_backend \
  -e MQTT_BROKER=mtig_mosquitto \
  mqtt-publisher
```

#### 3. 運行容器（批量發布）
```bash
# 批量模式
docker run --rm --network mtig_backend \
  mqtt-publisher python mqtt_batch_publisher.py \
  --broker mtig_mosquitto --mode batch --messages 5000 --rate 200

# 歷史資料模式
docker run --rm --network mtig_backend \
  mqtt-publisher python mqtt_batch_publisher.py \
  --broker mtig_mosquitto --mode historical --hours 48 --interval 10
```

## 📊 資料格式

發布的 JSON 資料格式：
```json
{
  "id": "1",
  "name": "Plant_1",
  "ph": 6.8,
  "moisture": 55.3,
  "co2": 450.2,
  "o2": 20.5,
  "nh3": 2.3,
  "h2s": 0.8,
  "temp": 25.6,
  "humidity": 65.4,
  "timestamp": "2026-02-26T12:30:45.123456"
}
```

## ⚙️ 參數說明

### mqtt_batch_publisher.py 參數

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--mode` | 模式：`batch` 或 `historical` | batch |
| `--messages` | 批量模式：消息總數 | 1000 |
| `--devices` | 模擬設備數量 | 10 |
| `--rate` | 批量模式：每秒發送速率 | 100 |
| `--hours` | 歷史模式：往前追溯小時數 | 24 |
| `--interval` | 歷史模式：資料間隔分鐘數 | 5 |
| `--broker` | MQTT Broker 地址 | localhost |

## 💡 使用場景

### 1. 性能測試
```bash
# 測試系統每秒 500 條消息的處理能力
python mqtt_batch_publisher.py --mode batch --messages 10000 --rate 500
```

### 2. 資料填充
```bash
# 為 Grafana 視覺化準備歷史資料
python mqtt_batch_publisher.py --mode historical --hours 168 --interval 10
```

### 3. 壓力測試
```bash
# 持續高頻發送測試系統穩定性
# 修改 mqtt_test_publisher.py 中的 PUBLISH_INTERVAL = 0.01
python mqtt_test_publisher.py
```

## 🔍 監控

### 查看 InfluxDB 資料
```bash
# 進入 InfluxDB 容器
docker exec -it mtig_influxdb influx

# 使用資料庫
USE metrics

# 查看資料量
SELECT COUNT(*) FROM mqtt_consumer

# 查看最新資料
SELECT * FROM mqtt_consumer ORDER BY time DESC LIMIT 10
```

### 查看 Telegraf 日誌
```bash
docker logs -f mtig_telegraf
```

### 查看 Mosquitto 日誌
```bash
docker logs -f mtig_mosquitto
# 或
cat mosquitto/log/mosquitto.log
```

## 🎯 建議測試流程

1. **小規模測試** - 先發送 100 條消息確認流程正常
   ```bash
   python mqtt_batch_publisher.py --mode batch --messages 100 --rate 10
   ```

2. **中規模測試** - 測試 1000 條消息的處理
   ```bash
   python mqtt_batch_publisher.py --mode batch --messages 1000 --rate 50
   ```

3. **大規模測試** - 測試系統極限
   ```bash
   python mqtt_batch_publisher.py --mode batch --messages 10000 --rate 200
   ```

4. **持續測試** - 長時間運行測試穩定性
   ```bash
   python mqtt_test_publisher.py
   # 運行數小時或過夜
   ```

5. **填充歷史資料** - 為視覺化準備資料
   ```bash
   python mqtt_batch_publisher.py --mode historical --hours 168 --interval 5
   ```
