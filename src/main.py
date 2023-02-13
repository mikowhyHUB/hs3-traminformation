from mqtt import Mqtt
from traminformation import TramFinder
import random
import os

broker = os.getenv('MQTT_BROKER', '127.0.0.1')
port = 1883
topic = "feed/public_transport"
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = ''
password = ''

STOP_IDS: list = [2031, 2030]
LINES_TO_SHOW: int = 5


def main():
    mqtt = Mqtt(broker, port, username, password, topic, client_id)
    tram = TramFinder(STOP_IDS, LINES_TO_SHOW)
    mqtt.run(tram)


if __name__ == '__main__':
    main()
