import board
import busio
import adafruit_adxl34x
import alarm

# pins used buy the ADXL345
scl_pin = board.IO1
sda_pin = board.IO2
int1_pin = board.IO8

# pin for the switch
switch_pin = board.IO15

# init the ADXL345
i2c = busio.I2C(scl_pin, sda_pin)
accelerometer = adafruit_adxl34x.ADXL345(i2c)
accelerometer.enable_motion_detection()
accelerometer._read_clear_interrupt_source() # need to clear the interrupt

# pin change alarm, will be active when movement is detected by the ADXL345
pin_alarm = alarm.pin.PinAlarm(int1_pin, value = False)

# enter deep sleep
alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
# does not return. Exits, and restarts after the sleep time.
