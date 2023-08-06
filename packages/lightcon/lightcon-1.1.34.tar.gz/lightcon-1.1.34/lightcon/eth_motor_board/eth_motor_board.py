# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 16:09:38 2019

@author: butkus

TO MAKE EVERYTHING WORK:
    1. Configure ethernet adapter to use static IP address 10.1.1.x, where x is anything from 1 to 255
    2. Run commands from http://nova/display/HAR/EthMotorBoard    
"""

import socket
import time

class EthMotorBoard:
    BUFFER_SIZE = 1024
    sock = None
    connected = False
    name = None
    timeout = 100
    fv = None
    ip_address = None
    max_position = 2**21-1
    status_registers = [(0x01,0x01,'HiZ'), (0x02,0x0,'BUSY'), (0x04,0x04, 'SW_F'), (0x08,0x08,'SW_ENV'), #(0x10, 0x10,'DIR'), 
                        (0x60,0x00,'Stopped'), (0x60,0x20,'Acceleration'), (0x60,0x40,'Deceleration'), (0x60,0x60,'Constant speed'), (0x80,0x80,'NOTPERF_CMD'),
                        (0x100,0x100,'WRONG_CMD'), (0x200,0x0,'OVLO'), (0x400,0x0,'TH_WRN'),(0x800,0x0,'TH_SD'),
                        (0x1000,0x0,'OCD'), (0x2000,0x0,'STEP_LOSS_A'), (0x4000,0x0,'STEP_LOSS_B'), (0x8000,0x8000,'SCK_MOD')]    
    ls_registers = [(0x01,0x01,'Left LS reached'), (0x02,0x02,'Right LS reached')]
    def __init__ (self, ip_address='10.1.1.0'):
        self.ip_address = ip_address           
                    
        self.name = self.send('GET BOARD_NAME')
        self.fv = self.send('FIRMWARE_VERSION')
        
        self.connected = self.fv != None
        
        if self.connected:
            print ('Successfullly connected to {:} (firmware version: {:})'.format(self.name, self.fv))
        else:
            print ('Motor board not found at {:}'.format(self.ip_address))
        
    def send(self, message, args=None):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(self.timeout/1000)
            self.sock.connect((self.ip_address, 80))            
            if args is None:
                self.sock.send((str(message)+'\r\n').encode('UTF-8'))
            else:
                self.sock.send((str(message)+' '+' '.join([str(arg) for arg in args])+'\r\n').encode('UTF-8'))
            data = self.sock.recv(self.BUFFER_SIZE)
            self.sock.close()        
            return data[:-2].decode()
        except socket.timeout:
            return None
    def get_status(self, motor_index):
        status = int(self.send('GET STATUS', [motor_index]))
        ls_status = eval(self.send('GET LIMIT_SWITCH', [motor_index]))['Logical']
        return [stat for mask, val, stat in self.status_registers if status & mask == val] + [stat for mask, val, stat in self.ls_registers if ls_status & mask == val]   
                
    def wait_until_stopped(self, motor_index):
        repeat = True
        while repeat:
            repeat = int(self.send('GET STATUS ' + str(motor_index))) & 0x60 != 0
            time.sleep(0.05)    
