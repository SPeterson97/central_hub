#   This file will run the script for the Central Hub
#   This file was created by: Sam Peterson
#   This file was created on: 10/14/19
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import sys
from BleManager import BleManager

#######     Below are functions to support the main loop    #######
def run_mode():
    #   See if there are any commandline arguments to process
    args = sys.argv
    if len(args) is not 0 and args[1] is not None:
        print(args[1])
    #   Will need to read in that line and use it later`

    #   Return 1 for add peripheral, 2 for get data, -1 to quit
    while (True):
        print("Please enter what mode you would like to run in (1,2, or 3):\n ")
        temp = int(input("1. Add Peripheral\n2. Normal Function\n3. Quit\n"))

        if temp == 1:
            return 1
        elif temp == 2:
            return 2
        elif temp == 3:
            return -1

#######     --------------------------------------------    #######

#######     Add a new peripheral to get data from           #######
def add_peripheral():
    #   Here we want to collect data and add data to the database
    return 0


#######     --------------------------------------------    #######

#######     Below is to run the normal data gathering       #######
def run():
    #do nothing
    return 0

#######     --------------------------------------------    #######

#######     Below is the main script to run the program     #######
def main():
    #   Test scanning for peripherals
    '''
    ble_manager.setup()
    count = 0
    while count < 100:
        ble_manager.print_current_devices()
        count += 1
    '''
        
        
    #   Get everthing setup
    ble_manager.setup()
    
    #   Find the device
    device = None
    while device is None:
        device = ble_manager.find_device("Adafruit")

    print('Found {0}'.format(device.name))
    
    #   Initialize peripheral
    peripheral = BlePeripheral()
    peripheral.device = device
    
    try:
        #   Connect to the peripheral
        ble_manager.connect(peripheral.device)
        
        #   Set up uart
        peripheral.uart = ble_manager.setup_uart(peripheral.device)
        
        done = False
        while not done:
            message = input("Enter the message to send")
            if "done" in message:
                done = True
            else:
                ble_manager.send(peripheral.uart,message)
                
        
    finally:
        #   Disonnect to the peripheral
        ble_manager.disconnect(peripheral.device)
    
    
    
    #   Allow for multiple modes
    '''
    stop = False
    while (not stop):
        #   Get what mode the user wants to run in
        mode = run_mode()

        if mode == 1:
            print("Add Peripheral")
            #add_peripheral()
        elif mode == 2:
            print("Run")
            #run()
        elif mode == -1:
            stop = True
            
    '''
#######     --------------------------------------------    #######

#######               Initialization Pre-Main               #######

#   Let's initialize the Bluetooth prior to running the main
ble_manager = BleManager()

#   Run the main in a background thread
ble_manager.ble.run_mainloop_with(main)

#######     --------------------------------------------    #######
