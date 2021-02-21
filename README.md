# linak_desk

It's a Home Assistant custom component to control and receive a status of the Linak desk with a Bluetooth DPG controller.

Supported features:
- read the current desk height

## Installation

Move files to `HA_CONFIG/custom_components/linak_desk` or just clone the repository in `HA_CONFIG/custom_components`.

## Example Home Assistant configuration

```yaml
sensor:
  - platform: linak_desk
    mac: AA:BB:CC:DD:EE
    min_height_m: 0.635
    max_height_m: 1.28
    scan_interval:
      seconds: 30
```