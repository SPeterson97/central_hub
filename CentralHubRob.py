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
        mode = int(args[1])
        args_present = True

    #   Return 1 for add peripheral, 2 for get data, -1 to quit if no args
    while (not args_present):
        print("Please enter what mode you would like to run in (1,2, or 3):\n ")
        mode = int(input("1. Add Peripheral\n2. Normal Function\n3. Quit\n"))
        args_present = True

    if mode == 1:
        return 1
    elif mode == 2:
        return 2
    else:
        return -1

#######     --------------------------------------------    #######

#######     Add a new peripheral to get data from           #######
def add_peripheral():
    #   Here we want to collect data and add data to the database
    new_device_id = input("What to make the device id? ")
    mounted_height = int(input("What's the mounted height (cm)? "))
    data_arr = []
    
    print("Setting up database connection...")
    db = firestore.Client()
    db_col = db.collection(u'sensor_data')
    doc_ref = db_col.document(new_device_id)
    print("Connection established")
    
    #   Gather the peripherals from the data base
    devices = gather_database_peripherals()
    
    for i in range(3):
        #   Gather data 3 times
        for device in devices:
            #   Get the data from the readings
            get_data(device)
            
            print("Got data")
            
            data_arr.append(device.return_data())
    
    #   All data collected, now send to database
    doc_ref.set({
        u'base_to_road_angle' : 15,
        u'reading1' : data_arr[0].angle_data,
        u'reading2' : data_arr[1].angle_data,
        u'reading3' : data_arr[2].angle_data,
        u'gps_location' : None,
        u'lat' : 0,
        u'long' : 0,
        u'mounted_height' : mounted_height,
        u'sensor_id' : int(new_device_id)
    })
    print("Done")
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
        #counter = counter + 1
        
        #   Wait for 5 min or a response
        check_for_update()
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
    print("Finding the device")
    while test is None and elapsed < 15 and not device.device.is_connected:
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
        success = ble_manager.connect(device.device)
        
        if not success:
            print("Failure to connect")
            return

        #   Make sure that uart is set up
        if not device.uart_init:
            #   Set up uart
            print("Initializing UART")
            device.uart = ble_manager.setup_uart(device.device)
            device.uart_init = True
        else:
            print("UART already initialized")
        
        print("Telling device to run")
        device_responsive = ble_manager.get_response(device)
        
        #   Make sure the device is ready. If not, just return
        if not device_responsive:
            print("Starting the data collection failed")
            return
        
        #   Now sleep for 15 seconds
        time.sleep(8)
        
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
        #ble_manager.disconnect(device.device)
        return#print("Disconnected")
        
def check_for_update():
    #   Will check the database to see if we update, otherwise just wait 5 min
    start = time.time()
    time.clock()
    
    elapsed = 0
    print("Waiting to update")
    while elapsed < 300 and not check_update():
        #   Will wait 5 min or until triggered
        time.sleep(2)
        elapsed = time.time() - start
        
    return
    
def check_update():
    #   Check for trigger
    print("Checking to see if trigger was set")
    db = firestore.Client()
    db_col = db.collection(u'get_data_trigger')
    doc_ref = db_col.document(u'trigger')
    to_update = doc_ref.get().get(u'get_data')
    
    #   Now need to check if we need to update
    if to_update == 1:
        #   Yes, update. Reset back to 0.
        print("Trigger set")
        doc_ref.set({
            u'get_data': 0
        })
        
        return True
    else:
        #   No update
        return False

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

#######     --------------------------------------------    #######

#######               Initialization Pre-Main               #######

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/pi/Documents/SeniorDesign/central_hub/ParkIT-3ee0b46b06f7.json"

#   Initialize some global variables
update = False
db = None

#   Let's initialize the Bluetooth prior to running the main
ble_manager = BleManager()

#   Run the main in a background thread
ble_manager.ble.run_mainloop_with(main)
#######     --------------------------------------------    #######
