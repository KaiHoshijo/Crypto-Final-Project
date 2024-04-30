# http://cryptography.gmu.edu/documentation/fobos/cpa.html
import numpy

import get_analysis


def calculate_inter_vals(plaintexts: [], subkeys: []) -> []:
    """
    Wanna go through all combinations of the plaintexts (d) and subkeys (k) combos
    
    plaintexts (d): gonna assume we have them in a list or something
    subkeys (k): also gonna assume we have them in a list or something
    
    I'll follow step 3 in the article above
    
    V needs to be ints right? Does this do that or..?
    
    """
    num_d = len(plaintexts)
    num_k = len(subkeys)
    V = numpy.zeros((num_d, num_k))

    # calculate intermediate value f(d, k) for all combos of d and k
    for i in range(num_d):
        for j in range(num_k):
            V[i][j] = get_analysis.calc_intermediate(plaintexts[i], subkeys[j])

    # so each col in V is intermediate value calculated for all d for one key
    return V.astype(int)
