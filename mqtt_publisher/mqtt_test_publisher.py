#!/usr/bin/env python3
"""
MQTT 測試資料發布器
用於向 mosquitto 發布大量 JSON 資料以測試 InfluxDB
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import os
from datetime import datetime

# MQTT 配置 - 從環境變數或使用預設值
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "app055/data")

# 測試配置
NUM_DEVICES = 10  # 模擬設備數量
PUBLISH_INTERVAL = 0.5  # 發布間隔（秒）

def generate_sensor_data(device_id):
    """生成模擬的感測器資料"""
    return {
        "id": str(device_id),
        "name": f"Plant_{device_id}",
        "ph": round(random.uniform(5.5, 8.0), 2),
        "moisture": round(random.uniform(20.0, 80.0), 2),
        "co2": round(random.uniform(300.0, 1000.0), 2),
        "o2": round(random.uniform(18.0, 22.0), 2),
        "nh3": round(random.uniform(0.0, 10.0), 2),
        "h2s": round(random.uniform(0.0, 5.0), 2),
        "temp": round(random.uniform(18.0, 35.0), 2),
        "humidity": round(random.uniform(30.0, 90.0), 2),
        "timestamp": datetime.now().isoformat()
    }

def on_connect(client, userdata, flags, rc):
    """連接回調函數"""
    if rc == 0:
        print(f"✅ 成功連接到 MQTT Broker ({MQTT_BROKER}:{MQTT_PORT})")
        print(f"📡 發布主題: {MQTT_TOPIC}")
        print(f"🔢 模擬設備數量: {NUM_DEVICES}")
        print(f"⏱️  發布間隔: {PUBLISH_INTERVAL} 秒")
        print("-" * 60)
    else:
        print(f"❌ 連接失敗，錯誤代碼: {rc}")

def on_publish(client, userdata, mid):
    """發布回調函數"""
    pass  # 不打印每次發布，避免輸出過多

def main():
    """主函數"""
    # 創建 MQTT 客戶端
    client = mqtt.Client(client_id="test_publisher")
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        # 連接到 MQTT Broker
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        # 等待連接建立
        time.sleep(1)
        
        message_count = 0
        device_id = 1
        
        print("🚀 開始發布測試資料...\n")
        
        while True:
            # 輪流為不同設備發布資料
            data = generate_sensor_data(device_id)
            
            # 發布到 MQTT
            result = client.publish(MQTT_TOPIC, json.dumps(data), qos=0)
            
            message_count += 1
            
            # 每 10 條消息顯示一次統計
            if message_count % 10 == 0:
                print(f"📊 已發布 {message_count} 條消息 | "
                      f"設備 {device_id}: pH={data['ph']}, "
                      f"溫度={data['temp']}°C, "
                      f"濕度={data['humidity']}%")
            
            # 切換到下一個設備
            device_id = (device_id % NUM_DEVICES) + 1
            
            # 等待間隔
            time.sleep(PUBLISH_INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n\n⏹️  停止發布")
        print(f"📈 總共發布了 {message_count} 條消息")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        print("👋 已斷開連接")

if __name__ == "__main__":
    main()
