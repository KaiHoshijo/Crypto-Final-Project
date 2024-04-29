# http://wiki.newae.com/Correlation_Power_Analysis
# http://cryptography.gmu.edu/documentation/fobos/cpa.html
import math

def hamming_weight(val: int):
    """
    val: the value to to have its hamming weight calculated for

    Hamming Weight is the number of ones that a value contains
    """
    weight = 0
    while val != 0:
        weight += (val & 1) # check if lowest bit is one
        val >>= 1 # Shift down by 1
    return weight

def correlation(subkey_i: int, voltage_j: int, power_estimates_h: [], power_traces_t: []) -> float:
    """
    Get Pearson correlation coefficient for a given subkey and voltage measurement
    Returns [-1, 1] idk i'm not a stats nerd

    subkey_i: the subkey index
    voltage_j: the measured voltage index (for the trace)
    power_estimates_h: power consumption models, D plaintexts by I subkeys
        power_estimates_h[d][i] refers to power estimate for trace d and subkey i
    power_traces_t: D power traces, each with T data points
        power_traces_t[d][j] refers to point j in trace d
   """
    D = len(power_traces_t)

    # Numerator
    s1 = 0
    sum_hdi = 0
    sum_hdi_sqr = 0
    sum_tdj = 0
    sum_tdj_sqr = 0
    for d_iter in range(D):
        s1 += power_estimates_h[d_iter][subkey_i] * power_traces_t[d_iter][voltage_j]
        sum_hdi += power_estimates_h[d_iter][subkey_i]
        sum_tdj += power_traces_t[d_iter][voltage_j]
        sum_hdi_sqr += power_estimates_h[d_iter][subkey_i] * power_estimates_h[d_iter][subkey_i]
        sum_tdj_sqr += power_traces_t[d_iter][voltage_j] * power_traces_t[d_iter][voltage_j]
    numerator = (D * s1) - (sum_hdi * sum_tdj)

    # Denominator
    s2 = (sum_hdi * sum_hdi) - (D * sum_hdi_sqr)
    s3 = (sum_tdj * sum_tdj) - (D * sum_tdj_sqr)
    denominator = math.sqrt(s2 * s3)

    return numerator / denominator


def gen_subkeys() -> []:
    return [i for i in range(0, 256)]


def pick_subkey(power_estimates: [], power_traces: []) -> int:
    """
    Find the highest r_i to get the subkey.
    Returns the chosen subkey index
    """
    all_subkeys = gen_subkeys()
    max_i = -1
    max_j = -1
    max_r = -1
    for i in range(all_subkeys):
        for j in range(2000):
            r = abs(correlation(i, j, power_estimates, power_traces))
            if r > max_r:
                max_i = i
                max_j = j
                max_r = r
    return max_i
