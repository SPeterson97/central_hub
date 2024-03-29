#   This file will run the script for the Central Hub
#   This file was created by: Sam Peterson
#   This file was created on: 10/14/19
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
from google.cloud import firestore
import sys
from BleManager import BleManager
from BlePeripheral import BlePeripheral
from threading import Thread
import time
from datetime import datetime
import os
import uuid

#######     Below are functions to support the main loop    #######
def run_mode():
    #   See if there are any commandline arguments to process
    args = sys.argv
    args_present = False
    if len(args) > 1 and args[1] is not None:
        print(args[1])
        temp = int(args[1])
        args_present = True
    #   Will need to read in that line and use it later`

    #   Return 1 for add peripheral, 2 for get data, -1 to quit
    while (not args_present):
        print("Please enter what mode you would like to run in (1,2, or 3):\n ")
        temp = int(input("1. Add Peripheral\n2. Normal Function\n3. Quit\n"))
        args_present = True

    if temp == 1:
        return 1
    elif temp == 2:
        return 2
    else:
        return -1

#######     --------------------------------------------    #######

#######     Add a new peripheral to get data from           #######
def add_peripheral():
    #   Here we want to collect data and add data to the database
    return 0


#######     --------------------------------------------    #######

#######     Below is to run the normal data gathering       #######
def run():
    #   Set up database connections
    print("Setting up database connection...")
    db = firestore.Client()
    db_col = db.collection(u'data')
    print("Connection established")

    #   Gather the peripherals from the data base
    devices = gather_database_peripherals()
    
    #   Will want to get reading every 5 minutes.
    count = 1
    while (count == 1):
        #   Gather data from each device
        for device in devices:
            #   Get the data from the readings
            get_data(device)
        '''
        d = BlePeripheral()
        d.saved_data_buffer = ["0,1;1,2;2,3","3,4;4,5"]
        d.sensor_id = 50
        now = datetime.now().strftime("%m%d%Y_%H%M")
        doc_ref = db_col.document(now)
        d.send_data(doc_ref)
        '''
        print("Got data, going to process data")
        
        #   Now have the device process their data
        for device in devices:
            print(device.device_name)
            #   Have each device send the data
            now = datetime.now().strftime("%m%d%Y_%H%M")
            doc_ref = db_col.document(now)
            device.send_data(doc_ref)
            
        print("Done")
        print("Counter: "+str(count))
        #   Sleep for 1min now
        time.sleep(30)
    return 0
    
def gather_database_peripherals():
    #   Need to return list of peripherals
    
    #   Will got to database later, just get device for now
    device = None
    while device is None:
        device = ble_manager.find_device("Adafruit")
        #service_uuids=[uuid.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')]
        
    print('Found {0}'.format(device.name))
    
    #   Initialize peripheral
    peripheral = BlePeripheral()
    peripheral.device = device
    
    return [peripheral]
    
def get_data(device):
    #   Make sure the device is in range and set timeout of 15 seconds
    start = time.time()
    time.clock()
    
    test = None
    elapsed = 0
    while test is None and elapsed < 15:
        print("Finding the device")
        test = ble_manager.find_device(device.device_name)
        elapsed = time.time() - start
        
    #   See if we timed out
    if elapsed > 15:
        print("Couldn't find -- timeout")
        return
        
    #   Now that the device is in range, start getting data process
    try:
        #   Connect to the peripheral
        print("Connecting")
        ble_manager.connect(device.device)
    
        #   Make sure that uart is set up
        if not device.uart_init:
            #   Set up uart
            print("Initializing UART")
            device.uart = ble_manager.setup_uart(device.device)
            device.uart_init = True
            
        #   Set up device to start reading data
        thread = Thread(target = ble_manager.read_data, args = (device, ))
        print("Starting thread:")
        thread.start()
        print("Thread running")
        
        #   UART is set up and looking for data, need to signal the device to start reading data
        ble_manager.send(device.uart, "START")
        
        #   Wait for the thread to finish
        thread.join()
        print("Thread done, returning and disconnecting to process data")
    except:
        return
    finally:
        #   Make sure we disconnect
        ble_manager.disconnect(device.device)
        print("Disconnected")

#######     --------------------------------------------    #######

#######     Below is the main script to run the program     #######
def main():
    #   Get everthing setup
    ble_manager.setup()
    
    #   Lets figure out what to run
    mode = run_mode()
    
    if mode == 1:
        #   Need to add peripherals
        add_peripheral()
    elif mode == 2:
        #   Normal operation
        run()
        print("Done running")
        sys.exit(0)
    else:
        #   Just exit
        sys.exit(0)
    
    '''
    #   Scan for the devices
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
        flag = 1
        while True:
            if not peripheral.device.is_connected:
                #   Connect to the peripheral
                ble_manager.connect(peripheral.device)
                
                if flag == 1:
                    #   Set up uart
                    peripheral.uart = ble_manager.setup_uart(peripheral.device)
                    flag = 2
                
                #   Start looking for data
                thread = Thread(target = ble_manager.read_data, args = (peripheral.uart,peripheral.device, ))
                print("Starting thread:")
                thread.start()
                print("Thread running")
                thread.join()
                print("Thread done")
        
        
        #   Being loop to send data
        
        done = False
        while not done:
            message = input("Enter the message to send: ")
            if "done" in message:
                done = True
            else:
                ble_manager.send(peripheral.uart,message)
         
        
    finally:
        #   Disonnect to the peripheral
        print("Exiting")
        ble_manager.disconnect(peripheral.device)
    '''
    sys.exit(0)
    
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

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/pi/Documents/SeniorDesign/central_hub/ParkIT-3ee0b46b06f7.json"
'''
while(True):
    try:
        #   Let's initialize the Bluetooth prior to running the main
        ble_manager = BleManager()

        #   Run the main in a background thread
        ble_manager.ble.run_mainloop_with(main)
    except:
        print("There was an error... Rerunning")
    finally:
        print("Rerunning")
'''
#   Let's initialize the Bluetooth prior to running the main
ble_manager = BleManager()

#   Run the main in a background thread
ble_manager.ble.run_mainloop_with(main)
#######     --------------------------------------------    #######
