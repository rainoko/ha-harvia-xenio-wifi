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
        """Register with the device and publish the current state."""
        await super().async_added_to_hass()
        self._device.thermostat = self
        await self._device.update_ha_devices()

    async def async_set_temperature(self, **kwargs):
        """Set the target temperature."""
        if (temperature := kwargs.get(ATTR_TEMPERATURE)) is not None:
            self._attr_target_temperature = temperature
            await self._device.set_target_temperature(int(temperature))
            self.async_write_ha_state()

    async def async_set_hvac_mode(self, hvac_mode):
        """Set the HVAC mode (heat turns the sauna on, off turns it off)."""
        active = hvac_mode == HVACMode.HEAT
        await self._device.set_active(active)
        self._attr_hvac_mode = hvac_mode
        self.async_write_ha_state()

        if self._device.powerSwitch is not None and self._device.powerSwitch.added:
            self._device.powerSwitch._is_on = active
            await self._device.powerSwitch.update_state()

    async def async_turn_on(self):
        await self.async_set_hvac_mode(HVACMode.HEAT)

    async def async_turn_off(self):
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def update_state(self):
        self.async_write_ha_state()

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the Harvia thermostats."""
    devices = await hass.data[DOMAIN]['api'].get_devices()
    thermostats = []

    for device in devices:
        _LOGGER.debug(f"Loading thermostats for device: {device.name}")
        device_thermostats = await device.get_thermostats()
        for device_thermostat in device_thermostats:
            thermostats.append(device_thermostat)

    async_add_entities(thermostats, True)
