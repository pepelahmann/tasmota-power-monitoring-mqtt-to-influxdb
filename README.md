# Tasmota Power Monitoring → MQTT → InfluxDB 2

📡 Dieses Tool liest Energiewerte von Tasmota-Smartplugs über MQTT aus und schreibt sie in eine InfluxDB 2.x Instanz.

---

## 🚀 Installation mit Docker

### 🧾 Voraussetzungen

- Docker
- MQTT-Broker (z. B. Mosquitto oder ein anderer MQTT-Dienst)
- InfluxDB 2.x (getestet mit 2.7+)

---

## ⚙️ Setup

### 1. Repository klonen

```bash
git clone https://github.com/pepelahmann/tasmota-power-monitoring-mqtt-to-influxdb.git
cd tasmota-power-monitoring-mqtt-to-influxdb
