#This file will be used for BLE peripheral devices
from google.cloud import firestore
import datetime
from pytz import timezone
from DataReading import DataReading

class BlePeripheral:

    #   This data is what will be stored in the database
    sensor_id = -1
    gps_lat = -1
    gps_long = -1
    mounted_height = -1
    base_to_road_angle = -1

    #   Other necessary data
    uuid = ""
    device_name = ""
    
    #   More UART objects
    device = None
    uart = None
    uart_init = False
    
    #   Data saved
    saved_data_buffer = None
    

    def __init__(self):
        #   Initialize the peripheral sensor
        self.uart = None
        self.saved_data_buffer = list()
        
    def send_data(self, db):
        #   First, check to see if there is data to send
        if self.saved_data_buffer is None or len(self.saved_data_buffer) < 2:
            print("No data to send to database")
            return
            
        #   Parse data and send it to the database
        data = self._parse_data()
        
        #   Send the database object
        db.set({
            u'angle_data' : data.angle_data,
            u'sensor_id' : self.sensor_id,
            u'time_stamp' : data.timestamp
        })
        
        #   Clear data
        self.saved_data_buffer = list()
        
    def return_data(self):
        #   First, check to see if there is data to send
        if self.saved_data_buffer is None or len(self.saved_data_buffer) < 2:
            print("No data to send to database")
            return
                
        #   Parse data and send it to the database
        data = self._parse_data()
            
        #   Clear data
        self.saved_data_buffer = list()
        
        #   Return the parsed data
        return data
        
    def _parse_data(self):
        #   Append all the data together
        temp_str = ""
        for data in self.saved_data_buffer:
            temp_str = temp_str + str(data)
        
        #   Break the data apart: 0,1;1,3;...
        temp_data = list()
        for d in temp_str.split(';'):
            if d is not None or d is not "":
                temp_data.append(d)
        
        #   Populate the Data Reading object
        newest_data = DataReading()
        for data_point in temp_data:
            #   Make sure we look at valid data point
            if len(data_point) > 1 and (data_point[0] is not None or data_point[0] is not ""):
                #   If we get nothing for the distance, just put 0
                if data_point[1] is None or data_point[1] is "":
                    data_point[1] = 0
                    newest_data.add_data(data_point)
                else:
                    newest_data.add_data(data_point)
            
        #   Return the data reading object
        return newest_data
