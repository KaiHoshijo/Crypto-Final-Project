# http://wiki.newae.com/Correlation_Power_Analysis
# http://cryptography.gmu.edu/documentation/fobos/cpa.html
import math


def correlation(subkey_i, voltage_j, power_estimates_h, power_traces_t):
    """
    subkey_i: the subkey
    voltage_j: the measured voltage
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
