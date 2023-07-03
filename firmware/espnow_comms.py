import wifi
import espnow

class ESPNowComms(object):
    def __init__(self, mac_address, system_data,):
        
        wifi.radio.enabled = True
        wifi.radio.mac_address = bytearray(mac_address)
        self._espnow_comms = espnow.ESPNow()
        self._packets = []
        self._system_data = system_data
        self.power_switch_id = 4 # power switch ESPNow messages ID
        
    def process_data(self):
        try:
            data = self._espnow_comms.read()
            if data is not None:
                data = [n for n in data.msg.split()]
                # only process packages for us
                if int(data[0]) == self.power_switch_id:
                    self._system_data.display_communication_counter = int(data[1])
                    self._system_data.turn_off_relay = True if int(data[2]) != 0 else False

        except Exception as ex:
                pass

    def send_data(self):
        pass