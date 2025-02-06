# HA-Alfen-load-balancing
Load balancing in HomeAssistant for Alfen charger

For 3 phases charger on 16A group in an installation of 3*25A

# Prerequisites 
- DSMR reader add on: https://github.com/sanderdw/hassio-addons/tree/master/dsmr_reader
- Mosquitto broker add on: https://github.com/home-assistant/addons/tree/master/mosquitto
- MQTT integration: https://www.home-assistant.io/integrations/mqtt/
- DSMR reader integration: https://www.home-assistant.io/integrations/dsmr_reader
- AppDaemon add on: https://github.com/hassio-addons/repository/tree/master/appdaemon


# Instructions
- make changes in configuration.yaml to reflect your situation
  - set ip of charger in line 17
  - please check your sensor names in mqtt - they should be copied in configuration.yaml lines 84, 85, 86
- set up appdaemon app
  - copy modbus_reader.py to appdaemon directory (typically addon_configs/something_appdaemon/apps
  - if you already have apps running, add the statements of apps.yaml to your apps.yaml
  - otherwise copy apps.yaml to the apps directory
  - make a long lived access token: https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token
  - if you already have code in appdaemon.yaml, add the lines
  - otherwise take the given appdaemon.yaml
  - add the token on line 11
- restart appdaemon
  - check log
