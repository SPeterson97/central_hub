#This file will be used for BLE peripheral devices
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


    def __init__():
        #   Initialize the peripheral sensor