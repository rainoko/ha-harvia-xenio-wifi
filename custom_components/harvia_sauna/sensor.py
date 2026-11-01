from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
    UnitOfTemperature,
    UnitOfTime,
)
from .constants import DOMAIN, _LOGGER
from .entity import HarviaEntity


@dataclass(frozen=True, kw_only=True)
class HarviaSensorEntityDescription(SensorEntityDescription):
    """Sensor description; value_attr names the HarviaDevice attribute holding the value."""

    value_attr: str


# The key is used as unique ID suffix; 'humidity_sensor' must stay as-is for existing installs.
SENSORS = (
    HarviaSensorEntityDescription(
        key="humidity_sensor",
        name="Humidity",
        value_attr="humidity",
        icon="mdi:water-percent",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
    ),
    HarviaSensorEntityDescription(
        key="temperature_sensor",
        name="Temperature",
        value_attr="currentTemp",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
    ),
    HarviaSensorEntityDescription(
        key="remaining_time",
        name="Remaining time",
        value_attr="remainingTime",
        icon="mdi:timer-sand",
        device_class=SensorDeviceClass.DURATION,
        native_unit_of_measurement=UnitOfTime.MINUTES,
    ),
    HarviaSensorEntityDescription(
        key="wifi_rssi",
        name="WiFi signal",
        value_attr="wifiRssi",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
)


class HarviaSensor(HarviaEntity, SensorEntity):
    """A read-only value reported by the sauna."""

    entity_description: HarviaSensorEntityDescription

    def __init__(self, device, sauna, description: HarviaSensorEntityDescription):
        super().__init__(device, sauna, description.key, description.name)
        self.entity_description = description

    @property
    def native_value(self):
        return getattr(self._device, self.entity_description.value_attr)

    async def update_state(self):
        self.async_write_ha_state()

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Harvia sensors."""
    devices = await hass.data[DOMAIN]['api'].get_devices()
    all_sensors = []

    for device in devices:
        _LOGGER.debug(f"Loading sensors for device: {device.name}")
        device_sensors = await device.get_sensors()
        all_sensors.extend(device_sensors)

    async_add_entities(all_sensors, True)
