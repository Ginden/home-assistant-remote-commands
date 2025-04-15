from platform import uname
from getpass import getuser
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    mqtt_host: str = Field('localhost', alias="MQTT_HOST")
    mqtt_port: int = Field(1883, alias="MQTT_PORT")
    mqtt_username: Optional[str] = Field(None, alias="MQTT_USERNAME")
    mqtt_password: Optional[str] = Field(None, alias="MQTT_PASSWORD")

    mqtt_tls_enabled: bool = Field(False, alias="MQTT_TLS_ENABLED")
    mqtt_tls_insecure: bool = Field(False, alias="MQTT_TLS_INSECURE")
    mqtt_ca_certs: Optional[str] = Field(None, alias="MQTT_CA_CERTS")

    host_id: str = Field(uname().node, alias="HOST_ID")
    user_id: str = Field(getuser(), alias="USER_ID")

    model_config = SettingsConfigDict(env_file=".env")
