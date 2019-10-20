#   This file will maintain the connection to bluetooth devices
#   This file was created by: Sam Peterson
#   This file was created on: 10/19/19
import atexit
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import io
import sys


class BleManager:
    
    #   Class Attributes:
    adapter = None
    uarts = None
    


    def __init__(self):
        #   Want to catch any output while initializing
        text_catcher = io.StringIO()
        sys.stdout = text_catcher
        
        #   Initialize the BLE provider
        self.ble = Adafruit_BluefruitLE.get_provider()
        
        #   Initialize the BLE system
        self.ble.initialize()
        
        #   Restore printing to console
        sys.stdout = sys.__stdout__

    def setup(self):
        #   Clear any cached data, prevent from going stale
        self.ble.clear_cached_data()
        
        #   Get a BLE network adapter and turn it on
        self.adapter = self.ble.get_default_adapter()
        self.adapter.power_on()
        
        #   Disconnect from any uart devices
        UART.disconnect_devices()

    def scan(self):
        #   Search for available UART devices
        try:
            self.adapter.start_scan()
        
            #   Make sure we stop scanning after the program is over
            #atexit.register(self.adapter.stop_scan)
        
            #   Get the found UART devices
            self.uarts = set(UART.find_devices())
        finally:
            #   Finish scanning
            self.adapter.stop_scan()
            
    def find_device(self, name):
        #   Scan to see if we can find any devices
        self.scan()
        
        #   Return the proper device, otherwise return none
        if self.uarts != None and len(self.uarts) != 0:
            for device in self.uarts:
                if name in device.name:
                    return device
        else:
            return None
        
    def print_current_devices(self):
        #   Re-scan for current devices
        self.scan()
        
        count = 1
        
        #   Print out the names of the current devices
        if self.uarts != None and len(self.uarts) != 0:
            for device in self.uarts:
                print(str(count) + ". " +device.name)
                count += 1
        else:
            print("\tNone found")
            
    def setup_uart(self, device):
        print('Discovering services...')
        #   Discover the services and create a uart object
        UART.discover(device)
        
        # Once service discovery is complete create an instance of the service
        # and start interacting with it.
        uart = UART(device)
        
        return uart

    def connect(self, device):
        #   Connect to the peripheral device and try to disconnect
        device.connect()
        
    def disconnect(self, device):
        #   Disconnect from device
        device.disconnect()

    def send(self, uart, message):
        #   Send the message via uart
        uart.write(message.encode())
        print("Send the message: {0}".format(message))
