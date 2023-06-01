import board
import digitalio

# enable the relay as soon as possible
switch_pin_number = board.IO33
switch_pin = digitalio.DigitalInOut(switch_pin_number)
switch_pin.direction = digitalio.Direction.OUTPUT
switch_pin.value = True

import supervisor
supervisor.runtime.autoreload = False

import busio
import adafruit_adxl34x
import alarm
import time
import ulab
import espnow_display
import system_data

################################################################
# CONFIGURATIONS

timeout_minutes_to_disable_relay = 20 # 20 minutes seems a good value

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

system_data = system_data.SystemData()
espnow_display = espnow_display.Display(system_data)

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

previous_display_communication_counter = 0
last_time_reset = time.monotonic()

while True:
  espnow_display.process_data()

  if system_data.display_communication_counter != previous_display_communication_counter:
    previous_display_communication_counter = system_data.display_communication_counter
    
    # received data from the display, so update the last_time_reset
    last_time_reset = time.monotonic()

  if system_data.turn_off_relay:
    break

  # check for timeout
  if (time.monotonic() - last_time_reset) > (timeout_minutes_to_disable_relay * 60):
    break

  time.sleep(0.1)

# while True:
#   # calculate next timeout alarm
#   next_time_to_timeout = time.monotonic() + (timeout_minutes_to_disable_relay * 60)
#   timeout_alarm = alarm.time.TimeAlarm(monotonic_time = next_time_to_timeout)

#   # enter deep sleep and will wakeup only with movement detection or on the timeout
#   wakeup_reason = alarm.light_sleep_until_alarms(pin_alarm_motion_detection, timeout_alarm)
#   accelerometer._read_clear_interrupt_source() # need to clear the interrupt

#   if wakeup_reason == timeout_alarm:
#     # we just timeout, so leave this while True loop
#     break

# if we are here, we did timeout
# disable relay switch pin
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
pins_to_preserve = [switch_pin]
for pin in buzzer_pins:
  pins_to_preserve.append(pin)
alarm.exit_and_deep_sleep_until_alarms(pin_alarm_motion_detection, preserve_dios = pins_to_preserve)
# Does not return. Exits, and restarts after the deep sleep time.
