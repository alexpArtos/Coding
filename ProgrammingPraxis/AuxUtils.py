#Auxiliary functions to declutter the main one

import unittest
import SumXor2
import pdb

def get_base_value(s_bits, x_bits, fixed_bits):
    '''
        Returns an integer with all the fixed bits
        set to their uniquely determined value
        and all other bits set to 0.
        Fixed bits occur in positions where x is 0.
        The value of a fixed bit is equal to the carry
        sent to the next column. This is equal to the xor
        of s and x for that column.
    '''
    a = 0
    
    x_length = len(x_bits)
    s_length = len(s_bits)
    if x_length < s_length:
        fixed_bits += [i for i in range(x_length, s_length)]

    for bit_index in fixed_bits:
        index_next_bit = bit_index + 1
                       
        if index_next_bit >= s_length:
            # there is no next column in s, so there must not have been a carry to it
            # the number is complete
            return a
        if index_next_bit >= x_length:
            # there are no x bits at this position, so x's bit is 0
            bit = s_bits[index_next_bit]
        else:          
            bit = x_bits[index_next_bit] ^ s_bits[index_next_bit]            
        a |= bit << bit_index
    return a
    

def generate_and_print_all_pairs_just_in_time(a, x, free_bits, test=0):
    '''
        Takes a base value and uses a Gray Code to iterate
        through all combinations of free bit positions.
        Each codeword indicates which free bit positions
        should be added to a (bit is 1) or removed from a (bit is 0).
        The Gray Code ensures the change between successive pair values
        only changes in one position, to save as much time as possible
        in the full generation.
        
        Example:
            free_bits = [3,5,6]
            the Gray Code will iterate from 000 to 100 (passing through all 8 possible values)
            the change positions for the Gray Code are 1, 2 and 4,
            and we want to associate these to the weights of the free bits:
            1 to (1 << 3)
            2 to (1 << 5)
            4 to (1 << 6)
    '''
    if test==1:
        list=[]
        
    k = len(free_bits)
    change_weights = {1 << bit : 1 << (free_bits[bit]) for bit in range(0,k)}      
   
    current_code = gray_code(0)
    value = a
    b = a^x
    print(a,b)
    if test==1:
        list.append((a,b))   
    count = 1
    
    for i in range(1, 1 << k):
        code = gray_code(i)
        change = current_code ^ code
        a = a ^ change_weights[change]
        b = a^x
        print(a,b)
        if test==1:
            list.append((a,b))   

        count += 1
        current_code = code        
    print ("Total number of pairs: ", count)
    if test==1:
        return list


def gray_code(n):
    '''
        Returns the nth Gray Code word. The first one is 0.
    '''
    return n ^ (n >> 1)

def generate_and_print_all_pairs_in_memory(a, free_bits, x, test=0):
    '''
        Produces all satisfying values of a using a list in memory.
        Then prints all the corresponding pairs.
    '''
    if test==1:
        list=[]
        
    values = generate_all_values_to_list(a, free_bits)
    for a in values:
        b = a^x
        print(a, b)       
        if test==1:
            list.append((a,b))

    print ("Total number of pairs: ", len(values))
    if test==1:
        return list

def generate_all_values_to_list(a, free_bits):
    '''
        Creates a list with all variants that have a as their base format.
        For each free bit i, creates a copy of all values currently in the list
        with the single difference bit i = 1.
        Each step doubles the number of values in the list, and so the whole process
        covers all combinations of the free bit positions.
    '''
    values = [a]
    free_bits_weights = [1 << n for n in free_bits]
    # for each bit 1 in the the xor mask
    for setbit in free_bits_weights:
        # copy each value in the list
        newvalues = []
        for value in values:
            # and set this bit to 1
            newvalue = value | setbit
            newvalues.append(newvalue)
        values = values + newvalues
    return values

def get_binary_representation_plus_0_and_1_lists(n):
    '''
        Returns a list with each bit of n.
    '''
    return get_binary_representation(n, 1)        


def get_binary_representation(n, with_lists=0):
    '''
        Returns a list with each bit of n
        The first element is the least significant bit
        Besides, if with_lists > 0, returns two lists with the indices
        of the bits 0 and the bits 1, respectively.
        
        Some clarity has been sacrificed to optimize running time,
        and avoid repeated code as much as possible.
    '''
    if n == 0:
        if with_lists == 0:
            return [0]
        else:
            return ([0],[0],[])
        
    # If we require the list of 0 and 1 bits, initialize them here.
    if with_lists > 0:
        bits_0 = []
        bits_1 = []

    index = 0
    bits = []
    while n > 0:
        bit = n & 1
        bits.append(bit)
        n >>= 1
        if with_lists > 0:
            if bit == 1:
                bits_1.append(index)
            else:
                bits_0.append(index)
            index += 1
    if with_lists == 0:            
        return bits
    else:
        return (bits, bits_0, bits_1)


