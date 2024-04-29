from analysis import get_traces, get_inter_vals, get_analysis


def do_stuff():
    # 1. Read traces t
    power_traces = get_traces.get_traces()

    # 2. Calculate intermediate values for all d (plaintext block) and k (subkey) combinations
    # tried to follow step 3 in the article, where the plaintext and subkeys coming from?
    plaintexts = get_traces.get_plaintexts()  # TODO: Read plaintexts from waveforms.txt
    subkeys = get_analysis.gen_subkeys()
    all_inter_vals = get_inter_vals.calculate_inter_vals(plaintexts, subkeys)

    # 3. Build power model h by calculating Hamming Weight for each intermediate value
    power_estimates = get_analysis.calc_all_hamming(all_inter_vals)

    # 4. Calculate correlation between power model h and traces t. Get subkey from the highest correlation.
    subkey_index = get_analysis.pick_subkey(power_estimates, power_traces)
    subkey = subkeys[subkey_index]

    # 5. Somehow get from a subkey to the entire key?
    "what"

    pass


if __name__ == '__main__':
    do_stuff()
