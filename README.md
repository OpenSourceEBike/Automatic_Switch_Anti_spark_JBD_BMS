# Automatic switch anti-spark for JBD BMS

**What:** a small DIY board that automatically switches ON the [popular JBD BMS](https://jiabaidabms.com/), effectively switching ON the EBike/EScooter, when there is motion / vibration. Automatically switches OFF the BMS after a timeout without motion, like 20 minutes (configured).<br>

Avoids the need to install a mechanical switch and also adds the safe timeout that automatically switches OFF the EBike/EScooter.

On the next picture, the green board is the JBD BMS and the other small purple and blue board, is the DIY automatic switch board:<br>
[<img src=documentation/board_05.jpg width=400>](documentation/board_05.jpg)

## Features ##
* **Switches ON the EBike/EScooter by detection motion:** JBD BMS switches ON when there is motion of the EBike/EScooter.
* **Automatic switches OFF the EBike/EScooter:** JBD BMS switches OFF after a custom timeout like 30 minutes, when there is no more motion.
* **[Ultra low power](https://learn.adafruit.com/deep-sleep-with-circuitpython/power-consumption):** espected to use only 0.007 watts when JBD BMS is switched OFF (will take 8 years to discharge a 500Wh battery).
* **Cheap and easy to DIY:** costs 5€ in materials and needs only soldering 8 wires.
* **Wireless communication with other boards (planned, optional):** an EBike/EScooter main board can communicate by wireless and switch OFF immediatly the JBD BMS.

## How to build it ##

You will need to buy the ESP32-S2 Lolin S2 Mini board (I bought on Aliexpress).<br>
You will also need to buy the ADXL345 module board (I bought on Aliexpress).

### 1. Install CircuitPyhton ###

Download the archieved CircuitPyhton binary from [here](firmware/circuitpython_binary/adafruit-circuitpython-lolin_s2_mini-en_US-8.1.0-beta.1.bin).<br>

Connect the ESP32-S2 board in bootloader mode to your PC with a USB-C cable. On Linux I use this command to flash the CircuitPython:<br>

```esptool.py write_flash 0 adafruit-circuitpython-lolin_s2_mini-en_US-8.1.0-beta.1.bin```

Follow the CircuitPython guides to make sure your board is working, like make some print("hello world") code.

### 2. Install the firmware ###

Connect the ESP32-S2 board to your PC using a USB-C cable. A USB flash disk should apear. Copy the files main.py and safemode.py, as also the lib folder, to the USB flash disk. Unmount the USB flash disk from your PC, remove the USB-C cable. Next time you power up the ESP32-S2 board, the firmware will run, like when connecting again the USB-C cable. See the CircuitPyhton basic tutorial if you have questions.

### 3. Understand the schematic ###

[<img src=hardware/schematic.png width=800>](hardware/schematic.png)

The ESP32-S2 board is powered by the 3.3V from the BMS. The BMS have a continuous 3.3V voltage, even when it is switched off. This means the ESP32-S2 will always be running, althought in deep sleep mode, ultra low power, while waiting for the motion pin signal change, that is the output of ADXL345 module.

The ADXL345 module is powered also by the 3.3V from the BMS and is ultra low power. With motion, the ADXL345 INT1 pin will change.

The switch signal from the ESP32-S2, will have a 0 volts to turn switch on the BMS and 3.3V to switch off the BMS.

### 4. Build the board ###

Following the schematic, build the board as the following images.

I did solder the ADXL345 board on the back of the ESP32-S2 board. I used kapton tape to make sure I isolated the back of both boards from touch electronically each other. I also used dual face tape.

I used 6 header pins to solder the pins directly, and avoid the need to wires wires. Still, 2 wires are needed: 3.3V (VCC) and GND (black wire):<br>
[<img src=documentation/board_01.jpg width=400>](documentation/board_01.jpg)

[<img src=documentation/board_02.jpg width=400>](documentation/board_02.jpg)

Top of the ESP32-S2 board:<br>
[<img src=documentation/board_03.jpg width=400>](documentation/board_03.jpg)

Top save the most power possible, I removed the little resistor near the LED and this way there are no energy used by the LED. I also removed the 5 pin little integrated circuit, that is 5V -> 3.3V voltage regulator - note that once you remove it, the board will only work when you provid the 3.3V externally, it will not work any more from the USB-C:<br>
[<img src=documentation/board_04.jpg width=400>](documentation/board_04.jpg)

Here are the connections to the BMS. You need to find where is the switch connection on the board, on my case the connector was not populated. I measured with the multimeter and found the pad on the PCB that is equal to the B+, that is the GND and so I wired to there the black wire.

The 3.3V is common to the BMS microcontroller, and there I wired the red wire.

The other pin of the switch connection on the BMS board, has 3.3V but will be connected to the GND by the ESP32-S2 to switch on the BMS.

[<img src=documentation/board_05.jpg width=400>](documentation/board_05.jpg)

To test if everything is working, measure the voltage with the multimeter between the GND and the 3.3V on the ESP32-S2 board - it must be near 3.3 volts. Then measure between the GND and the switch wire (yellow) - should be near 0 volts when the ESP32-S2 board detects motion but after the timeout, it will be 3.3V - hard to measure with the multimeter as you will make motion to be able to measure.

NOTE: you can use the JBD BMS app to see the switch state. You will need to enable the switch feature on the app, otherwise it will never switch on.

Finally, use some good tape to cover all the board.

## Understand the firmware (optional) ##

The firmware is on the following files:
* main.py
* safemode.py
* lib folder

The main firmware is on the main.py file. The safemode.py code is run if eventiually the Pyhton enters in safemode, and that will reboot the board to the regular mode.

The lib folder has the needed Pyhton libraries, like the adafruit_adxl34x that communicates with the ADXL345 module.

The main firmware:
* Starts by turn switch pin to low state / 0 volts, as needed to switch on the BMS.
* Initialize the ADXL345 and enable the motion detection. The ADXL345 will change the INT1 pin when it detects motion.
* A PinAlarm is created, this will wakeup the ESP32-S2 everytime the ADXL345 INT1 pin changes.
* The code inside the while True will run continuously until the timeout happens (no motion detected during timeout_minutes_to_disable_JBD_BMS minutes) and wake up the ESP32-S2 from the light sleep mode.
  * There are 2 alarms here that will wake up the ESP32-S2: alarm to detect motion and timeout alarm. If the motion alarm wakes up the ESP32-S2, the timeout will be restarted. When the timeout alarm happens, the while True loop is stopped with the break.
* Next code runs because the timeout did happen, so the code switches off the BMS by turning the switch pin to logic 1 / 3.3 volts.
* Finally, ESP32-S2 enters in deep sleep mode (ultra low power), keeping the switch pin in the state to keep the BMS switched off. The motion alarm will be active meaning the ESP32-S2 will then wake up when detection motion, and the firmware will run again starting from the begin.

Planned: use [ESPNow low power wireless communication](https://docs.circuitpython.org/en/latest/shared-bindings/espnow/index.html) to communicate with the EBike/EScooter board by wireless, that will be able to switch OFF immediatly the JBD BMS.


