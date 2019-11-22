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
    read = None
    read_data_buffer = list()
    look_for_data = False


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
        #   First check to see if we are already connected or not
        if device.is_connected:
            #   Device is already connected, don't do anything
            print("Device is already connected")
            return True
    
        #   Connect to the peripheral device and try to disconnect
        try:
            device.connect()
            success = True
        except:
            success = False
        finally:
            #   Don't handle the error, may have abruptly disconnected
            return success
        
    def disconnect(self, device):
        #   Disconnect from device
        try:
            if device.is_connected:
                device.disconnect()
            #else:
            #    device.connect()
            #    device.disconnect()
        finally:
            if not device.is_connected:
                #   Already disconnected, just return
                return
            else:
                #   Problem disconnecting, just return anyways
                return
            

    def send(self, uart, message):
        #   Send the message via uart
        uart.write(str(message+"\n").encode())
        print("Send the message: {0}".format(message))

    def read_data(self, peripheral):
        #   Continuously read data until we time out 5 times
        timeouts = 0
        got_data = False
        
        while peripheral.device.is_connected and timeouts < 3:
            #   Read data for x number of seconds
            print("Reading data")
            received = peripheral.uart.read(timeout_sec=5)
            
            #   Add the received data to the buffer
            if received is not None:
                peripheral.saved_data_buffer.append(received)
                got_data = True
                print(str(received))
            elif got_data and received is None:
                print("Already got data and timed out.. returning")
                return
            else:
                print("--No data received--")
                timeouts = timeouts + 1
    
    def get_response(self, peripheral):
        #   Continuously tell the peripheral to read data
        got_response = False
    
        while peripheral.device.is_connected and not got_response:
            #   Set up device to start reading data
            print("Starting thread")
            thread = Thread(target = self.send_get_data, args = (peripheral.uart,))
            print("Start thread to send data request:")
            thread.start()
            print("Thread started, going to wait a second before sending data")
        
            #   Read data for x number of seconds
            print("Waiting for response of OK")
            received = peripheral.uart.read(timeout_sec=3)
            
            #   Join the thread now
            thread.join()
        
            #   Add the received data to the buffer
            if received is not None and received is "ok":
                #   Got response we wanted
                got_response = True
                print("Received: "+str(received))
            elif received is None:
                print("--No response received--")
            else:
                print("--Got different response than expected--")
                
        #   Let's see if the device disconnected
        if not peripheral.device.is_connected:
            #   Know the device disconnected without getting response, so return false
            print("Peripheral disconnected without getting a response")
            return False
        #   Got the correct response, so return true
        return True
                
    def send_get_data(self, uart):
        #   Wait a second and then send data
        time.sleep(1)
        self.send(uart, "DATA")

    def stop_reading(self, uart):
        #   Stop the reading of data
        read = False
