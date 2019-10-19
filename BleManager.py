#   This file will maintain the connection to bluetooth devices
#   This file was created by: Sam Peterson
#   This file was created on: 10/19/19
import atexit
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART


class BleManager:
    
    #   Class Attributes:
    ble = None
    adapter = None
    uarts = None
    


    def __init__(self):
        #   Initialize the BLE provider
        ble = Adafruit_BluefruitLE.get_provider()
        
        #   Initialize the BLE system
        ble.initialize()

    def uart_setup():
        #   Clear any cached data, prevent from going stale
        ble.clear_cached_data()
        
        #   Get a BLE network adapter and turn it on
        adapter = ble.get_default_adapter()
        adapter.power_on()
        
        #   Disconnect from any uart devices
        UART.disconnect_devices()

    def scan():
        #   Search for available UART devices
        adapter.start_scan()
        
        #   Make sure we stop scanning after the program is over
        atexit.register(adapter.stop_scan)
        
        #   Get the found UART devices
        uarts = set(UART.find_devices())
        
        #   Finish scanning
        adapter.stop_scan()
        
    def print_current_devices():
        #   Re-scan for current devices
        self.scan()
        
        count = 1
        
        #   Print out the names of the current devices
        if uarts != None:
            for device in uarts:
                print(str(count) + ". " +device.name)
                count += 1
