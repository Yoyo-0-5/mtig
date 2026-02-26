#!/usr/bin/env python3
"""
MQTT 批量測試資料發布器
用於快速發布大量資料進行壓力測試
"""

import paho.mqtt.client as mqtt
import json
import time
import random
import os
from datetime import datetime, timedelta
import argparse

# MQTT 配置 - 從環境變數或使用預設值
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "app055/data")

def generate_sensor_data(device_id, timestamp=None):
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
        "timestamp": (timestamp or datetime.now()).isoformat()
    }

def batch_publish(num_messages, num_devices, rate_per_second=100):
    """批量發布資料"""
    client = mqtt.Client(client_id="batch_publisher")
    
    try:
        print(f"🔗 連接到 {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        time.sleep(1)
        
        print(f"📤 開始批量發布...")
        print(f"   - 總消息數: {num_messages}")
        print(f"   - 設備數: {num_devices}")
        print(f"   - 發送速率: {rate_per_second} msg/s")
        print("-" * 60)
        
        interval = 1.0 / rate_per_second
        start_time = time.time()
        
        for i in range(num_messages):
            device_id = (i % num_devices) + 1
            data = generate_sensor_data(device_id)
            
            client.publish(MQTT_TOPIC, json.dumps(data), qos=0)
            
            if (i + 1) % 100 == 0:
                elapsed = time.time() - start_time
                rate = (i + 1) / elapsed
                print(f"✅ 已發送 {i + 1}/{num_messages} | "
                      f"速率: {rate:.1f} msg/s | "
                      f"設備 ID: {device_id}")
            
            time.sleep(interval)
        
        # 等待所有消息發送完成
        time.sleep(2)
        
        total_time = time.time() - start_time
        actual_rate = num_messages / total_time
        
        print("\n" + "=" * 60)
        print(f"✨ 完成!")
        print(f"   - 總消息數: {num_messages}")
        print(f"   - 總耗時: {total_time:.2f} 秒")
        print(f"   - 平均速率: {actual_rate:.1f} msg/s")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    finally:
        client.loop_stop()
        client.disconnect()

def historical_data_publish(num_devices, hours_back=24, interval_minutes=5):
    """發布歷史資料（用於填充資料庫）"""
    client = mqtt.Client(client_id="historical_publisher")
    
    try:
        print(f"🔗 連接到 {MQTT_BROKER}:{MQTT_PORT}...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        time.sleep(1)
        
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours_back)
        current_time = start_time
        
        total_points = int(hours_back * 60 / interval_minutes)
        print(f"📅 發布歷史資料...")
        print(f"   - 時間範圍: {start_time.strftime('%Y-%m-%d %H:%M')} ~ {end_time.strftime('%Y-%m-%d %H:%M')}")
        print(f"   - 設備數: {num_devices}")
        print(f"   - 資料間隔: {interval_minutes} 分鐘")
        print(f"   - 每設備資料點: {total_points}")
        print("-" * 60)
        
        count = 0
        while current_time <= end_time:
            for device_id in range(1, num_devices + 1):
                data = generate_sensor_data(device_id, current_time)
                client.publish(MQTT_TOPIC, json.dumps(data), qos=0)
                count += 1
                
                if count % 100 == 0:
                    print(f"✅ 已發送 {count} 條 | 時間: {current_time.strftime('%Y-%m-%d %H:%M')}")
            
            current_time += timedelta(minutes=interval_minutes)
            time.sleep(0.01)  # 快速發送
        
        time.sleep(2)
        
        print("\n" + "=" * 60)
        print(f"✨ 完成! 共發布 {count} 條歷史資料")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    finally:
        client.loop_stop()
        client.disconnect()

def main():
    parser = argparse.ArgumentParser(description='MQTT 批量測試資料發布器')
    parser.add_argument('--mode', choices=['batch', 'historical'], default='batch',
                        help='發布模式: batch (批量) 或 historical (歷史資料)')
    parser.add_argument('--messages', type=int, default=1000,
                        help='批量模式: 要發送的消息總數 (預設: 1000)')
    parser.add_argument('--devices', type=int, default=10,
                        help='模擬的設備數量 (預設: 10)')
    parser.add_argument('--rate', type=int, default=100,
                        help='批量模式: 每秒發送速率 (預設: 100)')
    parser.add_argument('--hours', type=int, default=24,
                        help='歷史模式: 往前追溯的小時數 (預設: 24)')
    parser.add_argument('--interval', type=int, default=5,
                        help='歷史模式: 資料間隔分鐘數 (預設: 5)')
    parser.add_argument('--broker', type=str, default=None,
                        help='MQTT Broker 地址 (預設: 從環境變數 MQTT_BROKER 讀取，或 localhost)')
    
    args = parser.parse_args()
    
    global MQTT_BROKER
    # 只有在命令列提供了 --broker 參數時才覆蓋環境變數
    if args.broker:
        MQTT_BROKER = args.broker
    
    if args.mode == 'batch':
        batch_publish(args.messages, args.devices, args.rate)
    else:
        historical_data_publish(args.devices, args.hours, args.interval)

if __name__ == "__main__":
    main()
