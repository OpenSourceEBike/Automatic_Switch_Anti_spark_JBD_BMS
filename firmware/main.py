import board
import busio
import adafruit_adxl34x
import alarm
import digitalio
import time

################################################################
# CONFIGURATIONS

timeout_minutes_to_disable_JBD_BMS = 20 # 20 minutes seems a good value

################################################################

# if we are here, is because
# the system just wake up from deep sleep,
# due to motion detection

# enable the JBD BMS switch
switch_pin_number = board.IO15
switch_pin = digitalio.DigitalInOut(switch_pin_number)
switch_pin.direction = digitalio.Direction.OUTPUT
# JBD BMS is enabled by pulling the switch pin to GND
switch_pin.value = False 

# pins used by the ADXL345
scl_pin = board.IO1
sda_pin = board.IO2
int1_pin = board.IO8

# init the ADXL345
i2c = busio.I2C(scl_pin, sda_pin)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_motion_detection()
accelerometer._read_clear_interrupt_source() # need to clear the interrupt

# pin change alarm, will be active when motion is detected by the ADXL345
pin_alarm_motion_detection = alarm.pin.PinAlarm(int1_pin, value = False)

while True:
  # calculate next timeout alarm
  # next_time_to_timeout = time.monotonic() + (timeout_minutes_to_disable_JBD_BMS * 60)
  next_time_to_timeout = time.monotonic() + (10)
  timeout_alarm = alarm.time.TimeAlarm(monotonic_time = next_time_to_timeout)

  # enter deep sleep and will wakeup only with movement detection or on the timeout
  wakeup_reason = alarm.light_sleep_until_alarms(pin_alarm_motion_detection, timeout_alarm)
  accelerometer._read_clear_interrupt_source() # need to clear the interrupt

  if wakeup_reason == timeout_alarm:
    # we just timeout, so leave this while True loop
    break
  
# if we are here, we did timeout
# disable JBD BMS switch pin
switch_pin.value = True

# now enter in deep sleep
# preserve the switch pin state, which is disable
alarm.exit_and_deep_sleep_until_alarms(pin_alarm_motion_detection, preserve_dios = [switch_pin])
# Does not return. Exits, and restarts after the deep sleep time.
