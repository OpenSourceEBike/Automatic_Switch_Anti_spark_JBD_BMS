# Automatic switch anti-spark for JBD BMS

**What:** switches ON the [popular JBD BMS](https://jiabaidabms.com/), effectively switching ON the EBike/EScooter with a shaking/vibration. Avoids the need to install a mechanical switch and also adds a safe timeout for automatically switching OFF the EBike/EScooter.

WORK IN PROGRESS, not finished yet!

## Features ##
* **Switch ON the EBike/EScooter by shaking:** JBD BMS switchs ON when shaking / make vibrations of the EBike/EScooter.
* **Automatic switch OFF the EBike/EScooter:** JBD BMS switchs OFF after a custom timeout like 30 minutes, when there is no more vibrations.
* **Wireless communication with other boards (optional):** an EBike/EScooter main board can communicate by wireless and switch OFF immediatly the JBD BMS.
* **Cheap and easy to DIY:** costs 5€ in materials and needs only soldering 8 wires

## Tecnhical notes ##
* Hardware
    * very easy to DIY: only 8 wires to solder ([see the schematic](hardware/schematic.png))
    * [low power](https://learn.adafruit.com/deep-sleep-with-circuitpython/power-consumption): espected to use only 0.007 watts when JBD BMS is switched OFF (will take 8 years to discharge a 500Wh battery)
* Firmware
    * uses easy to learn and fast to develop [Python language](https://circuitpython.org/)
    * only need a USB-C cable to program the firmware (optionally by wireless Wifi)
    * [ADXL345 library](https://github.com/adafruit/Adafruit_CircuitPython_ADXL34x)
    * [sleep low power mode](https://learn.adafruit.com/deep-sleep-with-circuitpython/power-consumption)
    * uses [ESPNow low power wireless communication](https://docs.circuitpython.org/en/latest/shared-bindings/espnow/index.html)

## Schematic ##
<img src=hardware/schematic.png>
