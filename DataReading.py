#   Use this document to contain data reading objects
import datetime
from pytz import timezone

class DataReading:

    #   Data to store in the database {"angle": 1}
    angle_data = dict()
    timestamp = None

    def __init__(self):
        #   Use this to init the data reading
        self.timestamp = datetime.datetime.now()
        angle_data = dict()
        
    def clear_data(self):
        #   Clear data
        angle_data = dict()
        
    def set_timestamp(self):
        timestamp = datetime.datetime.now(timezone('EST'))
        
    def add_data(self, data):
        #   Add a data point
        print(data)
        parsed_data = data.split(',')
        distance = 0
        try:
            distance = int(parsed_data[1])
        except:
            distance = 0
        
        self.angle_data[str(parsed_data[0])] = distance
