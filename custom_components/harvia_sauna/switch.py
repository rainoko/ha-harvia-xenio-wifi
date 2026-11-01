from homeassistant.components.switch import SwitchEntity
from .constants import DOMAIN, STORAGE_KEY, STORAGE_VERSION, REGION,_LOGGER
from .entity import HarviaEntity
from homeassistant.components.climate.const import HVACMode

class HarviaPowerSwitch(HarviaEntity, SwitchEntity):
    def __init__(self, device, sauna):
        super().__init__(device, sauna, 'power', 'Power switch')
        self._is_on = device.active
        self._attr_icon = 'mdi:heater'

    @property
    def is_on(self):
        return self._is_on

    async def async_added_to_hass(self):
        """Acties die uitgevoerd moeten worden als entiteit aan HA is toegevoegd."""
        await super().async_added_to_hass()
        self._device.powerSwitch = self
        await self._device.update_ha_devices()

    async def update_state(self):
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        # Code om de sauna aan te zetten
        await self._device.set_active(True)
        self._is_on = True
        self.async_write_ha_state()
        if self._device.thermostat is not None:
            self._device.thermostat._attr_hvac_mode = HVACMode.HEAT
            await self._device.thermostat.update_state()

    async def async_turn_off(self, **kwargs):
        # Code om de sauna uit te zetten
        await self._device.set_active(False)
        self._is_on = False
        self.async_write_ha_state()
        if self._device.thermostat is not None:
            self._device.thermostat._attr_hvac_mode = HVACMode.OFF
            await self._device.thermostat.update_state()

class HarviaLightSwitch(HarviaEntity, SwitchEntity):
    def __init__(self, device, sauna):
        super().__init__(device, sauna, 'light', 'Light Switch')
        self._is_on = device.lightsOn
        self._attr_icon = 'mdi:lightbulb-multiple'


    async def async_added_to_hass(self):
        """Acties die uitgevoerd moeten worden als entiteit aan HA is toegevoegd."""
        await super().async_added_to_hass()
        self._device.lightSwitch = self
        await self._device.update_ha_devices()

    async def update_state(self):
        self.async_write_ha_state()

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        # Code om de sauna aan te zetten
        await self._device.set_lights(True)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        # Code om de sauna uit te zetten
        await self._device.set_lights(False)
        self._is_on = False
        self.async_write_ha_state()

class HarviaSteamerSwitch(HarviaEntity, SwitchEntity):
    def __init__(self, device, sauna):
        super().__init__(device, sauna, 'steamer', 'Steamer Switch')
        self._is_on = device.steamOn
        self._attr_icon = 'mdi:wave'


    async def async_added_to_hass(self):
        """Acties die uitgevoerd moeten worden als entiteit aan HA is toegevoegd."""
        await super().async_added_to_hass()
        self._device.steamerSwitch = self
        await self._device.update_ha_devices()

    async def update_state(self):
        self.async_write_ha_state()

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        # Code om de sauna aan te zetten
        await self._device.set_steamer(True)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        # Code om de sauna uit te zetten
        await self._device.set_steamer(False)
        self._is_on = False
        self.async_write_ha_state()

class HarviaFanSwitch(HarviaEntity, SwitchEntity):
    def __init__(self, device, sauna):
        super().__init__(device, sauna, 'fan', 'Fan Switch')
        self._is_on = device.fanOn
        self._attr_icon = 'mdi:fan'


    async def async_added_to_hass(self):
        """Acties die uitgevoerd moeten worden als entiteit aan HA is toegevoegd."""
        await super().async_added_to_hass()
        self._device.fanSwitch = self
        await self._device.update_ha_devices()

    async def update_state(self):
        self.async_write_ha_state()

    @property
    def is_on(self):
        return self._is_on

    async def async_turn_on(self, **kwargs):
        # Code om de sauna aan te zetten
        await self._device.set_fan(True)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        # Code om de sauna uit te zetten
        await self._device.set_fan(False)
        self._is_on = False
        self.async_write_ha_state()

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up de Harvia switches."""
    # Hier zou je de logica toevoegen om je apparaten op te halen.
    # Voor nu voegen we handmatig een schakelaar toe als voorbeeld.
    devices = await hass.data[DOMAIN]['api'].get_devices()
    switches = []

    for device in devices:
        _LOGGER.debug(f"Loading switches for device: {device.name}")
        device_switches = await device.get_switches()
        for device_switch in device_switches:
            switches.append(device_switch)

    async_add_entities(switches, True)
