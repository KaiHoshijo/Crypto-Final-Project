from numpy import genfromtxt
import numpy as np
import binascii
import os

def get_traces():
    try:
        # Load the traces if they already exist
        traces = np.load('analysis/traces.npz')
        traces = traces[traces.files[0]]
    except FileNotFoundError:
        traces = np.empty(shape=(2000, 2000, 2))  # Array of all the traces
        i = 0
        # If the traces don't already exist, load them
        for wavename in os.listdir('waveforms'):
            # First two rows are name columns
            data = genfromtxt(f'waveforms/{wavename}', delimiter=',')[2:]
            # TODO: delete time column because we only need voltage
            #       numpy.delete(data, 0, 1)
            traces[i] = data
            i += 1
        # Save the traces so that this expensive operation doesn't occur often
        np.savez('analysis/traces.npz', traces)
    return traces

def fix_bytes(hexstring: list) -> bytes:
    """
    hexstring: The string to fix any bytes within the string passed

    All the single-bytes need to have a zero put in front of it
    In addition, the string is turned into a byte string
    """
    updated = []
    for hex in hexstring:
        # Update single bytes
        if len(hex) == 1:
            hex = '0' + hex
        updated.append(hex)    
    updated = ''.join(updated)
    # Convert str list to hexadecimal bytes
    return binascii.unhexlify(bytes(updated.encode()))

def get_waveform():
    """
    The structure of the waveforms.txt is the following:
        Key Value
        IV Value
        W#.csv
        Input Value
        Output Value
        Repeats the previous three values
    """
    # Structure is the above in the waveform
    data = {}
    with open("waveforms.txt", "r") as f:
        lines = f.readlines()
        # First two lines are key and iv
        key = lines[0].split(' ')

        data[key[0].lower] = fix_bytes(key[1].split(' '))
        iv = lines[1].split(' ')
        data[iv[0].lower] = fix_bytes(iv[1].split(' '))
        # Rest are the waveform file with the input and output
        for index in range(2, len(data), 2):
            filename = data[index]
            # The two values after the filename are the plaitext and ciphertext
            plaintext = data[index + 1].split(' ')
            # Converting the plaintext to hex
            plaintext = fix_bytes(plaintext[1].split(' '))
            ciphertext = data[index + 2].split(' ')
            # Converting the ciphertext to hex
            ciphertext = fix_bytes(ciphertext[1].split(' '))
            data[filename] = [plaintext, ciphertext]
    return data