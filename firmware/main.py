import board
import digitalio

import supervisor
supervisor.runtime.autoreload = False

# enable the IO pins to control the switch
# needs a few pins as the relay uses some good amount of current
switch_pins_numbers = [board.IO18, board.IO33, board.IO35, board.IO37, board.IO39]
switch_pins = [0] * len(switch_pins_numbers)

# configure the pins as outputs and enable
for index, switch_pin_number in enumerate(switch_pins_numbers):
  switch_pins[index] = digitalio.DigitalInOut(switch_pin_number)
  switch_pins[index].direction = digitalio.Direction.OUTPUT
  switch_pins[index].value = True

import busio
import adafruit_adxl34x
import alarm
import time
import gc
import espnow_comms
import system_data

################################################################
# CONFIGURATIONS

timeout_no_motion_minutes_to_disable_relay = 2 # 2 minutes seems a good value

seconds_to_wait_before_movement_detection = 20 # 20 seconds seems a good value

my_mac_address = [0x68, 0xb6, 0xb3, 0x01, 0xf7, 0xf1]

################################################################

timeout_no_motion_minutes_to_disable_relay *= 60 # need to multiply by 60 seconds

# if we are here, is because
# the system just wake up from deep sleep,
# due to motion detection
system_data = system_data.SystemData()
espnow_comms = espnow_comms.ESPNowComms(my_mac_address, system_data)

# pins used by the ADXL345
scl_pin = board.IO1
sda_pin = board.IO2
int1_pin = board.IO8

# init the ADXL345
i2c = busio.I2C(scl_pin, sda_pin)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_motion_detection(threshold = 18) # 18 seems a good value
accelerometer.events.get('motion') # this will clear the interrupt

last_time_reset = time.monotonic()

while True:
  # if motion is detected, reset the timeout counter
  if accelerometer.events.get('motion'):
    last_time_reset = time.monotonic()

  # if timeout, no motion was detected in last 2 minutes,
  # we should turn off the relay, so leave this infinite loop
  if (time.monotonic() - last_time_reset) > timeout_no_motion_minutes_to_disable_relay:
    break

  # check if we received the command to turn off the relay (by wireless communications)
  # will update the system_data.turn_off_relay
  espnow_comms.process_data()
  # if we should turn off the relay, leave this infinite loop
  if system_data.turn_off_relay:
    break

  # do memory clean
  gc.collect()

  # sleep some very little time before do everything again
  time.sleep(0.02)

# if we are here, we should turn off the relay
# disable relay switch pins
for index in range(len(switch_pins)):
  switch_pins[index].value = False

# wait some time before next movement detection
time.sleep(seconds_to_wait_before_movement_detection)

# pin change alarm, will be active when motion is detected by the ADXL345
pin_alarm_motion_detection = alarm.pin.PinAlarm(int1_pin, value = True)

accelerometer.events.get('motion') # this will clear the interrupt
alarm.exit_and_deep_sleep_until_alarms(pin_alarm_motion_detection, preserve_dios = switch_pins)
# Does not return. Exits, and restarts after the deep sleep time.
