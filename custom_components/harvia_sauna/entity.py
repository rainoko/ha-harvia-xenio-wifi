from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .constants import DOMAIN


class HarviaEntity(Entity):
    """Common base for all Harvia entities: push updates, one HA device per sauna."""

    _attr_should_poll = False
    _attr_has_entity_name = True

    def __init__(self, device, sauna, unique_id_suffix: str, name: str):
        self._device = device
        self._sauna = sauna
        self.added = False  # True while the entity is registered in HA (not disabled/removed)
        # Unique IDs must stay identical to earlier versions to keep entity history.
        self._attr_unique_id = f"{device.id}_{unique_id_suffix}"
        self._attr_name = name
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device.id)},
            name=device.name,
            manufacturer="Harvia",
        )

    @property
    def available(self) -> bool:
        return self._sauna.available

    async def async_added_to_hass(self):
        self.added = True
        self.async_on_remove(
            async_dispatcher_connect(self.hass, self._sauna.signal_availability, self.async_write_ha_state)
        )

    async def async_will_remove_from_hass(self):
        self.added = False
