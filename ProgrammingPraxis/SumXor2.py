import sys
import time
import pdb

import AuxUtils

# Sum and Xor:
# Assume there are two positive integers a and b that have sum s and XOR x.
# Given an s on the range [2, 1012] and x on the range [0, 1012],
# find a list of possible values of the ordered pairs (a, b). For instance,
# given s = 9 and x = 5, there are four possible pairs:
# (2, 7), (7, 2), (3, 6) and (6, 3).

# All solutions have the same format, i.e.,
# all possible a and b have exactly the same values in some fixed positions.
# These are called in the code fixed_bits by opposition to free bits.

# These methods compute all pairs.
# A simple improvement would be to stop the generation process short at half-point and
# each time a pair is generated, its symmetric would also be printed

def sumxor_list(s, x, test = 0):
    '''                   
        This solution first finds the minimal a that satisfies the conditions.
        Then it finds all the other such pairs by changing a only in its free bits.
        The computation of these variants is done wholly in memory,
        with as many steps as there are free bits:
        it keeps a list of discovered solution values, and at each step
        doubles this list by shifting one bit in a copy of the existing values        
    '''
    s_bits = AuxUtils.get_binary_representation(s)
    (x_bits, fixed_bits, free_bits) = AuxUtils.get_binary_representation_plus_0_and_1_lists(x)
    a = AuxUtils.get_base_value(s_bits, x_bits, fixed_bits)
    print("Fixed: ", a)
    values = AuxUtils.generate_and_print_all_pairs_in_memory(a, free_bits, x, test)
    if test==1:
        return values

def sumxor_graycode(s, x, test=0):
    '''                   
        This solution first finds the minimal a that satisfies the conditions.
        Then it finds all the other such pairs by changing a only in its free bits.
        The computation of these variants is done by generating a new value at each new step
        without keeping them in memory.
        To advance to the next step, I use a gray_code that iterates over all combinations of free bits
        but in a way that only one bit changes between two consecutive values
        Consequently, the pairs generated do not appear sorted by their first value.
    '''
    s_bits = AuxUtils.get_binary_representation(s)
    (x_bits, fixed_bits, free_bits) = AuxUtils.get_binary_representation_plus_0_and_1_lists(x)
    a = AuxUtils.get_base_value(s_bits, x_bits, fixed_bits)
    values = AuxUtils.generate_and_print_all_pairs_just_in_time(a, x, free_bits, test)
    if test==1:
        return values
    
def sumxor_naive(s, x, test=0):
    ''' This is the naive solution that simply iterates over all numbers
        printing all the solutions found on the way
    '''
    if test==1:
        list=[]
    count = 0
    a = 0    
    while True:
        b = a ^ x
        if (a > s):
            break
        if (a + b) == s:
            count += 1
            print(a, b)
            if test==1:
                list.append((a,b))
        a += 1
    print ("Total number of pairs: ", count)
    if test==1:
        return list

def sumxor_bit(s, x, test=0):
    ''' This is a solution given by Matthew at
        https://programmingpraxis.com/2016/04/01/sum-and-xor/2/
        It is fantastically compact!
        Note: I have changed the exit condition to iterate the whole set of pairs
    '''
    if test==1:
        list=[]    
    carries = (s ^ x) >> 1
    fixed = carries & (~x)
    a = fixed
    count = 0
    while True:
        b = a ^ x
        print(a, b)
        if test==1:
            list.append((a,b))

        a = ((( a | ~x) + 1) & x) | fixed
        count += 1
        if (a == fixed):
            break        
    print ("Total number of pairs: ", count)
    if test==1:
        return list

def time_run(method, s, x):
    before = time.clock()
    method(s,x)
    after = time.clock()
    print("Time for %s: %s" % (method.__name__, after - before ))
  
if __name__ == '__main__':
    # a = int(1e12)
    # x = 0x25af7612
    # b = a^x
    # s = a + b
    # 
    # time_run(sumxor_list,s, x)
    # time_run(sumxor_graycode,s, x)
    # time_run(sumxor_bit,s, x)
    
    a = 10348945
    x = 0xc853
    b = a^x
    s = a + b

    time_run(sumxor_list,s, x)
    time_run(sumxor_graycode,s, x)
    time_run(sumxor_bit,s, x)
    time_run(sumxor_naive,s, x)
