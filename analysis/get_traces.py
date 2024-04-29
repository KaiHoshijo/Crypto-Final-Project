from numpy import genfromtxt
import numpy as np
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
