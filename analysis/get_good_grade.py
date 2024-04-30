import concurrent.futures
import multiprocessing
import time

import numpy

import get_traces, get_analysis, get_inter_vals


def find_subkey(i: int, plaintexts: [], power_traces: [], subkeys: [], iv: [] = None):
    sub_plaintexts = plaintexts[i]

    if iv:
        iv_subset = iv[i]
        for j, plaintext in enumerate(sub_plaintexts):
            sub_plaintexts[j] = plaintext ^ iv_subset

    # 2. Calculate intermediate values for all d (plaintext block) and k (subkey) combinations
    # tried to follow step 3 in the article
    all_inter_vals = get_inter_vals.calculate_inter_vals(sub_plaintexts, subkeys)

    # 3. Build power model h by calculating Hamming Weight for each intermediate value
    power_estimates = get_analysis.estimate_all_powers(all_inter_vals)

    # 4. Calculate correlation between power model h and traces t. Get subkey from the highest correlation.
    subkey, r = get_analysis.pick_subkey(power_estimates, power_traces, subkeys)

    print(f"{i}: subkey is {hex(subkey)} ({r})")

    return i, subkey, r


def find_key_multithreaded():
    time_started = time.time()
    print(f"Time started: {time_started}")
    key = [0 for i in range(16)]

    # 1. Read traces t
    power_traces = get_traces.get_traces()

    plaintexts = get_traces.get_split_plaintexts()
    # plaintexts = get_traces.get_split_ciphertexts()
    subkeys = get_analysis.gen_subkeys()

    num_cores = multiprocessing.cpu_count()

    print(f"Starting analysis with {num_cores} threads...")
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_cores) as executor:
        args = []
        for i in range(16):
            args.append((i, plaintexts, power_traces, subkeys))

        futures = [executor.submit(find_subkey, *args) for args in args]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    corrs = []
    for tup in results:
        i, subkey, r = tup
        key[i] = subkey
        corrs.append(r)

    hex_string_key = [hex(i) for i in key]
    hex_string_key = [i[2:] for i in hex_string_key]
    print(f"\nKey: 0x{''.join(hex_string_key)}")
    print(f"Correlations: {corrs}")

    time_ended = time.time()
    print(f"Time ended: {time_ended}")
    print(f"Time delta: {time_ended - time_started} seconds")


def find_subkey_multithreaded(subset_i: int):
    """
    This finds the key for a subset of the plaintexts/subkeys.
    For example, if you pass in 0, it will guess the first
    byte of the key. If you pass in 5, it'll guess the 4th.
    And so on. It multithreads this by splitting up the subkeys
    by CPU core; other than that it's pretty much the same
    as do_stuff().
    """
    time_started = time.time()
    print(f"Time started: {time_started}")

    iv = get_traces.get_iv()

    # 1. Read traces t
    power_traces = get_traces.get_traces()

    plaintexts = get_traces.get_split_plaintexts()
    # plaintexts = get_traces.get_split_ciphertexts()
    subkeys = get_analysis.gen_subkeys()

    num_cores = multiprocessing.cpu_count()
    subkey_chunks = [i.astype(int) for i in numpy.array_split(subkeys, num_cores)]

    print(f"Starting analysis with {num_cores} threads...")
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_cores) as executor:
        args = []
        for i in range(num_cores):
            args.append((subset_i, plaintexts, power_traces, subkey_chunks[i], iv))

        futures = [executor.submit(find_subkey, *args) for args in args]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    max_i = -1
    max_key = -1
    max_r = -1
    for tup in results:
        i, subkey, r = tup
        if r > max_r:
            max_i = i
            max_key = subkey
            max_r = r

    print(f"\nKey: {hex(max_key)} ({max_r})")

    time_ended = time.time()
    print(f"Time ended: {time_ended}")
    print(f"Time delta: {time_ended - time_started} seconds")


if __name__ == '__main__':
    # find_key_multithreaded()
    find_subkey_multithreaded(0)