class AllTests(unittest.TestCase):

    def test_get_base_value(self):
        expected = 16
        x = 44
        s = 76
        x_bits = [0,0,1,1,0,1]
        fixed_bits = [0,1,4]
        s_bits = [0,0,1,1,0,0,1]
        # self.assertEqual(expected, get_base_value(s_bits, x_bits, fixed_bits))       

        expected = 1
        x = 44
        s = 46
        x_bits = [0,0,1,1,0,1]
        fixed_bits = [0,1,4]
        s_bits = [0,1,1,1,0,1]
        
        expected = 10000
        x = 161
        s = 20161
        (x_bits, fixed_bits, free_bits) = get_binary_representation(x,1)        
        s_bits = get_binary_representation(s)
        self.assertEqual(expected, get_base_value(s_bits, x_bits, fixed_bits))
        
        expected = 4
        x = 62459
        s = 62467
        (x_bits, fixed_bits, free_bits) = get_binary_representation(x,1)
        s_bits = get_binary_representation(s)
        # self.assertEqual(expected, get_base_value(s_bits, x_bits, fixed_bits))
    
        expected = 547
        x = 18572
        s = 19666
        (x_bits, fixed_bits, free_bits) = get_binary_representation(x,1)
        s_bits = get_binary_representation(s)
        # self.assertEqual(expected, get_base_value(s_bits, x_bits, fixed_bits))

        expected = 1408
        x = 27263
        s = 30079
        (x_bits, fixed_bits, free_bits) = get_binary_representation(x,1)
        s_bits = get_binary_representation(s)
        # self.assertEqual(expected, get_base_value(s_bits, x_bits, fixed_bits))
            
    def aux_single_binary_representation(self, n, expected, expected_0, expected_1):
        self.assertEqual(3, 2+1)
        bits = get_binary_representation(n)
        self.assertEqual(expected, bits)    
        (bits_x, bits_0, bits_1) = get_binary_representation(n,1)
        self.assertEqual(expected, bits_x)
        self.assertEqual(expected_0, bits_0)
        self.assertEqual(expected_1, bits_1)
    
    def test_get_binary_representation(self):
        n = 43
        expected = [1,1,0,1,0,1]
        expected_0 = [2,4]
        expected_1 = [0,1,3,5]
        self.aux_single_binary_representation(n, expected, expected_0, expected_1)

        n = 1234598046
        expected = [0,1,1,1,1,0,0,1,0,0,0,1,1,1,1,0,0,1,1,0,1,0,0,1,1,0,0,1,0,0,1]
        expected_0 = [0,5,6,8,9,10,15,16,19,21,22,25,26,28,29]
        expected_1 = [1,2,3,4,7,11,12,13,14,17,18,20,23,24,27,30]
        self.aux_single_binary_representation(n, expected, expected_0, expected_1)
        
        n = 508881353
        expected = [1,0,0,1,0,0,1,1,1,0,0,1,0,1,1,1,0,0,1,0,1,0,1,0,0,1,1,1,1]
        expected_0 = [1,2,4,5,9,10,12,16,17,19,21,23,24]
        expected_1 = [0,3,6,7,8,11,13,14,15,18,20,22,25,26,27,28]
        self.aux_single_binary_representation(n, expected, expected_0, expected_1)

        n = 3478846008
        expected = [0,0,0,1,1,1,0,0,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1,0,1,1,1,1,0,0,1,1]
        expected_0 = [0,1,2,6,7,8,10,16,18,21,23,28,29]
        expected_1 = [3,4,5,9,11,12,13,14,15,17,19,20,22,24,25,26,27,30,31]
        self.aux_single_binary_representation(n, expected, expected_0, expected_1)

        n = 610921329
        expected = [1,0,0,0,1,1,1,0,1,1,0,1,0,1,1,1,1,0,0,1,0,1,1,0,0,0,1,0,0,1]
        expected_0 = [1,2,3,7,10,12,17,18,20,23,24,25,27,28]
        expected_1 = [0,4,5,6,8,9,11,13,14,15,16,19,21,22,26,29]
        self.aux_single_binary_representation(n, expected, expected_0, expected_1)



if __name__ == '__main__':
    unittest.main()
