#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
from pyfirmata2 import Arduino
import time

#Original code titled "print_analog_data" by Bernd Porr <mail@berndporr.me.uk>
#Modified by Sherelle CH to fit Tugas 3 Sistem Mikroelektronika Biomedika (Kelas B)

PORT = Arduino.AUTODETECT

plt.style.use('seaborn-deep')

#initialize lists for plotting
xval = []
y0val = []
y1val = []
y2val = []

class AnalogPrinter:

    def __init__(self):
        # sampling rate: 50Hz
        self.samplingRate = 50
        self.timestamp = 0
        self.board = Arduino(PORT)

    def start0(self):
        self.board.analog[0].register_callback(self.myPrintCallback0)
        self.board.samplingOn(1000 / self.samplingRate)
        self.board.analog[0].enable_reporting()
        self.board.analog[1].register_callback(self.myPrintCallback1)
        self.board.analog[1].enable_reporting()
        self.board.analog[2].register_callback(self.myPrintCallback2)
        self.board.analog[2].enable_reporting()
        
    def myPrintCallback0(self, data0):
        hasil0=(data0/1)*5
        print("VR1 ","%f,%f" % (self.timestamp, hasil0)) 
        y0val.append(hasil0) 

    def myPrintCallback1(self, data1):
        hasil1=(data1/1)*5   
        print("VR2 ", "%f,%f" % (self.timestamp, hasil1))     
        y1val.append(hasil1)

    def myPrintCallback2(self, data2):
        hasil2=(data2/1)*5   
        print("VR3 ", "%f,%f" % (self.timestamp, hasil2))
        y2val.append(hasil2)
        xval.append(self.timestamp)
        self.timestamp += (1 / self.samplingRate)

    def stop(self):
        self.board.samplingOff()
        self.board.exit()

print("Let's print data from Arduino's analogue pins for 20secs.")

# Let's create an instance
analogPrinter = AnalogPrinter()

# and start DAQ
analogPrinter.start0()

#wait 20 seconds
time.sleep(20)

# stop DAQ
analogPrinter.stop()

#plotting
line1, = plt.plot(xval,y0val)
line2, = plt.plot(xval,y1val)
line3, = plt.plot(xval,y2val)

plt.legend([line1,line2,line3],["VR1","VR2","VR3"])

plt.ylabel('Voltage (V)')
plt.xlabel('Time (s)')
plt.title('Data Aquisition from 3 VRs')
plt.show()

print("finished")
