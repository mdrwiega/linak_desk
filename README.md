# linak_desk

It's a Home Assistant custom component to control and receive a status of the Linak desk with a Bluetooth DPG controller.

Supported features:
- read a current desk height

Example Home Assistant configuration:
```yaml
sensor:
  - platform: linak_desk
    mac: AA:BB:CC:DD:EE
    min_height_m: 0.635
    max_height_m: 1.28
```