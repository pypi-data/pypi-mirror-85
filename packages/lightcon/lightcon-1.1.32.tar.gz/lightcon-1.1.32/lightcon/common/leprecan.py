# -*- coding: utf-8 -*-
"""
Created on Thu May 18 17:45:11 2017

@author: butkus
"""
import numpy
from enum import Enum, IntEnum

class FrameType(IntEnum):
    BroadcastFrame = 0
    SetRegisterResponseFrame = 1
    GetRegisterResponseFrame = 2
    OutgoingIfuFrame = 3
    SetRegisterCommandFrame = 5
    GetRegisterCommandFrame = 6
    IncomingRawFrame = 7
    Invalid = 255
    
class ResponseStatus(IntEnum) :
    Success =                   0x00,
    UnsupportedCommand =        0x01,
    InvalidRegisterAddress =    0x02,
    InvalidIndex =              0x03,
    TypeError =                 0x04,
    DecryptionFailed =          0x05,
    InsufficientAccessLevel =   0x08,
    UnknownError2 =             0xef,
    UnknownError =              0xff

def iterate_crc_8byte(seed, newByte):
    data = numpy.uint8(seed ^ newByte);
    for i in range(8):
        if ((data & 0x80) != 0):
            data <<= 1;
            data ^= 0x07;
        else:
            data <<= 1;    
    return numpy.uint8(data);


def prepare_frame(data):
    indexes = [0, 1, 2, 4, 5, 6, 7]
    
    crc = iterate_crc_8byte (0xff, data[0]);    
    
    for index in indexes[1:]:
        crc = iterate_crc_8byte (crc, data[index])
        
    data[3] = crc;
    return data
    
def get_data_string (data):
    return ' '.join(["{0:#0{1}x}".format(cell,4)[2:] for cell in data])

def generate_message_id (baseId, frameType):
    return baseId + frameType.value

def generate_data_frame (frameType, registerAddress, index, flags=0x00, data4bytes=0x00000000):
    data = [0] * 8              
    
    if (frameType == FrameType.GetRegisterCommandFrame):
        data = prepare_frame([
                registerAddress & 0x00ff,
                registerAddress & 0xff00,
                index,
                0x00, # will be replaced by crc
                data4bytes & 0x000000ff,
                (data4bytes & 0x0000ff00) >> 8,
                (data4bytes & 0x00ff0000) >> 16,
                (data4bytes & 0xff000000) >> 24
                ]);     
    
    if (frameType == FrameType.SetRegisterCommandFrame):
        data = prepare_frame([
                registerAddress & 0x00ff,
                registerAddress & 0xff00,
                index,
                0x00, # will be replaced by crc
                data4bytes & 0x000000ff,
                (data4bytes & 0x0000ff00) >> 8,
                (data4bytes & 0x00ff0000) >> 16,
                (data4bytes & 0xff000000) >> 24
                ]);   

    return data        