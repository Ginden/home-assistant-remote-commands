import inspect

import paho.mqtt.client as mqtt

class HackyMqttClient(mqtt.Client):
    """MQTT client that ignores connect/loop calls from Subscriber/Discoverable"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._is_connected = False

    def connect(self, *args, **kwargs):
        # Check if call originates from Subscriber
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        if '_connect_client' in caller_frame.f_code.co_name:
            print(f"Skipping connect call from {caller_frame.f_code.co_name}")
            return mqtt.MQTT_ERR_SUCCESS
        self._is_connected = True
        print(f"Connecting to MQTT broker at {args[0]}:{args[1]}")
        return super().connect(*args, **kwargs)

    def loop_start(self):
        # Check if call originates from Subscriber
        frame = inspect.currentframe()
        caller_frame = frame.f_back
        if '_connect_client' in caller_frame.f_code.co_name:
            print(f"Skipping loop_start call from {caller_frame.f_code.co_name}")
            return None
        return super().loop_start()

    def is_connected(self):
        return self._is_connected
