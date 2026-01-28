# Mosquitto

### **clone安裝包**

```bash
git clone https://github.com/Yoyo-0-5/mtig.git
cd mtig
```

### 安裝 docker (若沒安裝docker)

刪除衝突 (若安裝過docker相關套件)

```bash
sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)
```

安裝

```bash
sudo apt update
sudo apt install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### 部屬

使用docker compose

```bash
docker compose up
```

### 測試方法

```bash
docker exec -it mosquitto sh
```

訂閱

```bash
mosquitto_sub -h localhost -t test -v
```

發送訊息

```bash
mosquitto_pub -h localhost -t test -m "Hello MQTT!"
```

### 資料庫

```bash
mosquitto_pub -h 127.0.0.1 -p 1883 -t "sensor/data" -m '{"id":"01","name":"玫瑰花","ph":7.0,"moisture":50.0,"co2":400.0,"o2":20.9,"nh3":0.1,"h2s":0.0,"isAuto":true}'
```

測試MQTT是否收入資料庫

```bash
docker exec mtig_influxdb influx -database 'metrics' -execute "SELECT * FROM mqtt_consumer WHERE time > now() - 5m ORDER BY time DESC LIMIT 10"
```
