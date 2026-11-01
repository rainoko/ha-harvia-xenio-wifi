from homeassistant.components.number import NumberEntity
from homeassistant.const import PERCENTAGE
from .constants import DOMAIN, _LOGGER
from .entity import HarviaEntity

class HarviaHumiditySetPoint(HarviaEntity, NumberEntity):
    """Target relative humidity for the steamer."""

    def __init__(self, device, sauna):
        super().__init__(device, sauna, 'humidity_set_point', 'Steamer Humidity')
        self._state = None
        self._attr_icon = 'mdi:cloud-percent'
        self._attr_native_min_value = 0
        self._attr_native_max_value = 100
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self):
        """Return the current target humidity."""
        return self._state

    async def async_added_to_hass(self):
        """Register with the device and publish the current state."""
        await super().async_added_to_hass()
        self._device.humidityNumber = self
        await self._device.update_ha_devices()

    async def update_state(self):
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float):
        """Send a new target humidity to the sauna."""
        self._state = int(value)
        await self._device.set_target_relative_humidity(int(value))
        self.async_write_ha_state()

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Harvia number entities."""
    devices = await hass.data[DOMAIN]['api'].get_devices()
    all_numbers = []

    for device in devices:
        _LOGGER.debug(f"Loading sensors for device: {device.name}")
        device_numbers = await device.get_numbers()
        all_numbers.extend(device_numbers)

    async_add_entities(all_numbers, True)
