# Wiener Netze Smartmeter Integration for Home Assistant

[![codecov](https://codecov.io/gh/DarwinsBuddy/WienerNetzeSmartmeter/branch/main/graph/badge.svg?token=ACYNOG1WFW)](https://codecov.io/gh/DarwinsBuddy/WienerNetzeSmartmeter)
![Tests](https://github.com/DarwinsBuddy/WienerNetzeSmartMeter/actions/workflows/test.yml/badge.svg)

![Hassfest](https://github.com/DarwinsBuddy/WienerNetzeSmartMeter/actions/workflows/hassfest.yml/badge.svg)
![Validate](https://github.com/DarwinsBuddy/WienerNetzeSmartMeter/actions/workflows/validate.yml/badge.svg)
![Release](https://github.com/DarwinsBuddy/WienerNetzeSmartMeter/actions/workflows/release.yml/badge.svg)

## About 

This repo contains a custom component for [Home Assistant](https://www.home-assistant.io) for exposing a sensor
providing information about a registered [WienerNetze Smartmeter](https://www.wienernetze.at/smartmeter).

## FAQs
[FAQs](https://github.com/DarwinsBuddy/WienerNetzeSmartmeter/discussions/19)

## About This Fork

This fork builds on [DarwinsBuddy/WienerNetzeSmartmeter](https://github.com/DarwinsBuddy/WienerNetzeSmartmeter) and includes fixes/features that were not (yet) merged upstream at the time of forking:

- **Official OAuth2 API support** alongside the legacy username/password scraper, as an alternative authentication method (`official_client.py`, `adapter.py`, `client_factory.py`). Originally contributed by [KrOnAsK](https://github.com/KrOnAsK) / Jonas Kruse.
- **Fallback to daily granularity** when the quarter-hour (`V002`) feed comes back empty for a Zaehlpunkt that's otherwise opted into 15-min values. Ported from [Sgoettschkes/WienerNetzeSmartmeter@fallback-daily-when-quarter-hour-empty](https://github.com/Sgoettschkes/WienerNetzeSmartmeter/tree/fallback-daily-when-quarter-hour-empty).
- **Defensive handling of malformed `bewegungsdaten` responses.** The legacy scraper's `bewegungsdaten()` call used to crash with an unhandled `KeyError` whenever WienerNetze returned a response without a `descriptor` field (e.g. an error payload). This is now caught and logged with the raw response, instead of aborting the whole statistics import silently.
- **Added the (as of September 2026) required `wandler` query parameter** to the `bewegungsdaten` request. WienerNetze started rejecting requests missing this parameter with `400 Bad Request: Required parameter 'wandler' is not present`. The official web portal sends `wandler=false` for standard (non-transformer-metered) Zaehlpunkte, which is what this fork now sends too.
- **Parallel cost statistic.** The importer now also writes a `<statistic_id>_cost` external statistic (in EUR) alongside the energy statistic, computed from the same per-hour usage values so cost and energy stay in sync. The price per kWh is configurable per entry via the integration's **Options** (Settings → Devices & Services → Wiener Netze Smartmeter → Configure); it defaults to `PRICE_PER_KWH` in `custom_components/wnsm/const.py` for entries that haven't set one. To use it, add the `<statistic_id>_cost` statistic as `stat_cost` for your grid source in Home Assistant's Energy Dashboard settings (fixed/entity pricing is not supported there for external-statistics sources).

### Getting an official API key

The OAuth2 method needs a `client_id`, `client_secret`, and `api_key`. These are issued by registering an application at the [Wiener Stadtwerke API Portal](https://api-portal.wienerstadtwerke.at) — specifically the [Smart Meter API product](https://api-portal.wienerstadtwerke.at/portal/apis/7f8a1cce-2a7e-4b18-840b-b0387ed9a3fc/apiinfo). Application approval is a manual review on Wiener Stadtwerke's side and can take a few days; there is no published SLA. Until it's approved, the legacy scraper method works without it.

## Installation

### Manual

Copy `<project-dir>/custom_components/wnsm` into `<home-assistant-root>/config/custom_components`

### HACS
1. Search for `Wiener Netze Smart Meter` or `wnsm` in HACS
2. Install
3. ...
4. Profit!

## Configure

You can choose between ui configuration or manual (by adding your credentials to `configuration.yaml` and `secrets.yaml` resp.)
After successful configuration you can add sensors to your favourite dashboard, or even to your energy dashboard to track your total consumption.

### UI
<img src="./doc/wnsm1.png" alt="Settings" width="500"/>
<img src="./doc/wnsm2.png" alt="Integrations" width="500"/>
<img src="./doc/wnsm3.png" alt="Add Integration" width="500"/>
<img src="./doc/wnsm4.png" alt="Search for WienerNetze" width="500"/>
<img src="./doc/wnsm5.png" alt="Authenticate with your credentials" width="500"/>
<img src="./doc/wnsm6.png" alt="Observe that all your smartmeters got imported" width="500"/>

### Manual
See [Example configuration files](https://github.com/DarwinsBuddy/WienerNetzeSmartmeter/blob/main/example/configuration.yaml)
## Copyright

This integration uses the API of https://www.wienernetze.at/smartmeter
All rights regarding the API are reserved by [Wiener Netze](https://www.wienernetze.at/impressum)

Special thanks to [platrysma](https://github.com/platysma)
for providing me a starting point [vienna-smartmeter](https://github.com/platysma/vienna-smartmeter)
and especially [florianL21](https://github.com/florianL21/)
for his [fork](https://github.com/florianL21/vienna-smartmeter/network)

