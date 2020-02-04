'''
    Based on PyDmx made by YoshiRi
    https://github.com/YoshiRi/PyDMX
'''
import serial
import time
import numpy as np
import threading


class Dmx(threading.Thread):
    def __init__(self,COM='COM3',Brate=250000,Bsize=8,StopB=2,sleepms=50,breakus=176,MABus=16,frequency=100,debug=False,**kargs):
        super().__init__(**kargs)
        #start serial
        self.ser = serial.Serial(COM,baudrate=Brate,bytesize=Bsize,stopbits=StopB)
        self.data = np.zeros([513],dtype='uint8')
        self.data[0] = 0 # StartCode
        self.sleepms = sleepms
        self.breakus = breakus
        self.MABus = MABus
        self.sleepcycle = 1/frequency #frequency given in hz, stored in ms
        self.runSemaphore = True
        self.debug = debug
        
    def set_random_data(self):
        self.data[1:513]= np.random.rand(512)*255

    def set_data(self,id,data):
        self.data[id]=data

    def send(self):
        # Send Break : 88us - 1s
        self.ser.break_condition = True
        time.sleep(self.breakus/1000000.0)
        
        # Send MAB : 8us - 1s
        self.ser.break_condition = False
        time.sleep(self.MABus/1000000.0)
        
        # Send Data
        #print(bytearray(self.data))
        self.ser.write(bytearray(self.data))
        
        # Sleep
        time.sleep(self.sleepms/1000.0) # between 0 - 1 sec

    def sendzero(self):
        self.data = np.zeros([513],dtype='uint8')
        self.send()

    def run(self):
        while self.runSemaphore:
            if self.debug: print('DMX-Cycle')
            self.send()
            time.sleep(self.sleepcycle)
        self.sendzero()
    
    def stop(self):
        self.runSemaphore = False

    def __del__(self):
        print('Close serial server!')
        self.sendzero()
        self.ser.close()


if __name__ == '__main__':
    dmx = Dmx('COM3',daemon=True)
    dmx.start()
    for i in range(0,10):
        dmx.set_data(1,255)
        #dmx.send()
        time.sleep(0.2)
        dmx.set_data(1,0)
        #dmx.send()
        time.sleep(0.2)
    del dmx
