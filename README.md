# Tasmota Power Monitoring → MQTT → InfluxDB

📡 Liest Energiewerte von Tasmota-Steckdosen über MQTT und schreibt sie in InfluxDB.

---

## 🚀 Installation mit Docker

### 🧾 Voraussetzungen

- Docker
- MQTT-Broker (z. B. Mosquitto)
- InfluxDB (getestet mit Version 1.x)

---

## ⚙️ Setup

```bash
# Repository klonen
git clone https://github.com/pepelahmann/tasmota-power-monitoring-mqtt-to-influxdb.git
cd tasmota-power-monitoring-mqtt-to-influxdb

# .env Datei anlegen
cp .env.example .env
# Dann .env mit deinen Werten bearbeiten (MQTT / InfluxDB)

# Docker-Image bauen
docker build -t tasmota-monitor .

# Container starten
docker run --env-file .env tasmota-monitor
