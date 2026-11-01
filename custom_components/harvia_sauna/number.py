from homeassistant.components.number import NumberEntity
from homeassistant.const import PERCENTAGE
from .constants import DOMAIN, STORAGE_KEY, STORAGE_VERSION, REGION,_LOGGER
from .entity import HarviaEntity

class HarviaHumiditySetPoint(HarviaEntity, NumberEntity):
    """Representatie van een nummer entiteit om de gewenste vochtigheid in te stellen."""

    def __init__(self, device, sauna):
        """Initialiseer de humidity number set point."""
        super().__init__(device, sauna, 'humidity_set_point', 'Steamer Humidity')
        self._state = None
        self._attr_icon = 'mdi:cloud-percent'
        self._attr_native_min_value = 0
        self._attr_native_max_value = 100
        self._attr_native_step = 1
        self._attr_native_unit_of_measurement = PERCENTAGE

    @property
    def native_value(self):
        """Return de huidige ingestelde waarde."""
        return self._state

    async def async_added_to_hass(self):
        """Acties die uitgevoerd moeten worden als entiteit aan HA is toegevoegd."""
        await super().async_added_to_hass()
        self._device.humidityNumber = self
        await self._device.update_ha_devices()

    async def update_state(self):
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float):
        """Update de ingestelde waarde."""
        self._state = int(value)
        await self._device.set_target_relative_humidity(int(value))
        self.async_write_ha_state()

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up de Harvia numbers."""
    devices = await hass.data[DOMAIN]['api'].get_devices()
    all_numbers = []  # Gebruik een andere variabele om verwarring te voorkomen

    for device in devices:
        _LOGGER.debug(f"Loading sensors for device: {device.name}")
        device_numbers = await device.get_numbers()  # Verkrijg  sensors voor het huidige apparaat
        all_numbers.extend(device_numbers)  # Voeg de verkregen sensors toe aan de lijst

    async_add_entities(all_numbers, True)
