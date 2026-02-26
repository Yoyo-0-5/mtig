#!/usr/bin/env python3
"""
MQTT 連接測試
用於驗證 MQTT Broker 是否正常運作
"""

import paho.mqtt.client as mqtt
import json
import sys
import os
from datetime import datetime

# 從環境變數或使用預設值
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "app055/data")

def on_connect(client, userdata, flags, rc):
    """連接回調"""
    if rc == 0:
        print("✅ MQTT 連接成功!")
        print(f"   Broker: {MQTT_BROKER}:{MQTT_PORT}")
        print(f"   主題: {MQTT_TOPIC}\n")
        
        # 發送測試消息
        test_data = {
            "id": "test_001",
            "name": "Test_Device",
            "ph": 7.0,
            "moisture": 50.0,
            "co2": 400.0,
            "o2": 21.0,
            "nh3": 0.0,
            "h2s": 0.0,
            "temp": 25.0,
            "humidity": 60.0,
            "timestamp": datetime.now().isoformat()
        }
        
        print("📤 發送測試消息...")
        result = client.publish(MQTT_TOPIC, json.dumps(test_data), qos=0)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print("✅ 測試消息發送成功!")
            print(f"   資料: {json.dumps(test_data, indent=2)}")
        else:
            print(f"❌ 測試消息發送失敗，錯誤代碼: {result.rc}")
            
    else:
        print(f"❌ MQTT 連接失敗，錯誤代碼: {rc}")
        error_messages = {
            1: "不正確的協議版本",
            2: "無效的客戶端 ID",
            3: "伺服器不可用",
            4: "錯誤的用戶名或密碼",
            5: "未授權"
        }
        print(f"   錯誤: {error_messages.get(rc, '未知錯誤')}")
        sys.exit(1)

def main():
    print("=" * 60)
    print("🧪 MQTT 連接測試工具")
    print("=" * 60 + "\n")
    
    print(f"🔗 嘗試連接到 {MQTT_BROKER}:{MQTT_PORT}...\n")
    
    client = mqtt.Client(client_id="connection_test")
    client.on_connect = on_connect
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        # 等待連接和發送完成
        import time
        time.sleep(3)
        
        client.loop_stop()
        client.disconnect()
        
        print("\n" + "=" * 60)
        print("✨ 測試完成!")
        print("=" * 60)
        
    except ConnectionRefusedError:
        print(f"❌ 連接被拒絕，請確認:")
        print(f"   1. MQTT Broker 是否正在運行")
        print(f"   2. 地址 {MQTT_BROKER}:{MQTT_PORT} 是否正確")
        print(f"   3. 防火牆是否允許連接")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
