import appdaemon.plugins.hass.hassapi as hass
import struct
import asyncio
from datetime import timedelta

class ModbusReader(hass.Hass):
    def initialize(self):
        """Initialize the Modbus reader, listen for changes, and schedule periodic updates."""
        self.log("ModbusReader AppDaemon started!")

        # Listen for changes in max_charger_current
        self.listen_state(self.update_max_charger_current, "sensor.max_charger_current")

        # Run every 5 minutes
        self.run_every(self.periodic_update, self.datetime() + timedelta(seconds=300), 300)

    def update_max_charger_current(self, entity, attribute, old, new, kwargs):
        """Triggered when sensor.max_charger_current changes in Home Assistant."""
        self.process_new_value(new)

    def periodic_update(self, kwargs):
        """Runs every 5 minutes regardless of sensor changes."""
        self.log("Running periodic update: Writing last known value to Modbus.")
        current_value = self.get_state("sensor.max_charger_current")
        self.process_new_value(current_value)

    def process_new_value(self, value):
        """Writes max charger current to Modbus."""
        try:
            if value in [None, "unavailable", "unknown"]:
                self.log("Warning: sensor.max_charger_current is unavailable. Using 0 A.", level="WARNING")
                value = 0.0
            else:
                value = float(value)

            self.log(f"Writing max charger current: {value} A to Modbus.")

            # Write the value to Modbus
            self.write_max_current_to_modbus(value)

        except Exception as e:
            self.log(f"Error processing max charger current: {e}", level="ERROR")

    async def async_write_modbus(self, value):
        """Asynchronously write max available charger current to Modbus register 1210."""
        try:
            # Convert float32 to MSB/LSB
            network_long = struct.unpack('>I', struct.pack('>f', value))[0]
            msb = (network_long >> 16) & 0xFFFF
            lsb = network_long & 0xFFFF

            self.log(f"Writing {value} A (MSB: {msb}, LSB: {lsb}) to Modbus register 1210.")

            # Send values to Modbus
            await self.call_service(
                "modbus/write_register",
                hub="laadpaal",  # Must match configuration.yaml
                unit=1,          # Slave ID
                address=1210,    # The Modbus register for max current
                value=[msb, lsb]
            )

            self.log(f"Successfully sent {value} A to Modbus register 1210.")

        except Exception as e:
            self.log(f"Error writing max current to Modbus: {e}", level="ERROR")

    def write_max_current_to_modbus(self, value):
        """Schedule Modbus write operation asynchronously."""
        self.create_task(self.async_write_modbus(value))
