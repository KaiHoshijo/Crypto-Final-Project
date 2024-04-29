from numpy import genfromtxt
import numpy as np
import os

def get_traces():
    traces = np.array([]) # Array of all the traces
    try:
        # Load the traces if they already exist
        traces = np.load('analysis/traces.npz')
        traces = traces[traces.files[0]]
    except FileNotFoundError:
        # If the traces don't already exist, load them
        for wavename in os.listdir('waveforms'):
            data = genfromtxt(f'waveforms/{wavename}', delimiter = ',')
            # First two rows are name columns
            traces = np.append(traces, data[2:10])
        # Save the traces so that this expensive operation doesn't occur often
        np.savez('analysis/traces.npz', traces)
    return traces