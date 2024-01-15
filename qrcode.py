import numpy as np

# Hashmaps
ALPHANUMERIC_TABLE = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'A': 10,
    'B': 11,
    'C': 12,
    'D': 13,
    'E': 14,
    'F': 15,
    'G': 16,
    'H': 17,
    'I': 18,
    'J': 19,
    'K': 20,
    'L': 21,
    'M': 22,
    'N': 23,
    'O': 24,
    'P': 25,
    'Q': 26,
    'R': 27,
    'S': 28,
    'T': 29,
    'U': 30,
    'V': 31,
    'W': 32,
    'X': 33,
    'Y': 34,
    'Z': 35,
    ' ': 36,
    '$': 37,
    '%': 38,
    '*': 39,
    '+': 40,
    '-': 41,
    '.': 42,
    '/': 43,
    ':': 44
}

MODE_INDICATOR_TABLE = {
    'Numeric': '0001',
    'Alphanumeric': '0010',
    'Byte': '0100',
    'Kanji': '1000'
}

EC_CODEWORDS = {
    '1-L': 7,
    '1-M': 10,
    '1-Q': 13,
    '1-H': 17,
    '2-L': 10,
    '2-M': 16,
    '2-Q': 22,
    '2-H': 28,
    '3-L': 15,
    '3-M': 26
}

DATACODEWORDS_G1 = {
    '1-L': 19,
    '1-M': 16,
    '1-Q': 13,
    '1-H': 9,
    '2-L': 34,
    '2-M': 28,
    '2-Q': 22,
    '2-H': 16,
    '3-L': 55,
    '3-M': 44
}

BLOCKS_G1 = {
    '1-L': 1,
    '1-M': 1,
    '1-Q': 1,
    '1-H': 1,
    '2-L': 1,
    '2-M': 1,
    '2-Q': 1,
    '2-H': 1,
    '3-L': 1,
    '3-M': 1
}

BLOCKS_G2 = {
    '1-L': 0,
    '1-M': 0,
    '1-Q': 0,
    '1-H': 0,
    '2-L': 0,
    '2-M': 0,
    '2-Q': 0,
    '2-H': 0,
    '3-L': 0,
    '3-M': 0
}

TOTALBITS_TABLE = {
    '1-L': 152,
    '1-M': 128,
    '1-Q': 104,
    '1-H': 72,
    '2-L': 272,
    '2-M': 224,
    '2-Q': 176,
    '2-H': 128,
    '3-L': 440,
    '3-M': 352
}

def GF(number):
    # Calculates the Galois Field 256 of a number modulo 100011101 (285)
    # A hash map could be used here, but I wanted to code it

    if number < 2 ** 8:
        return number

    if number == 2 ** 8:
        return number ^ 285

    aux = GF(number >> 1) * 2
    if aux >= 256:
        return aux ^ 285
    
    return aux

class QRCode():
    def __init__(self, data, mode, version, ec_level):
        self.id = f'{version}-{ec_level}'
        self.version = version
        self.data = data
        self.datalen = len(data)
        self.string = ''
        self.ec = ec_level
        self.mode = mode
        self.eccodewords = EC_CODEWORDS.get(self.id)
        self.blocksG1 = BLOCKS_G1.get(self.id)
        self.datacodeG1 = DATACODEWORDS_G1.get(self.id)
        self.blocksG2 = BLOCKS_G2.get(self.id)
        self.totalbits = TOTALBITS_TABLE.get(f'{version}-{ec_level}')
        self.g1 = []
        self.g2 = []

    # ---- RAW DATA ENCODING ---- 

    def fill_zeros (self, string, amount):
        ## Fills the given string with ´amount´ zeros before it.
        new_s = '0' * (amount - self.datalen) + string
        return new_s

    def set_mode(self):
        ## Appends the mode encoding to the class string.
        self.string += MODE_INDICATOR_TABLE.get(self.mode) # 9 bits for versions 1 through 9

    def character_count(self):
        ## Appends the character count enoding to the class string.

        if self.version >= 1 and self.version <= 9:
            
            if self.mode == 'Alphanumeric':

                bin = self.fill_zeros(format(self.datalen, 'b'), 9)
                self.string += bin
        

    def alpha_conversion(self):
        ## Encodes the data according to the alphanumeric table of conversion.
        
        if self.mode != 'Alphanumeric':
            return

        # Taking pairs of characters and encoding them using the alphanumeric table.
        for i in range(0, self.datalen - 1, 2):
            value = (45 * ALPHANUMERIC_TABLE.get(self.data[i]) + ALPHANUMERIC_TABLE.get(self.data[i + 1]))
            self.string += self.fill_zeros(format(value, 'b'), 11)

        if self.datalen % 2 != 0:
            value = ALPHANUMERIC_TABLE.get(self.data[self.datalen - 1])
            self.string += self.fill_zeros(format(value, 'b'), 6)


    def terminator(self):
        ## Adds terminator bits to string

        if self.version == 1 and self.ec == 'L':
            
            bits = len(self.string)
            if bits <=  self.totalbits - 4:
                self.string += 4 * '0'

            else:
                self.string += (self.totalbits - bits) * '0'


    def padding(self):
        ## Adds the final padding to make sure the string lenght is a multiple of 8

        remainder = len(self.string) % 8

        if remainder != 0:
            self.string += (8 - remainder) * '0'
    
        ## Filling the remaining bits by repeating the '11101100 00010001' string of bits
        bits_to_fill = self.totalbits - len(self.string)

        for i in range(0, bits_to_fill // 8):
            if i % 2 == 0:
                self.string += '11101100'
            else:
                self.string += '00010001'
            
    #endregion

    # ---- ERROR CORRECTION -----
                
    def data_codewords(self):
        ## Generates the blocks and groups of codewords. Blocks are represented by the items in the g1 array
        if self.blocksG2 == 0:
            counter = 0
            for _ in range(self.datacodeG1):
                new_s = ''
                for i in range(8): # Each codeword has exactly 8 bits
                    new_s +=  self.string[counter + i]
                
                counter += 8
                self.g1.append(new_s)

    
    
print(GF(2**12))
for i in range(9, 20):
    print(f'2 ^ {i}: {GF(2**i)}')

# qr = QRCode('HELLO', 'Alphanumeric', 1, 'L')

# ## ENCODING THE RAW DATA
# qr.set_mode()
# qr.character_count()
# qr.alpha_conversion()
# qr.terminator()
# qr.padding()
# qr.data_codewords()