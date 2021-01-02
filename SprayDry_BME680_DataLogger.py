#!/usr/bin/env python2

'''
Created Sep - Nov 2019
DataLogger BME680
@author: Frederik Doerr (CMAC, frederik.doerr@strath.ac.uk, GitHub: https://github.com/frederik-d)

Setup:
Find Ard: ls -l /dev/ttyUSB*
Enable USB: sudo chmod 666 /dev/ttyUSB0
sudo chmod 666 /dev/ttyACM0

Path: /home/pi/B290_BME680_Data/SprayDry_BME680_DataLogger.py
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
        self.DL_Port = '/dev/ttyACM0'
        self.DL_file_path = '/home/pi/B290_BME680_Data'

    def ensure_dir(self):
        if not os.path.exists(self.DL_file_path):
            os.makedirs(self.DL_file_path)
            
    def createDataFile(self,file_path,file_name):
        self.file_ID = open(os.path.join(file_path,file_name),'a',0)
        self.file_ID.write('SprayDry BME680 DataLogger\n')
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
        delay_time = 3; # time between readings in seconds
        self.ensure_dir()
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
	file_name ='Data_SprayDry_BME680_' + st + '.txt'
        current_time = 0;
        ser_Check = False
        print 'Initiate Logging'
        while True:
            if portIsUsable(self.DL_Port) and not ser_Check: #can only be read once!
                ser = serial.Serial(self.DL_Port, 9600)
                ser_Check = True
                print 'Serial connected'
            if ser_Check:
                if not os.path.isfile(os.path.join(self.DL_file_path,file_name)):
                    file_Sensor_DataLog = self.createDataFile(self.DL_file_path,file_name)
                    print 'SprayDry_BME680_DataLogger\n' + 'StartTime: ' + st + ':\n'
                ser              
                value = ser.read()
                value_string = ''
                while value.lower() != '\n':
                    value_string += value
                    value = ser.read()
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
		if current_time > 6:                
			file_Sensor_DataLog.write(st + ';' + value_string + '\n')
                	print st + '\t' + value_string
            time.sleep(delay_time)
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


