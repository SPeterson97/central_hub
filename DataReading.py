#   Use this document to contain data reading objects
import datetime
from pytz import timezone

class DataReading:

    #   Data to store in the database
    angle_data = {"angle": 1}
    timestamp = None

    def __init__(self):
        #   Use this to init the data reading
        timestamp = datetime.datetime.now()
        angle_data = dict()
        
    def clear_data(self):
        #   Clear data
        angle_data = dict()
        
    def set_timestamp(self):
        timestamp = datetime.datetime.now()
        
    def add_data(self, data):
        #   Add a data point
        parsed_data = data.split(',')
        angle_data[str(parsed_data[0])] = int(parsed_data[1])
