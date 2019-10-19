#   This file will run the script for the Central Hub
#   This file was created by: Sam Peterson
#   This file was created on: 10/14/19
import bluetooth
import sys

#######     Below are functions to support the main loop    #######
def run_mode():
    #   See if there are any commandline arguments to process
    args = sys.argv
    if args.length is not 0 and args[0] is not None:
        print(args[0])

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
    #   Allow for multiple modes
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
#######     --------------------------------------------    #######









main()