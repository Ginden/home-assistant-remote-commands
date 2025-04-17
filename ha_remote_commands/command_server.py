from typing import Any

from ha_remote_commands.app_config import AppConfig
from ha_mqtt_discoverable import Settings, DeviceInfo
from ha_mqtt_discoverable.sensors import Button, ButtonInfo
from paho.mqtt.client import Client, MQTTMessage

from ha_remote_commands.get_command_list import get_command_list, CommandDescription
from ha_remote_commands.mqtt_callback_router import MqttCallbackRouter
from ha_remote_commands.hacky_mqtt_client import HackyMqttClient
import logging


def get_mqtt_client(config: AppConfig) -> HackyMqttClient:
    """
    Convert the MQTTConfig to a Settings.MQTT object.
    """
    client_id = f"ha-remote-commands-{config.user_id}-{config.host_id}"
    client = HackyMqttClient(client_id=client_id)
    client.username_pw_set(config.mqtt_username, config.mqtt_password)

    if config.mqtt_tls_enabled:
        client.tls_set(ca_certs=config.mqtt_ca_certs)
        client.tls_insecure_set(config.mqtt_tls_insecure)

    return client


def construct_device_info(config: AppConfig) -> DeviceInfo:
    """
    Construct the device info for the MQTT discovery.
    """
    return DeviceInfo(
        identifiers=[f"{config.user_id}-{config.host_id}"],
        name=f"Remote Control {config.user_id} on {config.host_id}",
        manufacturer="HA Remote Commands",
        model="Command Server",
        sw_version="1.0.0",
    )


def button_callback(client: Client, cmd: CommandDescription, message: MQTTMessage) -> None:
    cmd.execute()


def start_command_server(command_dir: str, config: AppConfig) -> None:
    device_info = construct_device_info(config)
    command_list = get_command_list(command_dir)
    client = get_mqtt_client(config)

    router = MqttCallbackRouter()
    client.on_message = router
    mqtt_settings = Settings.MQTT(client=client)
    buttons: list[Button] = []

    for command in command_list:
        print(f"Creating button for command {command.name}")
        command_button_info = ButtonInfo(name=command.name, device=device_info, unique_id=command.unique_id)
        settings = Settings(mqtt=mqtt_settings, entity=command_button_info)
        button = Button(settings, router, command)
        router.add_callback(button._command_topic, button_callback, command)
        buttons.append(button)

    def on_connect(*args: Any, **kwargs: Any) -> None:
        print(f"Connected to MQTT broker")
        router.on_connect(*args, **kwargs)
        for button_to_publish in buttons:
            print(f"Writing config for {button_to_publish.state_topic}")
            button_to_publish.write_config()  # type: ignore[no-untyped-call]

    client.on_connect = on_connect
    client.on_message = router
    client.connect(config.mqtt_host, config.mqtt_port)
    client.loop_forever()
