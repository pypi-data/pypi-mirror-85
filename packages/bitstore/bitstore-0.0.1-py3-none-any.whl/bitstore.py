#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re as regex
import math

def int_to_bitstr(int_value: int) -> str:
    """
    A function which returns its bit representation as a string.

    Arguments:
    int_value (int) - The int value we want to get the bit representation for.

    Return:
    str             - The string representation of the bits required to form the int.
    """
    return bin(int_value)[2:]

def bitstr_to_int(bit_str: str) -> int:
    """
    A function which turns a string bit representation to its int value.

    Arguments:
    bit_str (str)   - The string representation of the bits corresponding to an int.

    Return:
    int             - The int value of the bits represented in the string .
                      Returns -1 if the input is invalid.
    """
    bits_value = 0
    if isinstance(bit_str, str) and regex.match("[0|1]+", bit_str):
        for n in range(len(bit_str)):
            bit_index = len(bit_str) - n - 1
            bits_value += 2**n if bit_str[bit_index] == "1" else 0
    else:
        bits_value = -1
            
    return bits_value

def modify_bit(input_value: int, bit_index: int, bit_value: bool = None) -> int:
    """
    A function which modifies the bit at bit index.
    Index 0 being the right most bit.

    Arguments:
    input_value (int)   - The int value of the bit array we want to modify
    bit_index   (int)   - The index of the bit we want to change.
    bit_value   (int)   - The value of the modification (True = 1, False = 0). Default is to flip the bit.

    Return:
    int                 - The value of the modified bit array
    """
    #if 2**bit_index <= input_value or input_value == 0: # Here we make sure that the index is within our bit representatation
    sig_bit_value = input_value >> bit_index # By shifting out input value we get the significant bit we are interested in
    if sig_bit_value % 2 == 1:
        if bit_value != True:
            return input_value - 2**bit_index
    else:
        if bit_value != False:
            return input_value + 2**bit_index
    return input_value

def bits_required(int_value: int) -> int:
    """
    Calculates the bits required to store the int value.

    Arguments:
    int_value (int) - The value of the bit array.

    Return:
    int             - The length of the bit array.
    """
    if int_value < 2:
        return 1
    elif int_value == 2:
        return 2
    else:
        return math.ceil(math.log2(int_value))

def bitstr_to_bitarr(bit_str: str) -> int:
    """
    This function creates an int representation of a bit array. It saves all information by adding a
    1 as the most significant bit, that way 0 won't be omitted in the int.

    Arguments:
    bit_str (str)   - The string representation of a bit array.

    Return:
    int             - The int representation of a bit array.
    """
    bitstr_value = bitstr_to_int(bit_str)
    return bitstr_value + 2**len(bit_str) if bitstr_value > -1 else -1

def int_to_bitarr(int_value: int) -> int:
    """
    A function which adds a padding 1 as the most significant bit to save 0 information in a bit array.

    Arguments:
    int_value   (int)   - The int value to be represented as a bit array.

    Return:
    int                 - The int representation of the bit array

    Example:
    int_to_bitarr(0b0001) => 0b10001
    """
    return int_value + 2**bits_required(int_value) if int_value > -1 else -1

def bitarr_combine(left: int, right: int) -> int:
    """
    A function which combines two bit arrays and returns the int representation of the combined array.

    Arguments:
    left    (int)   - The int representation of the left bit array.
    right   (int)   - The int representation of the right bit array.

    Return:
    int             - The int representation of the combined bit array.
    """
    right_length = bits_required(right)
    right_true_length = right_length - 1 # Removing the padding 1 at the most significant bit in right
    right_true_value = right - 2**right_true_length # Removing the value of the padding 1
    return (left << right_true_length) + right_true_value


__author__ = '{JesperGlas}'
__copyright__ = 'Copyright {2020}, {bitstore}'
__license__ = '{MIT}'
__version__ = '{0}.{0}.{1}'
__maintainer__ = '{JesperGlas}'
__email__ = '{jesper.glas@gmail.com}'