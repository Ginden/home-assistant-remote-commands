import paho.mqtt.client as mqtt


class MqttCallbackRouter:
    """Routes MQTT messages to appropriate callbacks based on topics

    Is this insane? Yes. Is it necessary? Also yes.

    https://github.com/unixorn/ha-mqtt-discoverable/issues/194
    https://github.com/unixorn/ha-mqtt-discoverable/issues/331

    """

    def __init__(self):
        self._message_callbacks = {}
        self._subscriptions = []

    def add_callback(self, topic: str, callback, user_data=None):
        print(f"Adding callback for topic {topic}")
        self._message_callbacks[topic] = (callback, user_data)
        # Store subscription info for when we connect
        self._subscriptions.append((topic, callback, user_data))

    def __call__(self, client, userdata, message):
        print(f"Received message on topic {message.topic}: {message.payload.decode()}")
        if message.topic in self._message_callbacks:
            callback, user_data = self._message_callbacks[message.topic]
            old_userdata = client.user_data_set(user_data)
            try:
                callback(client, user_data, message)
            finally:
                client.user_data_set(old_userdata)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        """Handle connection by subscribing to all topics"""
        for topic, callback, user_data in self._subscriptions:
            result, _ = client.subscribe(topic, qos=1)
            if result != mqtt.MQTT_ERR_SUCCESS:
                raise RuntimeError(f"Error subscribing to MQTT topic {topic}")
