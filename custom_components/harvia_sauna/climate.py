from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import HVACMode, ClimateEntityFeature
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from .constants import DOMAIN, _LOGGER
from .entity import HarviaEntity

class HarviaThermostat(HarviaEntity, ClimateEntity):
    _attr_min_temp = 40
    _attr_max_temp = 110
    _attr_target_temperature_step = 1
    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT]
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )

    def __init__(self, device, sauna):
        super().__init__(device, sauna, 'termostat', 'Thermostat')
        self._attr_current_temperature = None
        self._attr_target_temperature = None
        self._attr_hvac_mode = HVACMode.OFF

    async def async_added_to_hass(self):
        """Acties die uitgevoerd moeten worden als entiteit aan HA is toegevoegd."""
        await super().async_added_to_hass()
        self._device.thermostat = self
        await self._device.update_ha_devices()

    async def async_set_temperature(self, **kwargs):
        """Stel de doeltemperatuur in."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is not None:
            self._attr_target_temperature = temperature
            await self._device.set_target_temperature(int(temperature))
            self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        """Stel de HVAC-modus in."""
        active = hvac_mode == HVACMode.HEAT
        self._attr_hvac_mode = hvac_mode
        self.async_write_ha_state()

        await self._device.set_active(active)

        if self._device.powerSwitch is not None:
            self._device.powerSwitch._is_on = active
            await self._device.powerSwitch.update_state()

    async def async_turn_on(self):
        await self.async_set_hvac_mode(HVACMode.HEAT)

    async def async_turn_off(self):
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def update_state(self):
        self.async_write_ha_state()

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up de Harvia theromostats."""
    devices = await hass.data[DOMAIN]['api'].get_devices()
    theromostats = []

    for device in devices:
        _LOGGER.debug(f"Loading theromostats for device: {device.name}")
        device_theromostats = await device.get_thermostats()
        for device_theromostat in device_theromostats:
            theromostats.append(device_theromostat)

    async_add_entities(theromostats, True)
