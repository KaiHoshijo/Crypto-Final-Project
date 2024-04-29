import pyvisa
import time
import numpy as np
import serial
import os

'''
The configurations of the Keysight InfiniiVision MSOX3012T Oscilloscope is
as follows:

Channel 1: 5 (V/div)
Channel 2: 50m (V/div)
Period (s): 1 u
Trigger Mode: Edge
Trigger Source: 1
Trigger Type: Rising
'''

INTERVAL = 0.5
TIMEOUT = 100000
WAVEFORM = 1000
PORT = 'COM7'

rm = pyvisa.ResourceManager()
# Open the oscilloscope resource
instr = rm.open_resource(rm.list_resources()[0])
instr.timeout = TIMEOUT 
ser = serial.Serial(port = PORT, baudrate = 9600, parity=serial.PARITY_ODD,
                    stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)

IDN = instr.query('*IDN?')
print(IDN.strip())

def init():
    # Reset the board
    instr.query('*RST; *OPC?')
    # Configure the first channel
    instr.write(':CHANnel1:DISPlay ON')
    instr.write(':CHANnel2:DISPlay ON')
    instr.write(':CHANnel1:SCALe 5')
    instr.write(':CHANnel1:OFFSet -10')
    # Configure the second channel
    instr.write(':CHANnel2:SCALe .05')
    instr.write(':CHANnel2:OFFSet .05')
    # Configure horizontal scale and offset
    instr.write(':TIMebase:SCALe 0.000001')
    instr.write(':TIMebase:POSition 0')
    # Set the trigger mode
    instr.write(':TRIGger:MODE EDGE')
    # Set the source for the trigger
    instr.write(':TRIGger:EDGE SOURce CHANnel1')
    # Set the threshold for the trigger
    instr.write(':TRIGger:EDGE:LEVel 2.5V')
    # Set the waveform format
    instr.write(':SAVE:WAVeform:FORMat CSV')
    # instr.write(':SAVE:WAVeform:LENGth 1000')

def read_serial():
    out = ''
    while ser.inWaiting() > 0:
        a = ser.read(1).decode()
        if a != '\r':
            out += a
    return out


# Initialize the oscope
init()
print(f'Capturing this number of waveforms: {WAVEFORM}')
# Get the latest file name from waveforms
i = 0
with open("waveforms.txt", "r") as f:
    lines = f.readlines()
    if len(lines) != 0:
        for i in range(len(lines) - 1, -1, -1):
            line = lines[i]
            if '.csv' in line:
                i = int(line[1:].split('.csv')[0]) + 1
                break
print(i)
# Get the key and the iv from the arduino
output = read_serial()
if i != 0: # Only get key and iv if values haven't been retrieved already
    output = ''
print(output)
instr.write('*ESE 255')
# Start the serial by writing to it
try:
    while i < WAVEFORM:
        # Send the command to run
        ser.write(b'1')
        # Turn the display for channel 1 on after turning it off for the image
        instr.write(':CHANnel1:DISPlay ON')
        # Wait for one trigger
        instr.write('*CLS;:SINGle')
        # Wait until the encryption happens before running next code block
        triggered = 0
        while triggered == 0:  # Poll the scope until it returns a 1
            triggered = int(instr.query(':TER?'))
            time.sleep(INTERVAL)  # Pause to prevent excessive queries
        # Name the file to be saved
        filename = f'W{i}'
        i += 1
        # Turn off channel 1 so its data doesn't conflict the power analysis
        instr.write(':CHANnel1:DISPlay OFF')
        # Set the file name and the file type
        instr.write(f':SAVE:FILename "{filename}"')
        instr.write(':SAVE:WAVeform:FORMat CSV')
        # Run continuously if there is an error so that I can fix it
        num = ''
        while num != '0':
            # Try to write to usb first
            instr.write(f':SAVE:WAVeform "/usb/{filename}.csv"')
            res = instr.query('*OPC?')
            num,msg = instr.query(':SYSTem:ERRor?').split(',')
            # If there is an error, try writing to usb2
            if '257' in num:
                instr.write(f':SAVE:WAVeform "/usb2/{filename}.csv"')
                res = instr.query('*OPC?')
                num,msg = instr.query(':SYSTem:ERRor?').split(',')
            # Print the error output
            num = num[1:] # should be zero if nothing went wrong
            if num != '0':
                print(msg.strip())
            print(instr.query('*ESR?').strip())
            time.sleep(1) # Wait for one second to not overwhelm the oscope
        # Get the plaintext and the first round encryption
        output += f'{filename}.csv\n'
        print(filename)
        output += read_serial()
    print(f'Captured this number of of waveforms: {WAVEFORM}')
finally:
    with open('waveforms.txt', 'a') as f:
        f.write(output)