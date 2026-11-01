from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.const import STATE_OFF
from .constants import DOMAIN, _LOGGER
from .entity import HarviaEntity

class HarviaDoorSensor(HarviaEntity, BinarySensorEntity):
    """Whether the sauna door is open."""

    def __init__(self, device, sauna):
        super().__init__(device, sauna, 'door_sensor', 'Door')
        self._state = STATE_OFF
        self._attr_icon = 'mdi:door'

    @property
    def device_class(self):
        return  BinarySensorDeviceClass.DOOR

    @property
    def is_on(self):
        """Return True when the door is open."""
        if self._state == STATE_OFF:
            return False
        else:
            return True

    async def async_added_to_hass(self):
        """Register with the device and publish the current state."""
        await super().async_added_to_hass()
        self._device.doorSensor = self
        await self._device.update_ha_devices()

    async def update_state(self):
        self.async_write_ha_state()

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Harvia binary sensors."""
    devices = await hass.data[DOMAIN]['api'].get_devices()
    all_binary_sensors = []

    for device in devices:
        _LOGGER.debug(f"Loading binary sensors for device: {device.name}")
        device_binary_sensors = await device.get_binary_sensors()
        all_binary_sensors.extend(device_binary_sensors)

    async_add_entities(all_binary_sensors, True)
