import board
import digitalio

# enable the relay as soon as possible
switch_pin_number = board.IO33
switch_pin = digitalio.DigitalInOut(switch_pin_number)
switch_pin.direction = digitalio.Direction.OUTPUT
switch_pin.value = True

import busio
import adafruit_adxl34x
import alarm
import time
import ulab

################################################################
# CONFIGURATIONS

timeout_minutes_to_disable_JBD_BMS = 20 # 20 minutes seems a good value

################################################################

# if we are here, is because
# the system just wake up from deep sleep,
# due to motion detection

def buzzer_set_state(state):
  for index in range(len(buzzer_pins)):
    buzzer_pins[index].value = state

def buzzer_play(sequence):
  for delay_time in sequence:
    buzzer_set_state(True)
    time.sleep(delay_time[0])
    buzzer_set_state(False)
    time.sleep(delay_time[1])

# enable the IO pins to control the buzzer
# needs a few pins as the buzzer uses about 20mA
buzzer_pins_numbers = [board.IO3, board.IO5, board.IO7, board.IO9, board.IO11, board.IO12]
buzzer_pins = [0] * len(buzzer_pins_numbers)

# configure the pins as outputs
for index, buzzer_pin_number in enumerate(buzzer_pins_numbers):
  buzzer_pins[index] = digitalio.DigitalInOut(buzzer_pin_number)
  buzzer_pins[index].direction = digitalio.Direction.OUTPUT

# play the enable relay sequence sound
time_array_lenght = 10
time_on_array = ulab.numpy.linspace(0.005, 0.05, time_array_lenght)
time_off_array = ulab.numpy.linspace(0.05, 0.0005, time_array_lenght)
play_sequence = [[0,0]] * time_array_lenght
for i in range(time_array_lenght):
  play_sequence[i] = [time_on_array[i], time_off_array[i]]
buzzer_play(play_sequence)

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
pin_alarm_motion_detection = alarm.pin.PinAlarm(int1_pin, value = True)

while True:
  # calculate next timeout alarm
  next_time_to_timeout = time.monotonic() + (timeout_minutes_to_disable_JBD_BMS * 60)
  timeout_alarm = alarm.time.TimeAlarm(monotonic_time = next_time_to_timeout)

  # enter deep sleep and will wakeup only with movement detection or on the timeout
  wakeup_reason = alarm.light_sleep_until_alarms(pin_alarm_motion_detection, timeout_alarm)
  accelerometer._read_clear_interrupt_source() # need to clear the interrupt

  if wakeup_reason == timeout_alarm:
    # we just timeout, so leave this while True loop
    break

# if we are here, we did timeout
# disable JBD BMS switch pin
switch_pin.value = False

# play the disable relay sequence sound
time_array_lenght = 10
time_on_array = ulab.numpy.linspace(0.005, 0.0005, time_array_lenght)
time_off_array = ulab.numpy.linspace(0.001, 0.1, time_array_lenght)
play_sequence = [[0,0]] * time_array_lenght
for i in range(time_array_lenght):
  play_sequence[i] = [time_on_array[i], time_off_array[i]]
buzzer_play(play_sequence)

# now enter in deep sleep
# preserve the switch pin state, which is disable
alarm.exit_and_deep_sleep_until_alarms(pin_alarm_motion_detection, preserve_dios = [switch_pin])
# Does not return. Exits, and restarts after the deep sleep time.
