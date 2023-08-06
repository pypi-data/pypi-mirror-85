from bitstore import int_to_bitstr, bitstr_to_int, modify_bit, bits_required, bitarr_combine, bitstr_to_bitarr, int_to_bitarr
"""
int_to_bitstr(value: int) -> str
bitstr_to_int(bit_str: str) -> int
modify_bit(value: int, position: int, bit_value: bool = None) -> int
bits_required(value: int) -> int
"""

class TestBitstore:
    def test_int_to_bitstr(self):
        assert int_to_bitstr(0b101) == "101"
        assert int_to_bitstr(0b0) == "0"
        assert int_to_bitstr(0b1010101000111) == "1010101000111"

    def test_bitstr_to_int(self):
        assert bitstr_to_int("101") == 0b101
        assert bitstr_to_int("0") == 0b0
        assert bitstr_to_int("342") == -1 # Invalid returns -1
        assert bitstr_to_int(0) == -1

    def test_modify_bit(self):
        assert modify_bit(0b101, 1) == 0b111
        assert modify_bit(0b101, 3) == 0b1101
        assert modify_bit(0b111, 1) == 0b101
        assert modify_bit(0b0, 0) == 0b1
        assert modify_bit(0b0, 0, bit_value=False) == 0b0
        assert modify_bit(0b0, 0, bit_value=True) == 0b1
        assert modify_bit(0b1000, 3, bit_value=False) == 0b0000
        assert modify_bit(0b000000000, 8) == 0b100000000

    def test_bits_required(self):
        assert bits_required(0b0) == 1
        assert bits_required(0b1) == 1
        assert bits_required(0b10) == 2
        assert bits_required(0b11) == 2
        assert bits_required (0b10010101) == 8

    def test_bitstr_to_bitarr(self):
        assert bitstr_to_bitarr("234") == -1
        assert bitstr_to_bitarr("0") == 0b10
        assert bitstr_to_bitarr("1") == 0b11
        assert bitstr_to_bitarr("0011") == 0b10011
        assert bitstr_to_bitarr("001") == 0b1001

    def test_bitarr_combine(self):
        # 0(10-2) comb 0(10-2) == 4(100)
        assert bitarr_combine(0b10, 0b10) == 0b100
        assert bitarr_combine(0b10, 0b101) == 0b1001
        assert bitarr_combine(0b1001, 0b1011) == 0b1001011
    
    def test_int_to_bitarr(self):
        assert int_to_bitarr(0b001) == 0b11
        assert int_to_bitarr(0b0) == 0b10
        assert int_to_bitarr(0b1100) == 0b11100
        assert int_to_bitarr(-3) == -1