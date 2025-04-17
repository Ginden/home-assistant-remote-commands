import inspect
from typing import ParamSpec

import paho.mqtt.client as mqtt


class HackyMqttClient(mqtt.Client):
    """MQTT client that ignores connect/loop calls from Subscriber/Discoverable"""

    def __init__(self, *args, **kwargs) -> None:  # type: ignore[no-untyped-def]
        super().__init__(*args, **kwargs)
        self._is_connected = False

    def connect(self, *args, **kwargs) -> int:  # type: ignore[no-untyped-def,override]
        # Check if call originates from Subscriber
        frame = inspect.currentframe()
        if frame is None:
            return mqtt.MQTT_ERR_SUCCESS

        frame = frame.f_back
        if frame is not None and frame.f_code is not None:
            function_name = frame.f_code.co_name
            if '_connect_client' in function_name:
                print(f"Skipping connect call from {function_name}")
                return mqtt.MQTT_ERR_SUCCESS
        self._is_connected = True
        print(f"Connecting to MQTT broker at {args[0]}:{args[1]}")
        return super().connect(*args, **kwargs)

    def loop_start(self) -> int | None:  # type: ignore[override]
        # Check if call originates from Subscriber
        frame = inspect.currentframe()
        if frame is None:
            return None

        frame = frame.f_back
        if frame is not None and frame.f_code is not None:
            function_name = frame.f_code.co_name
            if '_connect_client' in function_name:
                print(f"Skipping connect call from {function_name}")
                return None

        return super().loop_start()
