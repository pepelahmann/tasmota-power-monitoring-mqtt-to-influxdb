# Tasmota Power Monitoring → MQTT → InfluxDB 2.x

📡 Dieses Tool liest Energiedaten von Tasmota-Smartplugs über MQTT und schreibt sie in eine InfluxDB 2.x-Datenbank.

---

## 🚀 Features

- Unterstützung für **Tasmota**-Geräte mit Energiemessung
- Datenübertragung via **MQTT**
- Speicherung in **InfluxDB 2.x**
- Leichtgewichtiges Setup per Docker

---

## 🧾 Voraussetzungen

- Docker & Docker Compose
- MQTT-Broker (z. B. Mosquitto)
- InfluxDB 2.x (mit Token, Bucket und Organisation)

---

## ⚙️ Setup

### 🔧 1. Repository klonen

```bash
git clone https://github.com/pepelahmann/tasmota-power-monitoring-mqtt-to-influxdb.git
cd tasmota-power-monitoring-mqtt-to-influxdb
