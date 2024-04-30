import get_traces, get_analysis, get_inter_vals


def do_stuff():
    key = []

    # 1. Read traces t
    power_traces = get_traces.get_traces()

    plaintexts = get_traces.get_split_plaintexts()
    subkeys = get_analysis.gen_subkeys()

    for i in range(16):
        sub_plaintexts = plaintexts[i]

        # 2. Calculate intermediate values for all d (plaintext block) and k (subkey) combinations
        # tried to follow step 3 in the article
        all_inter_vals = get_inter_vals.calculate_inter_vals(sub_plaintexts, subkeys)

        # 3. Build power model h by calculating Hamming Weight for each intermediate value
        power_estimates = get_analysis.estimate_all_powers(all_inter_vals)

        # 4. Calculate correlation between power model h and traces t. Get subkey from the highest correlation.
        subkey_index = get_analysis.pick_subkey(power_estimates, power_traces)
        chosen_subkey = subkeys[subkey_index]
        key.append(chosen_subkey)
        print(f"Subkey: {hex(chosen_subkey)}")

    hex_string_key = [hex(i) for i in key]
    hex_string_key = [i[2:] for i in hex_string_key]
    print(f"Key: 0x{''.join(hex_string_key)}")


if __name__ == '__main__':
    do_stuff()
