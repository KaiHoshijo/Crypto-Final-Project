# http://cryptography.gmu.edu/documentation/fobos/cpa.html

# not really sure where you guys wanna pull the plaintexts and subkeys from
# unless i'm just blind and haven't seen them yet

def calculate_inter_vals(plaintexts, subkeys):
    """
    Wanna go through all combinations of the the plaintexts (d) and subkeys (k) combos
    
    plaintexts (d): gonna assume we have them in a list or something
    subkeys (k): also gonna assume we have them in a list or something
    
    I'll follow step 3 in the article above
    """
    num_d = len(plaintexts)
    num_k = len(subkeys)
    V = [[0 for i in range(num_k)] for j in range(num_d)] # D x K matrix
    
    # calculate intermdiate value f(d, k) for all combos of d and k
    for i in range(num_d):
        for j in range(num_k):
            V[i][j] = calculate_val(plaintexts[i], subkeys[j])
    
    # so each col in V is intermediate value calcualted for all d for one key
    return V

def calculate_val(plaintext, subkey):
    """
    calculate the specific intermediate value for the specified combo of plaintext and subkey
    
    is there a specific function we have to use here?
    
    using XOR as a placeholder?
    """
    
    val = plaintext ^ subkey
    
    return val
    
    