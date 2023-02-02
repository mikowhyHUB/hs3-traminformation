from mqtt import Mqtt
import random
from traminformation import TramFinder

broker = '192.168.1.118'
port = 1883
topic = "feed/public_transport"
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = ''
password = ''

STOP_IDS = [2031, 2030]


def main():
    mqtt = Mqtt(broker, port, username, password, topic, client_id)
    tram = TramFinder(STOP_IDS)
    mqtt.run(tram)


if __name__ == '__main__':
    main()
