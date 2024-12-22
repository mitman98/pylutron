# test.py
import logging
import os
import sys
import time
from pylutron import (
    Lutron,
    ThermostatMode,
    ThermostatFanMode
)

# Set up logging to see what's happening
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Your Lutron system details
LUTRON_HOST = "192.168.1.160"  # Your Lutron IP address
LUTRON_USER = "lutron"         # Default username
LUTRON_PASSWORD = "integration" # Default password
CACHE_FILE = "lutron_db.xml"   # Cache file name

def test_thermostat_controls(thermostat):
    """Test various thermostat control functions"""
    print(f"\nTesting controls for thermostat: {thermostat.name}")

    # Save original states to restore later
    original_mode = thermostat.mode
    original_fan = thermostat.fan_mode
    original_heat = thermostat.heat_setpoint
    original_cool = thermostat.cool_setpoint

    try:
        # Test heating mode
        print("\nTesting HEAT mode:")
        print("  Setting mode to HEAT...")
        thermostat.set_mode(ThermostatMode.HEAT)
        time.sleep(1)
        current_mode = thermostat.mode
        print(f"  Current mode: {current_mode.name}")

        # Test heat setpoint in heating mode
        test_heat = original_heat + 2 if original_heat is not None else 72
        print(f"  Setting heat setpoint to {test_heat}°F...")
        thermostat.set_setpoints(heat_setpoint=test_heat)
        time.sleep(1)
        current_heat = thermostat.heat_setpoint
        print(f"  Current heat setpoint: {current_heat}°F")

        # Test cooling mode
        print("\nTesting COOL mode:")
        print("  Setting mode to COOL...")
        thermostat.set_mode(ThermostatMode.COOL)
        time.sleep(1)
        current_mode = thermostat.mode
        print(f"  Current mode: {current_mode.name}")

        # Test cool setpoint in cooling mode
        test_cool = original_cool - 2 if original_cool is not None else 76
        print(f"  Setting cool setpoint to {test_cool}°F...")
        thermostat.set_setpoints(cool_setpoint=test_cool)
        time.sleep(1)
        current_cool = thermostat.cool_setpoint
        print(f"  Current cool setpoint: {current_cool}°F")

        # Test auto mode with both setpoints
        print("\nTesting AUTO mode:")
        print("  Setting mode to AUTO...")
        thermostat.set_mode(ThermostatMode.AUTO)
        time.sleep(1)
        current_mode = thermostat.mode
        print(f"  Current mode: {current_mode.name}")

        # Test both setpoints in auto mode
        test_heat = 70
        test_cool = 76
        print(f"  Setting heat setpoint to {test_heat}°F and cool setpoint to {test_cool}°F...")
        thermostat.set_setpoints(heat_setpoint=test_heat, cool_setpoint=test_cool)
        time.sleep(1)
        current_heat = thermostat.heat_setpoint
        current_cool = thermostat.cool_setpoint
        print(f"  Current setpoints: Heat={current_heat}°F, Cool={current_cool}°F")

    finally:
        # Restore original settings
        print("\nRestoring original settings...")
        if original_mode:
            thermostat.set_mode(original_mode)
        if original_fan:
            thermostat.set_fan_mode(original_fan)
        if original_heat is not None or original_cool is not None:
            thermostat.set_setpoints(heat_setpoint=original_heat, cool_setpoint=original_cool)

        print("Test complete!")

def main():
    # Create Lutron controller object
    lutron = Lutron(
        host=LUTRON_HOST,
        user=LUTRON_USER,
        password=LUTRON_PASSWORD
    )

    try:
        # Connect to the controller
        print(f"Connecting to Lutron system at {LUTRON_HOST}...")
        lutron.connect()

        # Load the XML database
        print("\nLoading XML database...")
        lutron.load_xml_db(cache_path=CACHE_FILE)

        # Find all areas with thermostats
        areas_with_thermostats = [area for area in lutron.areas if area.thermostats]
        print(f"\nFound {len(areas_with_thermostats)} areas with thermostats:")

        # Print details and test each thermostat
        for area in areas_with_thermostats:
            print(f"\nArea: {area.name}")
            print(f"  Number of thermostats: {len(area.thermostats)}")

            for thermostat in area.thermostats:
                print(f"\n  Thermostat: {thermostat.name}")
                print(f"    Integration ID: {thermostat.id}")

                try:
                    print(f"    Current Temperature: {thermostat.temperature}°F")
                    print(f"    Current Mode: {thermostat.mode.name if thermostat.mode else 'Unknown'}")
                    print(f"    Current Fan Mode: {thermostat.fan_mode.name if thermostat.fan_mode else 'Unknown'}")
                    print(f"    Heat Setpoint: {thermostat.heat_setpoint}°F")
                    print(f"    Cool Setpoint: {thermostat.cool_setpoint}°F")

                    # Run control tests
                    test_thermostat_controls(thermostat)

                except Exception as e:
                    print(f"    Error testing thermostat: {e}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Keep the script running to maintain connection
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()