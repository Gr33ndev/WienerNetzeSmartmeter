"""Set up the Wiener Netze SmartMeter Integration component."""
from homeassistant import core, config_entries
from homeassistant.core import DOMAIN


async def async_setup_entry(
        hass: core.HomeAssistant,
        entry: config_entries.ConfigEntry
) -> bool:
    """Set up platform from a ConfigEntry."""
    hass.data.setdefault(DOMAIN, {})
    # Options (e.g. the cost-statistic price, set via the Options flow) live
    # separately from the original entry data and are merged in here so the
    # sensor platform can read everything from one dict.
    hass.data[DOMAIN][entry.entry_id] = {**entry.data, **entry.options}

    # Reloading the entry re-runs this function, which picks up any options
    # changes made via the Options flow.
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    # Forward the setup to the sensor platform.
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    return True


async def async_reload_entry(
        hass: core.HomeAssistant,
        entry: config_entries.ConfigEntry
) -> None:
    """Reload the entry when its options change."""
    await hass.config_entries.async_reload(entry.entry_id)
