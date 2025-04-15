import paho.mqtt.client as mqtt
import json
import logging
import os
import datetime
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

BASE_TOPIC = "tele/power_meter/"
TIMEZONE = "Z"
LOGLEVEL = os.getenv("LOGLEVEL", "INFO")

logging.basicConfig(level=LOGLEVEL.upper())


def tasmota_uptime_to_seconds(uptime_string):
    days, timestr = uptime_string.split("T", 1)
    t = time.strptime(timestr, "%H:%M:%S")
    return int(datetime.timedelta(days=int(days), hours=t.tm_hour, minutes=t.tm_min, seconds=t.tm_sec).total_seconds())


def parse_sensor_message_into_point(power_socket, topic, msg):
    data = json.loads(msg.payload)
    fields = None
    measurement = None

    if topic == "SENSOR":
        fields = data["ENERGY"]
        measurement = "sensor"
    elif topic == "STATE":
        fields = {"Uptime": tasmota_uptime_to_seconds(data["Uptime"])}
        measurement = "state"
    else:
        raise ValueError("Unexpected topic " + topic)

    point = (
        Point(measurement)
        .tag("power_socket", power_socket)
        .tag("topic", topic)
        .time(data["Time"] + TIMEZONE)
    )

    for key, value in fields.items():
        try:
            point.field(key, float(value))
        except ValueError:
            point.field(key, str(value))

    return point


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(BASE_TOPIC + "#")


def on_message(client, userdata, msg):
    subtopic = msg.topic.replace(BASE_TOPIC, "")
    power_socket, topic = subtopic.split("/", 1)

    if topic in ["SENSOR", "STATE"]:
        logging.info(f"New {topic} message from {power_socket}")
        point = parse_sensor_message_into_point(power_socket, topic, msg)
        userdata["write_api"].write(bucket=userdata["bucket"], org=userdata["org"], record=point)
    elif topic == "LWT":
        logging.info(f"Power socket {power_socket} reports: {msg.payload.decode('UTF-8')}")
    else:
        logging.warning(f"Unexpected topic {msg.topic}: {msg.payload}")


def main():
    influxdb_client = InfluxDBClient(
        url=os.getenv("INFLUXDB_URL"),
        token=os.getenv("INFLUXDB_TOKEN"),
        org=os.getenv("INFLUXDB_ORG")
    )

    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

    mqtt_client = mqtt.Client(userdata={
        "influxdb_client": influxdb_client,
        "write_api": write_api,
        "bucket": os.getenv("INFLUXDB_BUCKET"),
        "org": os.getenv("INFLUXDB_ORG")
    })

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    logger = logging.getLogger("mqttclient")
    mqtt_client.enable_logger(logger)

    mqtt_client.connect(os.getenv("MQTT_HOST"), int(os.getenv("MQTT_PORT", "1883")), 60)
    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
