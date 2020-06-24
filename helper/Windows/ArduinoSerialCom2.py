import time
#TODO: Find a way to autodiscover the com port and offer a suggestion for selection
import serial
from serial.tools import list_ports
global ser


def write_to_file(data):
    #TODO: Find environment variable to save to windows temp directory to cope with permissions
    dataFile = open("cheserem.key", mode="w")
    dataFile.write(data)
def getValues():
    global ser
    ser.write(b'w')
    arduinoData = ser.readline().decode('ascii')
    return arduinoData


try:
    cdc = next(list_ports.grep("CH340"))
    print("Device was found ")
    # global ser
    ser = serial.Serial(f'{cdc.device}', baudrate=115200, timeout=1)
    time.sleep(2)
    # Do connection stuff on cdc
    status = True
    gotten = True
    userinput = 'y'  # input("Get a value ? ")
    values = []
    while status:
        if userinput == 'y':
            #:TODO: if the program is idle for too long I need it to remain paused
            # TODO: and resumes on user input
            while gotten:
                print("calling getValues() function")
                # saves arduino data line by line
                print(f"Before saving the contained value is {values}")
                values = getValues()
                # print(f"The gotten value is {values}")
                if values[:].__contains__("UID Value"):
                    print("UID value gotten the program is soon exiting")
                    # print(f"The array contains the following values: {values[:]}")
                    gotten = False

                # for i in values:
                #     if i.__contains__("UID Value"):
                #         # print( f"{i} is containing")
                #        gotten = False
            status = False

            # if statement that check if values contains the string UID Value if so exit loop
            # and save output to a file.
            print("Card Swipe was Successful !!!!!!!!!!!")
    print(f"Winners prize is {values}")
    write_to_file(values)
    ser.close()

except StopIteration:

    print ("No device found")
    # ser.close()


