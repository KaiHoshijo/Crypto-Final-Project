# http://wiki.newae.com/Correlation_Power_Analysis
# http://cryptography.gmu.edu/documentation/fobos/cpa.html
import math

import numpy

invSbox = [
    [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
    [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
    [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
    [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
    [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
    [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
    [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
    [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
    [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
    [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
    [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
    [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
    [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
    [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
    [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
]


def hamming_weight(val: int) -> int:
    """
    val: the value to have its hamming weight calculated for

    Hamming Weight is the number of ones that a value contains
    """
    weight = 0
    while val != 0:
        weight += (val & 1)  # check if lowest bit is one
        val >>= 1  # Shift down by 1
    return weight


def estimate_all_powers(inter_vals: []) -> []:
    """
    inter_vals: array of calculated intermediate values: d (plaintext block) by k (subkey)
    hamming_weights: array to hold all hamming weights for inter_vals
    
    Calculates Hamming weights for intermediate values, returning
    the power estimation array.
    """
    hamming_weights = numpy.empty((len(inter_vals), len(inter_vals[0])))
    for i, outer in enumerate(inter_vals):
        for j, inner in enumerate(outer):
            weight = hamming_weight(inner)
            hamming_weights[i][j] = weight

    return hamming_weights.astype(int)


def calc_intermediate(ciphertext: int, subkey_guess: int) -> int:
    """
    ciphertext: The ciphertext to make the power estimate with
    guess: The guessed subkey for the current power trace

    Calculate the intermediate value from InvSubBytes(ciphertext XOR guessed key)
    """
    # Calculate the inverse sub bytes
    xored = ciphertext ^ subkey_guess
    inv = invSbox[(xored & 0xf0) >> 4][xored & 0x0f]
    return inv


def calc_intermediate_forward(plaintext: int, subkey_guess: int) -> int:
    """
    plaintext: The plaintext to make the power estimate with
    guess: The guessed subkey for the current power trace

    Calculate the intermediate value from SubBytes(plaintext XOR guessed key)
    """
    s_box = [["63", "7c", "77", "7b", "f2", "6b", "6f", "c5", "30", "01", "67", "2b", "fe", "d7", "ab", "76"],
             ["ca", "82", "c9", "7d", "fa", "59", "47", "f0", "ad", "d4", "a2", "af", "9c", "a4", "72", "c0"],
             ["b7", "fd", "93", "26", "36", "3f", "f7", "cc", "34", "a5", "e5", "f1", "71", "d8", "31", "15"],
             ["04", "c7", "23", "c3", "18", "96", "05", "9a", "07", "12", "80", "e2", "eb", "27", "b2", "75"],
             ["09", "83", "2c", "1a", "1b", "6e", "5a", "a0", "52", "3b", "d6", "b3", "29", "e3", "2f", "84"],
             ["53", "d1", "00", "ed", "20", "fc", "b1", "5b", "6a", "cb", "be", "39", "4a", "4c", "58", "cf"],
             ["d0", "ef", "aa", "fb", "43", "4d", "33", "85", "45", "f9", "02", "7f", "50", "3c", "9f", "a8"],
             ["51", "a3", "40", "8f", "92", "9d", "38", "f5", "bc", "b6", "da", "21", "10", "ff", "f3", "d2"],
             ["cd", "0c", "13", "ec", "5f", "97", "44", "17", "c4", "a7", "7e", "3d", "64", "5d", "19", "73"],
             ["60", "81", "4f", "dc", "22", "2a", "90", "88", "46", "ee", "b8", "14", "de", "5e", "0b", "db"],
             ["e0", "32", "3a", "0a", "49", "06", "24", "5c", "c2", "d3", "ac", "62", "91", "95", "e4", "79"],
             ["e7", "c8", "37", "6d", "8d", "d5", "4e", "a9", "6c", "56", "f4", "ea", "65", "7a", "ae", "08"],
             ["ba", "78", "25", "2e", "1c", "a6", "b4", "c6", "e8", "dd", "74", "1f", "4b", "bd", "8b", "8a"],
             ["70", "3e", "b5", "66", "48", "03", "f6", "0e", "61", "35", "57", "b9", "86", "c1", "1d", "9e"],
             ["e1", "f8", "98", "11", "69", "d9", "8e", "94", "9b", "1e", "87", "e9", "ce", "55", "28", "df"],
             ["8c", "a1", "89", "0d", "bf", "e6", "42", "68", "41", "99", "2d", "0f", "b0", "54", "bb", "16"]]
    xored = plaintext ^ subkey_guess
    hex_xored = hex(xored)[2:]
    if len(hex_xored) == 1:
        hex_xored = "0" + hex_xored
    interm = s_box[int(hex_xored[0], 16)][int(hex_xored[1], 16)]
    return int(interm, 16)


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
        s1 += power_estimates_h[d_iter][subkey_i] * power_traces_t[d_iter][voltage_j][1]
        sum_hdi += power_estimates_h[d_iter][subkey_i]
        sum_tdj += power_traces_t[d_iter][voltage_j][1]
        sum_hdi_sqr += power_estimates_h[d_iter][subkey_i] * power_estimates_h[d_iter][subkey_i]
        sum_tdj_sqr += power_traces_t[d_iter][voltage_j][1] * power_traces_t[d_iter][voltage_j][1]
    numerator = (D * s1) - (sum_hdi * sum_tdj)

    # Denominator
    s2 = (sum_hdi * sum_hdi) - (D * sum_hdi_sqr)
    s3 = (sum_tdj * sum_tdj) - (D * sum_tdj_sqr)
    denominator = math.sqrt(s2 * s3)

    return numerator / denominator


def gen_subkeys() -> []:
    return [i for i in range(0, 256)]


def pick_subkey(power_estimates: [], power_traces: [], subkeys: []) -> (int, int):
    """
    Find the highest r_i to get the subkey.
    Returns the chosen subkey and its abs(correlation)
    """
    max_i = -1
    max_j = -1
    max_r = -1
    for i in range(len(subkeys)):
        for j in range(1999):
            r = abs(correlation(i, j, power_estimates, power_traces))
            if r > max_r:
                max_i = i
                max_j = j
                max_r = r
    return subkeys[max_i], max_r
