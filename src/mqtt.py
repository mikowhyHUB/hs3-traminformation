import time
from paho.mqtt import client as mqtt_client


class Mqtt:
    def __init__(self, broker: str, port: int, username: str, password: str, topic: str, client_id: str) -> None:
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.topic = topic
        self.client_id = client_id

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):  # zaa wyjątkiem rc argumenty chyba niepotrzebne?
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self, client, payload) -> mqtt_client:
        result = client.publish(self.topic, payload)
        status = result[0]
        if status == 0:
            print(f"Send `{payload}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")

    def run(self, tram) -> mqtt_client:
        client = self.connect_mqtt()
        client.loop_start()
        while True:
            payload = tram.json_file()
            self.publish(client, payload)
            time.sleep(20)
