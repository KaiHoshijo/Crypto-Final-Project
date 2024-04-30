import concurrent.futures
import multiprocessing

import get_traces, get_analysis, get_inter_vals


def run_for_section(i: int, plaintexts: [], power_traces: [], subkeys: []):
    sub_plaintexts = plaintexts[i]
    print(f"{i}: got plaintexts")

    # 2. Calculate intermediate values for all d (plaintext block) and k (subkey) combinations
    # tried to follow step 3 in the article
    all_inter_vals = get_inter_vals.calculate_inter_vals(sub_plaintexts, subkeys)
    print(f"{i}: calculated intermediate values")

    # 3. Build power model h by calculating Hamming Weight for each intermediate value
    power_estimates = get_analysis.estimate_all_powers(all_inter_vals)
    print(f"{i}: built power estimates")

    # 4. Calculate correlation between power model h and traces t. Get subkey from the highest correlation.
    print(f"{i}: starting correlation...")
    subkey_index = get_analysis.pick_subkey(power_estimates, power_traces)

    chosen_subkey = subkeys[subkey_index]
    print(f"{i}: subkey is {hex(chosen_subkey)}")

    return i, chosen_subkey


def do_stuff():
    key = [0 for i in range(16)]

    # 1. Read traces t
    power_traces = get_traces.get_traces()

    plaintexts = get_traces.get_split_plaintexts()
    subkeys = get_analysis.gen_subkeys()

    # Setup multithreading:
    # Get the number of CPU cores on your computer
    num_cores = multiprocessing.cpu_count()

    print(f"Starting analysis with {num_cores} threads...")
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_cores) as executor:
        args = []
        for i in range(16):
            args.append((i, plaintexts, power_traces, subkeys))

        futures = [executor.submit(run_for_section, *args) for args in args]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

    for tup in results:
        i, subkey = tup
        key[i] = subkey

    hex_string_key = [hex(i) for i in key]
    hex_string_key = [i[2:] for i in hex_string_key]
    print(f"Key: 0x{''.join(hex_string_key)}")


if __name__ == '__main__':
    do_stuff()
