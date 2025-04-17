from collections.abc import Callable
from typing import Any

import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage, CallbackOnMessage, ConnectFlags
from paho.mqtt.reasoncodes import ReasonCode


class MqttCallbackRouter:
    """Routes MQTT messages to appropriate callbacks based on topics

    Is this insane? Yes. Is it necessary? Also yes.

    https://github.com/unixorn/ha-mqtt-discoverable/issues/194
    https://github.com/unixorn/ha-mqtt-discoverable/issues/331

    """

    _subscriptions: set[str]
    _message_callbacks: dict[str, tuple[CallbackOnMessage, Any]]

    def __init__(self) -> None:
        self._message_callbacks = {}
        self._subscriptions = set()

    def add_callback(self, topic: str, callback: CallbackOnMessage, user_data: Any = None) -> None:
        print(f"Adding callback for topic {topic}")
        self._message_callbacks[topic] = (callback, user_data)
        # Store subscription info for when we connect
        self._subscriptions.add(topic)

    def __call__(self, client: mqtt.Client, userdata: Any, message: MQTTMessage) -> None:
        print(f"Received message on topic {message.topic}: {message.payload.decode()}")
        if message.topic in self._message_callbacks:
            callback, user_data = self._message_callbacks[message.topic]
            client.user_data_set(user_data)
            callback(client, user_data, message)

    def on_connect(self, client: mqtt.Client, userdata: Any, flags: ConnectFlags, rc: ReasonCode) -> None:
        """Handle connection by subscribing to all topics"""
        print(f"Connected with result code {rc}")
        for topic in self._subscriptions:
            result, _ = client.subscribe(topic, qos=1)
            if result != mqtt.MQTT_ERR_SUCCESS:
                raise RuntimeError(f"Error subscribing to MQTT topic {topic}")
