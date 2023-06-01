import espnow

class Display(object):
    def __init__(self, system_data):
        
        self._display_espnow = espnow.ESPNow()
        self._packets = []
        self._system_data = system_data
        self.power_switch_id = 5 # power switch ESPNow messages ID
        
    def process_data(self):
        # let's clear the buffer
        data = self._display_espnow.read()
        if data is not None:
            data = [n for n in data.msg.split()]
            # only process packages for us
            if int(data[0]) == self.power_switch_id:
              self._system_data.display_communication_counter = int(data[1])
              self._system_data.turn_off_relay = True if int(data[2]) != 0 else False
              print(self._system_data.turn_off_relay)

    def send_data(self):
        pass