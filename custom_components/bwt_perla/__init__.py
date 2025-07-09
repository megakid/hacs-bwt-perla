"""The BWT Perla integration."""

import logging

from bwt_api.api import BwtApi, BwtSilkApi
from bwt_api.exception import BwtException

from .api.registers import BwtRegistersApi

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform, CONF_CODE, CONF_HOST
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.entity_registry import async_migrate_entries

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up BWT Perla from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    try:
        if CONF_CODE in entry.data:
            api = BwtApi(entry.data["host"], entry.data["code"])
            await api.get_current_data()
        else:
            # Try to determine if it's the new registers API
            from .detector import determine_bwt_model
            model = await determine_bwt_model(entry.data["host"])
            
            if model == "perla_silk_registers":
                api = BwtRegistersApi(entry.data["host"])
                await api.get_registers()
            else:
                api = BwtSilkApi(entry.data["host"])
                await api.get_registers()
    except BwtException as e:
        _LOGGER.exception("Error setting up Bwt API")
        await api.close()
        raise ConfigEntryNotReady from e
    except Exception as e:
        _LOGGER.exception("Error setting up API")
        if 'api' in locals():
            await api.close()
        raise ConfigEntryNotReady from e

    hass.data[DOMAIN][entry.entry_id] = api

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        api = hass.data[DOMAIN].pop(entry.entry_id)
        await api.close()

    return unload_ok


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s", entry.version)

    # Add entry id to unique id in order to allow multiple devices
    if entry.version == 1:

        @callback
        def update_unique_id(entity_entry):
            """Update unique ID of entity entry."""
            return {"new_unique_id": entry.entry_id + "_" + entity_entry.unique_id}

        await async_migrate_entries(hass, entry.entry_id, update_unique_id)
        entry.version = 2

    _LOGGER.info("Migration to version %s successful", entry.version)

    return True
