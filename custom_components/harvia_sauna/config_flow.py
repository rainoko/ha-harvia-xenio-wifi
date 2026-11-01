from collections.abc import Mapping
from typing import Any

import botocore.exceptions
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from .api import HarviaSaunaAPI, HarviaApiError
from .constants import DOMAIN, _LOGGER


def unique_id_for(username: str) -> str:
    """Config entry unique ID: the Harvia account e-mail, case-insensitive."""
    return username.strip().lower()

class HarviaSaunaConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for your_component."""

    VERSION = 1  # De versie van je config flow

    async def _async_validate(self, username: str, password: str) -> dict:
        """Try to log in; return form errors (empty when the credentials work)."""
        api = HarviaSaunaAPI(username, password, self.hass)
        try:
            if not await api.authenticate():
                return {"base": "invalid_auth"}
        except (HarviaApiError, botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as err:
            _LOGGER.warning("Unable to connect to Harvia cloud: %s", err)
            return {"base": "cannot_connect"}
        except Exception:  # Show a form error instead of a broken flow
            _LOGGER.exception("Unexpected error while validating Harvia credentials")
            return {"base": "unknown"}
        return {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initiated by the user."""
        errors = {}

        # Controleer of we al een configuratie hebben
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        # Verwerk ingevulde gegevens
        if user_input is not None:
            await self.async_set_unique_id(unique_id_for(user_input[CONF_USERNAME]))
            self._abort_if_unique_id_configured()
            errors = await self._async_validate(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            if not errors:
                return self.async_create_entry(title="Harvia Sauna", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors,
        )

    async def async_step_reauth(self, entry_data: Mapping[str, Any]):
        """Started by HA when setup raises ConfigEntryAuthFailed."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(self, user_input=None):
        """Ask for a new password for the existing username."""
        errors = {}
        entry = self._get_reauth_entry()
        username = entry.data.get(CONF_USERNAME)

        if user_input is not None:
            errors = await self._async_validate(username, user_input[CONF_PASSWORD])
            if not errors:
                return self.async_update_reload_and_abort(
                    entry, data_updates={CONF_PASSWORD: user_input[CONF_PASSWORD]}
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({vol.Required(CONF_PASSWORD): str}),
            description_placeholders={"username": username},
            errors=errors,
        )

    async def async_step_reconfigure(self, user_input=None):
        """Change the username and password of the existing entry."""
        errors = {}
        entry = self._get_reconfigure_entry()

        if user_input is not None:
            errors = await self._async_validate(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
            if not errors:
                return self.async_update_reload_and_abort(
                    entry,
                    unique_id=unique_id_for(user_input[CONF_USERNAME]),
                    data_updates=user_input,
                )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME, default=entry.data.get(CONF_USERNAME)): str,
                vol.Required(CONF_PASSWORD): str,
            }),
            errors=errors,
        )
