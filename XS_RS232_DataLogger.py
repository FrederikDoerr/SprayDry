#!/usr/bin/env python2

'''
Created Sep - Nov 2019
DataLogger XS60002S
@author: Frederik Doerr (CMAC, frederik.doerr@strath.ac.uk, GitHub: https://github.com/frederik-d)

Setup:
Find Ard: ls -l /dev/ttyUSB*
Enable USB: sudo chmod 666 /dev/ttyUSB1

Path: /home/pi/B290_XS_RS232_Data/XS_RS232_DataLogger.py

Make shell excecutable:
sudo chmod +x /home/pi/Desktop/DataLogger_XS_RS232_autorun.sh

Minimum Working Example:

import os
import time
import datetime
import serial

DL_Port = '/dev/ttyUSB1'
DL_file_path = '/home/pi/B290_XS_RS232_Data'

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
file_name ='Data_SprayDry_XS_RS232_' + st + '.txt'

file_Sensor_DataLog = open(os.path.join(DL_file_path,file_name),'a',0)
print 'SprayDry_XS_RS232_DataLogger\n' + 'StartTime: ' + st + ':\n'

while True:
	ser = serial.Serial(DL_Port, 9600)
	time.sleep(0.75)
	value_string = ser.readline()
	time.sleep(0.5)
	value_string = ser.readline()
        ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')     
	file_Sensor_DataLog.write(st + ';' + value_string)                
	print st + '\t' + value_string
	ser.close()
	time.sleep(0.75)

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
        self.DL_Port = '/dev/ttyUSB1'
        self.DL_file_path = '/home/pi/B290_XS_RS232_Data'

    def ensure_dir(self):
        if not os.path.exists(self.DL_file_path):
            os.makedirs(self.DL_file_path)
            
    def createDataFile(self,file_path,file_name):
        self.file_ID = open(os.path.join(file_path,file_name),'a',0)
        self.file_ID.write('SprayDry XS_RS232 DataLogger\n')
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
        self.file_ID.write('StartTime: ' + st + ':\n')
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
	file_name ='Data_SprayDry_XS_RS232_' + st + '.txt'
        value_string = ''
        ser_Check = False
        print 'Initiate Logging'
        while True:
		if not os.path.isfile(os.path.join(self.DL_file_path,file_name)):
	    		file_Sensor_DataLog = self.createDataFile(self.DL_file_path,file_name)
            		print 'SprayDry_XS_RS232_DataLogger\n' + 'StartTime: ' + st + ':\n'
		ser = serial.Serial(self.DL_Port, 9600)
		time.sleep(0.75)
		value_string = ser.readline()
		time.sleep(0.5)
		value_string = ser.readline()
        	ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')     
		file_Sensor_DataLog.write(st + ';' + value_string)                
		print st + '\t' + value_string
		ser.close()
		time.sleep(0.75)
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

def varExist(var):
    try:
        var
    except NameError:
        return False
    else:
        return True


if __name__ == '__main__': 
    multiprocessing.log_to_stderr()
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    dl = DataLogger()
    p2 = Process(target=DataLogger().run_DataLogger())
    p2.start()


