# Custom HA integration for the BWT Perla

_BWT Perla integration repository for [HACS](https://github.com/custom-components/hacs)._
<!--
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=dkarv&repository=ha-bwt-perla)
-->
### Requirements

* Firmware with at least version 2.02xx [(more info)](#how-can-i-get-the-firmware-update)
* Local API enabled in Settings > General > Connection
* "Login-Code" sent to you by mail during registration [(more info)](#where-do-i-get-the-login-code)
* local network connection (you need the ip address during setup)

**Note:** This integration now also supports BWT water softeners with the new registers API (`/silk/registers` endpoint) which provides additional water usage and salt monitoring capabilities without requiring a login code.

### Installation

* Install BWT Perla in HACS
* Setup integration and enter host / ip address and the "Login-Code"
* Optional: set entity _bwt total output_ as water source in the energy dashboard

### Entities

| Entity Id(s) | Information |
| ------------- | ------------- |
| total_output | Increasing value of the blended water = the total water consumed. Use this as water source on the energy dashboard. |
| errors, warnings | The fatal errors and non-fatal warnings. Comma separated list or empty if no value present. [List of values](https://github.com/dkarv/bwt_api/blob/main/src/bwt_api/error.py). |
| state | State of the device. Can be OK, WARNING, ERROR |
| holiday_mode | If the holiday mode is active (true) or not (false) |
| holiday_mode_start | Undefined or a timestamp if the holiday mode is set to start in the future |
| hardness_in, hardness_out | dH value of the incoming and outgoing water. Note that this value is not measured, but configured on the device during setup |
| customer_service, technician_service | Timestamp of the last service performed by the customer or technician. The timezone of BWT device and HA server must be the same for this to be correct |
| regenerativ_level | Percentage of salt left |
| regenerativ_days | Estimated days of salt left |
| regenerativ_mass | Total grams of salt used since initial device setup |
| last_regeneration_1, last_regeneration_2 | Last regeneration of column 1 or 2. The timezone of BWT device and HA server must be the same for this to be correct |
| counter_regeneration_1, counter_regeneration_2 | Total count of regenerations since initial device setup |
| capacity_1, capacity_2 | Capacity the columns have left of water with hardness_out |
| day_output, month_output, year_output | The output of the current day, month and year. **These values are sometimes too low, probably when a lot of water is used in a short time. The total_output is more reliable to measure the water consumption.** https://github.com/dkarv/ha-bwt-perla/issues/14 |
| current_flow | The current flow rate. Please note that this value is not too reliable. Especially short flows might be completely missing, because this value is only queried every 30 seconds in the beginning. Only once a water flow is detected, it is queried more often. Once the flow is zero, the refresh rate cools down to 30 seconds. |

#### Additional Entities for New Registers API

If your BWT water softener supports the new registers API (`/silk/registers` endpoint), you'll also get these additional entities:

| Entity Id | Information |
| ------------- | ------------- |
| daily_average_water_use | Average daily water consumption in liters |
| capacity_percentage | Current capacity percentage remaining |
| max_salt_capacity | Maximum salt capacity in kilograms |
| current_salt_level | Current salt level in kilograms |

This firmware automatically detects the availability of the new endpoint and presents the appropriate entities.


### FAQ

#### How can I get the firmware update?

The firmware 2.02xx is currently rolling out to all devices. If your device does not have it yet, it can be requested through the customer service by mail and will be remotely installed on your device.

It looks like the customer service does not do the update on devices in the UK - it is still unclear why and what other countries are affected.

For more details and recent news, check out the discussion in the [HomeAssistant forum](https://community.home-assistant.io/t/bwt-best-water-tech-nology-support/270745/9999).

#### Where do I get the Login-Code?

The Login-Code is sent to you by mail when registering the device for the first time. It is not related to the login credentials for the BWT app.

#### Why are the values from the integration different to the ones on the device?

The integration calculates the blended water volume for all entities. [More info on blended water](#what-is-blended-water).
It does so to make the values comparable - if there is a remaining capacity of 200l, you can use 200l in your house before the BWT needs to start regeneration.

Also the salt level on the device is only showing 10% steps, while this integration has exact percentages.

#### What is blended water?

There are three different volume values, related to how the BWT operates internally. The BWT device sometimes shows either of them, which can lead to confusion.

* _incoming water_: flowing into the device at e.g. 20dH.
* _fully desalinated water_: the BWT produces water with a hardness of 0dH
* _blended water_: By mixing _incoming water_ and _fully desalinated water_ at a given ratio, the requested hardness is produced.

A small example: Target of _blended water_ is 4dH, incoming 20dH. The BWT mixes now 20% of incoming water with 80% fully desalinated water: 0.2 * 20dH + 0.8 * 0dH = 4dH.
