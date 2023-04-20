# Automatic switch anti-spark for JBD BMS

**What:** a small DIY board that automatically switches ON the [popular JBD BMS](https://jiabaidabms.com/), effectively switching ON the EBike/EScooter, when there is movement / vibration. Automatically switches OFF the BMS after a timeout without vibration, like 20 minutes (configured).<br>

Avoids the need to install a mechanical switch and also adds the safe timeout that automatically switchs OFF the EBike/EScooter.

On the next picture, the green board is the JBD BMS and the other small purple and blue board, is the DIY automatic switch board:<br>
[<img src=documentation/board_05.jpg width=400>](documentation/board_05.jpg)

## Features ##
* **Switch ON the EBike/EScooter by shaking:** JBD BMS switchs ON when shaking / make vibrations of the EBike/EScooter.
* **Automatic switch OFF the EBike/EScooter:** JBD BMS switchs OFF after a custom timeout like 30 minutes, when there is no more vibrations.
* **Wireless communication with other boards (planned, optional):** an EBike/EScooter main board can communicate by wireless and switch OFF immediatly the JBD BMS.
* **Cheap and easy to DIY:** costs 5€ in materials and needs only soldering 8 wires

## How to build it ##

You will need to buy the ESP32-S2 Lolin S2 Mini board (I bought on Aliexpress).<br>
You will also need to buy the ADXL345 module board (I bought on Aliexpress).

### Install CircuitPyhton ###

Download the archieved CircuitPyhton binary from [here](/circuitpython_binary). Connect the ESP32-S2 board in bootloader mode to your PC with a USB-C cable.



<img src=hardware/schematic.png>




## Technical notes ##
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
