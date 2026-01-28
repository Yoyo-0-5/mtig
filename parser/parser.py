from flask import Flask, jsonify
from influxdb import InfluxDBClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- 跨電腦連線設定 ---
# 💡 電腦 B 的 IP 地址 (運行 InfluxDB 的那台)
INFLUX_HOST = '192.168.50.209'
# 💡 InfluxDB 預設埠號
INFLUX_PORT = 8086
# 💡 對應 .env 中的 INFLUXDB_DATABASE
INFLUX_DB = 'metrics'
MEASUREMENT = 'mqtt_consumer'

client = InfluxDBClient(host=INFLUX_HOST, port=INFLUX_PORT, database=INFLUX_DB)

@app.route('/api/all_data', methods=['GET'])
def get_all_plants():
    try:
        # 💡 修正 1：移除 GROUP BY，直接抓取最近資料
        # 因為您的 id 是 Field 不是 Tag，不能在 InfluxDB 裡 GROUP BY
        query = f'SELECT * FROM "{MEASUREMENT}" ORDER BY time DESC LIMIT 100'
        result = client.query(query)

        # 💡 修正 2：直接使用 get_points()，這是最穩定的抓取方式
        points = list(result.get_points())

        if not points:
            print("資料庫內 mqtt_consumer 表是空的")
            return jsonify([])

        # 在 Python 中手動過濾重複的 id，只留最新的一筆
        plants_dict = {}
        for p in points:
            pid = str(p.get('id', ''))
            if not pid: continue

            # 因為是按時間倒序排，第一筆看到的 ID 就是最新的
            if pid not in plants_dict:
                plants_dict[pid] = {
                    "id": pid,
                    "name": p.get('name', '未命名'),
                    "ph": float(p.get('ph') or 7.0),
                    "moisture": float(p.get('moisture') or 0.0),
                    "co2": float(p.get('co2') or 400.0),
                    "o2": float(p.get('o2') or 20.9),
                    "nh3": float(p.get('nh3') or 0.0),
                    "h2s": float(p.get('h2s') or 0.0),
                    "temp": float(p.get('temp') or 25.0),      # 💡 新增：環境溫度
                    "humidity": float(p.get('humidity') or 60.0), # 💡 新增：環境濕度
                    "time": p.get('time')
                }

        # 轉回 List 格式傳給 Flutter
        final_list = list(plants_dict.values())
        print(f"成功找到 {len(final_list)} 盆植物: {final_list}")
        return jsonify(final_list)

    except Exception as e:
        print(f"解析崩潰細節: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/<node_id>', methods=['GET'])
def get_plant_history(node_id):
    try:
        # 抓取特定盆栽的歷史紀錄
        query = f'SELECT * FROM "{MEASUREMENT}" WHERE id=\'{node_id}\' ORDER BY time DESC LIMIT 50'
        result = client.query(query)
        return jsonify(list(result.get_points()))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # 啟動伺服器
    app.run(host='0.0.0.0', port=5000, debug=True)