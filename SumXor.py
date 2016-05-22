import sys
import time
# Sum and Xor:
# Assume there are two positive integers a and b that have sum s and XOR x.
# Given an s on the range [2, 1012] and x on the range [0, 1012],
# find a list of possible values of the ordered pairs (a, b). For instance,
# given s = 9 and x = 5, there are four possible pairs:
# (2, 7), (7, 2), (3, 6) and (6, 3).

def sumxor(s, x):
    '''
        Receives a sum (s) and a xor (x) and outputs
        all pairs (a,b) that satisfy:
            a + b = s
            a XOR b = x
    '''
    s_bits = get_binary_representation(s)
    s_length_in_bits = len(s_bits)
    (x_bits, fixed_bits, free_bits) = get_binary_representation_plus_free_and_fixed_bits(x, s_length_in_bits)
    a = get_base_value(s_bits, x_bits, fixed_bits)

    # Method 1: Using the memory to find all pairs
    generate_and_print_all_pairs_in_memory(a, free_bits, s, x)
    # Method 2: Using a gray code go generate all pairs consecutively
    generate_and_print_all_pairs_just_in_time(a, free_bits)

def generate_and_print_all_pairs_in_memory(a, free_bits, s, x):
    '''
        Produces all satisfying values of a using a list in memory.
        Then prints all the corresponding pairs.
    '''
    values = generate_all_values_to_list(a, free_bits)
    for value in values:
        print_pair(value, s, x)
    print ("Total number of pairs: ", len(values))

def generate_all_values_to_list(a, free_bits):
    '''
        Creates a list with all variants that have a as their base format.
        For each free bit i, creates a copy of all values currently in the list
        with the single difference bit i = 1.
        Each step doubles the number of values in the list, and so the whole process
        covers all combinations of the free bit positions.
    '''
    values = [a]
    # for each bit 1 in the the xor mask
    for index in free_bits:
        # copy each value in the list
        newvalues = []
        for value in values:
            # while setting this bit to 1
            newvalue = value | (1 << index)
            newvalues.append(newvalue)
        values = values + newvalues
    return values

def print_pair(a, s, x):
    b = a ^ x
    s = a + b
    print (a, b, s)    

def generate_and_print_all_pairs_just_in_time(a, free_bits):
    '''
        Takes a base value and uses a Gray Code to iterate
        through all combinations of free bit positions.
        Each codeword indicates which free bit positions
        should be added to a (bit is 1) or removed from a (bit is 0).
        The Gray Code ensures the change between successive pair values
        only changes in one position, to save as much time as possible
        in the full generation.
    '''
    free_bits_weights = compute_free_bits_weights(free_bits)
    value = a
    k = len(free_bits)
    current_code = gray_code(0)
    print_pair(value, s, x)
    count = 1
    for i in range(1, 1 << k):
        code = gray_code(i)
        change = current_code ^ code
        current_code = code
        value = value ^ free_bits_weights[change]
        print_pair(value, s, x)
        count += 1
    print ("Total number of pairs: ", count)

def gray_code(n):
    '''
        Returns the nth Gray Code word. The first one is 0.
    '''
    return n ^ (n >> 1)

def compute_free_bits_weights(free_bits):
    '''
        Instead of obtaining the position j that changes between two consecutive Gray codewords,
        it is easier to obtain 1 << j.
        This method builds a dictionary that associates these change values with the value of the
        corresponding free position.
    '''
    weights = {}
    for i in range(0, len(free_bits)):
        weights[1 << i] = 1 << free_bits[i]
    return weights

def get_base_value(s_bits, x_bits, fixed_bits):
    '''
        Returns an integer with all the fixed bits
        set to their uniquely determined value
        and all other bits set to 0
    '''
    a = 0
    x_length = len(x_bits)
    s_length = len(s_bits)
        
    for bit_index in fixed_bits:
        index_next_bit = bit_index + 1
        if index_next_bit >= s_length:
            bit = 0
        else:
            bit = x_bits[index_next_bit] ^ s_bits[index_next_bit]
        a |= bit << bit_index
    return a    

def get_binary_representation(n, bitLength = 0, full=0):
    '''
        Returns a list with each bit of n
        The first element is the least significant bit
        Besides, if full > 0, returns two lists with the indices
        of the bits 0 and the bits 1, respectively.
    '''
    if n == 0:
        if full == 0:
            return [0]
        else:
            return ([0],[0],[])
        
    if full > 0:
        bits_0 = []
        bits_1 = []

    index = 0        
    bits = []
    while n > 0 or index < bitLength:
        bit = n & 1
        bits.append(bit)
        n >>= 1
        if full > 0:
            if bit == 1:
                bits_1.append(index)
            else:
                bits_0.append(index)
            index += 1
    if full == 0:            
        return bits
    else:
        return (bits, bits_0, bits_1)

def get_binary_representation_plus_free_and_fixed_bits(n, bitLength = 0):
    '''
        Returns a list with each bit of n.
    '''
    return get_binary_representation(n, bitLength, 1)        
    
if __name__ == '__main__':
    s = int (sys.argv[1])
    x = int (sys.argv[2])
    # Example with larger numbers
    a = int(1e12)
    x = 0x25af7065
    b = a^x
    s = a + b
    sumxor(s, x)
