#!/usr/bin/env python2

'''
Created Sep - Nov 2019
DataLogger Mini Spray Dryer B-290 
@author: Frederik Doerr (CMAC, frederik.doerr@strath.ac.uk, GitHub: https://github.com/frederik-d)

Setup (Raspbian):
Find Ard: ls -l /dev/ttyUSB*
Enable USB: sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/ttyACM0

Path: /home/pi/B290_RS232_Data/SprayDry_RS232_DataLogger.py

Make shell excecutable:
sudo chmod +x /home/pi/Desktop/DataLogger_RS232_autorun.sh

Minimum Working Example:
import os
import time
import datetime
import serial

DL_Port = '/dev/ttyUSB0'
DL_file_path = '/home/pi/B290_RS232_Data'

ser = serial.Serial(DL_Port, 2400, parity=serial.PARITY_NONE)

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
file_name ='Data_SprayDry_RS232_' + st + '.txt'

file_Sensor_DataLog = open(os.path.join(DL_file_path,file_name),'w')
print 'SprayDry_RS232_DataLogger\n' + 'StartTime: ' + st + ':\n'

while True:
	value_string = ser.readline()
        ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')     
	file_Sensor_DataLog.write(st + ';' + value_string)                
	print st + '\t' + value_string

'''
import os
import time
import serial
import datetime
import glob
import logging
import tkMessageBox
import multiprocessing
from multiprocessing import Process

class DataLogger(object):
    def __init__(self):
        self.DL_Port = '/dev/ttyUSB0'
        self.DL_file_path = '/home/pi/B290_RS232_Data'

    def ensure_dir(self):
        if not os.path.exists(self.DL_file_path):
            os.makedirs(self.DL_file_path)
            
    def createDataFile(self,file_path,file_name):
        self.file_ID = open(os.path.join(file_path,file_name),'a',0)
        self.file_ID.write('SprayDry RS232 DataLogger\n')
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
        self.file_ID.write('StartTime: ' + st + ':\n')
        self.B_290_RS232_Header = ('Timestamp;'+'RelTime_B290;'+'T_Inlet_READ;'+'T_Outlet_READ;'+'Heater;'+'T_Inlet_SET;'+'Aspirator;'+'Aspirator_Speed_SET;'+'Pump;'+'Pump_Speed_SET;'+'Feed_Switch;'+'Con_B_295;'+'Oxygen_HIGH;'+'Pressure_LOW;'+'ErrorMsg;\n')
	self.file_ID.write(self.B_290_RS232_Header)
        return self.file_ID

    def read_DataLogger(self,file_Sensor_DataLog):
	value = ser.read()
	value_string = ''
	while value.lower() != '\n':
	    value_string += value
	    value = ser.read()
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
        file_Sensor_DataLog.write(st + ';' + value_string + '\n')

    def run_DataLogger(self):
        current_time = 0	
	delay_time = 1
        self.ensure_dir()
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
	file_name ='Data_SprayDry_RS232_' + st + '.txt'
        value_string = ''
        ser_Check = False
        print 'Initiate Logging'
        if portIsUsable(self.DL_Port) and not ser_Check: #can only be read once!
            ser = serial.Serial(self.DL_Port, 2400, parity=serial.PARITY_NONE)
            ser_Check = True
            print 'Serial connected'
        while True:
		if not os.path.isfile(os.path.join(self.DL_file_path,file_name)):
	    		file_Sensor_DataLog = self.createDataFile(self.DL_file_path,file_name)
            		print 'SprayDry_RS232_DataLogger\n' + 'StartTime: ' + st + ':\n'
			print(self.B_290_RS232_Header)
                value_string = ser.readline()
                ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')     
		file_Sensor_DataLog.write(st + ';' + value_string)                
		print st + '\t' + value_string
		current_time = current_time + delay_time
        if ser_Check:
            file_Sensor_DataLog.close() 
            ser.close()
            
def portIsUsable(portName):
    try:
        ser = serial.Serial(port=portName)
        ser.close()
        return True
    except:
        return False


if __name__ == '__main__': 
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    dl = DataLogger()
    p2 = Process(target=DataLogger().run_DataLogger())
    p2.start()
