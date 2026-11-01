from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE
from .constants import DOMAIN, STORAGE_KEY, STORAGE_VERSION, REGION,_LOGGER
from .entity import HarviaEntity

class HarviaHumiditySensor(HarviaEntity, SensorEntity):
    """Representatie van een vochtigheidssensor."""

    def __init__(self, device, sauna):
        """Initialiseer de humidity sensor."""
        super().__init__(device, sauna, 'humidity_sensor', 'Humidity')
        self._state = None
        self._attr_icon = 'mdi:water-percent'

    @property
    def state(self):
        """Return de staat van de sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return de eenheid die wordt gebruikt."""
        return PERCENTAGE

    async def async_added_to_hass(self):
        """Acties die uitgevoerd moeten worden als entiteit aan HA is toegevoegd."""
        await super().async_added_to_hass()
        self._device.humiditySensor = self
        await self._device.update_ha_devices()

    async def update_state(self):
        self.async_write_ha_state()

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up de Harvia sensors."""
    devices = await hass.data[DOMAIN]['api'].get_devices()
    all_sensors = []  # Gebruik een andere variabele om verwarring te voorkomen

    for device in devices:
        _LOGGER.debug(f"Loading sensors for device: {device.name}")
        device_sensors = await device.get_sensors()  # Verkrijg  sensors voor het huidige apparaat
        all_sensors.extend(device_sensors)  # Voeg de verkregen sensors toe aan de lijst

    async_add_entities(all_sensors, True)
