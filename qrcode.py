from matplotlib import pyplot as plt
import pprint

# Hashmaps
VERSIONS_DIMENSIONS = {
    1: 21,
    2: 25,
    3: 29,
    4: 33,
    5: 37,
    6: 41,
    7: 45,
    8: 49,
    9: 53,
    10: 57,
}

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

# ANTI_GF has an offset of 1 so that a diccionary is required
ANTI_GF = [
    0, 1, 25, 2, 50, 26, 198, 3, 223, 51, 238, 27, 104, 199, 75, 4, 100, 224, 14, 52,
    141, 239, 129, 28, 193, 105, 248, 200, 8, 76, 113, 5, 138, 101, 47, 225, 36, 15, 
    33, 53, 147, 142, 218, 240, 18, 130, 69, 29, 181, 194, 125, 106, 39, 249, 185, 
    201, 154, 9, 120, 77, 228, 114, 166, 6, 191, 139, 98, 102, 221, 48, 253, 226, 
    152, 37, 179, 16, 145, 34, 136, 54, 208, 148, 206, 143, 150, 219, 189, 241, 
    210, 19, 92, 131, 56, 70, 64, 30, 66, 182, 163, 195, 72, 126, 110, 107, 58, 
    40, 84, 250, 133, 186, 61, 202, 94, 155, 159, 10, 21, 121, 43, 78, 212, 229, 
    172, 115, 243, 167, 87, 7, 112, 192, 247, 140, 128, 99, 13, 103, 74, 222, 237, 
    49, 197, 254, 24, 227, 165, 153, 119, 38, 184, 180, 124, 17, 68, 146, 217, 35, 
    32, 137, 46, 55, 63, 209, 91, 149, 188, 207, 205, 144, 135, 151, 178, 220, 252, 
    190, 97, 242, 86, 211, 171, 20, 42, 93, 158, 132, 60, 57, 83, 71, 109, 65, 162, 
    31, 45, 67, 216, 183, 123, 164, 118, 196, 23, 73, 236, 127, 12, 111, 246, 108, 
    161, 59, 82, 41, 157, 85, 170, 251, 96, 134, 177, 187, 204, 62, 90, 203, 89, 
    95, 176, 156, 169, 160, 81, 11, 245, 22, 235, 122, 117, 44, 215, 79, 174, 213, 
    233, 230, 231, 173, 232, 116, 214, 244, 234, 168, 80, 88, 175
]

def GF(number):
    # Calculates the Galois Field GF(256) with byte-wise modulo 285
    # A hash map would be FAR better here, but I wanted to code it as a recursion
    # The inverse operation uses a hashmap for now
    if number < 2 ** 8:
        return number

    if number == 2 ** 8:
        return number ^ 285

    aux = GF(number >> 1) * 2
    if aux >= 256:
        return aux ^ 285
    
    return aux


def poly_mult(p1, p2):
    # A polynomial is represented by an array [a, bx^0, cx^1, ...]
    # In order forl this to work, we must use exponents of 2, so the polynomial must have a, b, c only as the value of the exponent
    # If the polynomial is 1 + 2x + 4x^2, the array should be [0, 1, 2]
    # This routine makes use of the arrays to calculate the multiplication
    # The output is in the form [a, b, c, ...] meaning 2^a + 2^b x + 2^c x^2 + ...

    new_p = []
    # Initializing the new polynomial with neutral XOR operator
    for i in range(len(p1) + len(p2) - 1):
        new_p.append(0)   

    # First getting the polynomial in its conventional form
    for i in range(len(p1)):
        for j in range(len(p2)):
            # Since we are using exponents, there is no need to multiply them            
            value = p1[i] + p2[j]
            if value >= 256:
                value = value % 255

            new_p[i + j] = new_p[i + j] ^ GF(2**value)

    # Converting back to the generator polynomial
    for i in range(len(new_p)):
        new_p[i] = ANTI_GF[new_p[i] - 1]

    return new_p

class QRCode():
    def __init__(self, data, mode, version, ec_level):
        self.id = f'{version}-{ec_level}'
        self.version = version
        self.data = data
        self.dim = VERSIONS_DIMENSIONS[self.version]
        self.datalen = len(data)
        self.shape = VERSIONS_DIMENSIONS[self.version]
        self.string = ''
        self.ec = ec_level
        self.mode = mode
        self.n_eccodewords = EC_CODEWORDS.get(self.id)
        self.blocksG1 = BLOCKS_G1.get(self.id)
        self.datacodeG1 = DATACODEWORDS_G1.get(self.id)
        self.blocksG2 = BLOCKS_G2.get(self.id)
        self.totalbits = TOTALBITS_TABLE.get(f'{version}-{ec_level}')
        self.g1 = []
        self.g2 = []
        self.ec_codewords = []
        self.matrix = []
        self.init_matrix()


    def init_matrix(self):
    # Initializes matrix full of zeros
        line = []
        for i in range(self.dim):
            line.append(0)
        for i in range(self.dim):
            self.matrix.append(line.copy())


    #region ---- RAW DATA ENCODING ---- 

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

    #region ---- ERROR CORRECTION -----
    # The error correction requires data codewords, a generator polynomial and a message polynomial
    # By dividing the polynomials we get the required codewords
    
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

    def generator_poly(self):
        # Creates the generator poly for any number of error correction codewords   
        # The polynomial is in the alpha notation form
        n_code = self.n_eccodewords
        poly = poly_mult([0, 0], [1, 0])

        for i in range(2, n_code):
            poly = poly_mult(poly, [i, 0])

        return poly

    def message_poly(self):
        # Creates the message polynomial which is represented by an array of [a, b, c,...]
        # This represents the polynomial a + bx + cx^2 + ....
        message = []
        for i in range(len(self.g1) - 1, -1, -1):
            message.append(int(self.g1[i], 2))

        for i in range(len(self.g2) - 1, -1, -1):
            message.append(int(self.g2[i], 2))

        return message

    def get_eccodewords(self):
        # Returns the error correction codewords as integers
        message = self.message_poly()
        generator = self.generator_poly()

        n_messageterm = len(message) # This is the original amount of terms
        # The firts step is to multiply the message polynomial by x^n where n is the number of error correction
        # codewords needed. This is to ensure that the exponent does not vanish during the divisions.
        # In this case, 0 means 2 ** 0 = 1, so I will use '' as a representation of 0
        for _ in range(self.n_eccodewords):
            message.insert(0, '')

        # The lead term of the generator polynomial should also have the same exponent
        for _ in range(len(message) - len(generator)):
            generator.insert(0, '')

        # The number of divisions must equal the number of terms in the message polynomial
        # This will result in a remainder of len(message) - n_messageterm which will be the codewords
        # For example, this should be 7 for a 1-L code
        ## STEPS ##
        # Multiply the Generator Polynomial by the Lead Term of the Message Polynomial
        # XOR the result with the message polynomial
        # REPEAT: Multiply the Generator Polynomial by the Lead Term of the XOR result from the previous step
        aux = []
        term = message[len(message) - 1]
        for i in range(n_messageterm):

            for j in range(len(generator)):

                # Since we are using exponents, there is no need to multiply them
                if generator[j] != '':
                    value = term + generator[j]
                    
                    if message[j] != '':

                        if value >= 256:
                            value = value % 255
                        aux.append(GF(2**value) ^ GF(2**message[j]))

                    # If message is zero, the XOR result is the value itself
                    else:
                        aux.append(GF(2**value))

                # If the generator is zero
                else:
                    if message[j] == '':
                        aux.append('')
                    else: 
                        # If the message is not zero, the XOR result is the message itself
                        aux.append(GF(2**message[j]))
            
            # Now it is important to get the next term to be multiplied
            # The message should be the result
            message = aux.copy()
            message[len(message) - 1 -i] = ''

            # If there are no more iterations, get out of the function
            if i != n_messageterm - 1:
                aux.clear()
            else:
                # Skipping unnecessary calculations
                break

            # Turning the message back to integer            
            for k in range(len(message)):
                if message[k] != '':
                    message[k] = ANTI_GF[message[k] - 1]
            term = message[-2 - i]
            
            # Adjusting the generator to the exponents needed
            for k in range(len(generator) - 1):
                generator[k] = generator[k + 1]
            generator[len(generator) - 1] = ''


        # The error correction codewords are the remainder terms
        # self.ec_codewords = aux[len(aux) - 1 - self.n_eccodewords: len(aux) - 1]
        eccodewords = message[:self.n_eccodewords]
        self.ec_codewords = eccodewords
        return eccodewords

    def place_eccodewords(self):
        # This function simply adds the ec codewords to the qr code string
        for i in range(self.n_eccodewords):
            codeword = format(self.ec_codewords[i], 'b')
            formatted_s = (8 - len(codeword)) * '0' + codeword
            self.string += formatted_s

    #endregion

    #region ---- CODE STRUCTURE -----
   
    # For now, this is very inefficient and all those steps can be done at once.
    # To keep things easier to debug, I've implemented them separetely

    def show_code(self):
        plt.imshow(self.matrix, interpolation='nearest', cmap='gray', vmin=0, vmax=1)
        plt.show()

    def finder_pattern(self):
        # Creates the finder pattern for the QR Code

        for i in range(self.dim):
            for j in range(self.dim):

                if (i == j == 0) or (i == 0 and j == self.dim - 7) or (i == self.dim - 7 and j == 0):
                    # Finder
                    for k in range(5):
                        self.matrix[i + 1][j + 1 + k] = 1
                        self.matrix[i + 5][j + 1 + k] = 1
                    
                    for k in range(3):
                        self.matrix[i + 2 + k][j + 1] = 1
                        self.matrix[i + 2 + k][j + 5] = 1
                    
                    # SEPARATOR
                    if j == 0:
                        # Right separator
                        for k in range(9):
                            if i != 0:
                                self.matrix[i + k - 1][j + 8] = 1

                        if i == 0:
                            # Bottom separator
                            for k in range(9):
                                if j != 0:
                                    self.matrix[i + 8][j - 1 + k] = 1

                        if i == self.dim - 7:
                            # Top separator
                            for k in range(9):
                                if j != 0:
                                    self.matrix[i - 1][j + k - 1] = 1

                    else:     
                        # Left separator
                        for k in range(9):
                            try:
                                self.matrix[i + k][j - 1] = 1
                            except IndexError:
                                pass
                        # Bottom separator
                        for k in range(9):
                            if j != 0:
                                self.matrix[i + 8][j - 1 + k] = 1
                

qr = QRCode('HELLO', 'Alphanumeric', 1, 'L')

# ## ENCODING THE RAW DATA
# qr.set_mode()
# qr.character_count()
# qr.alpha_conversion()
# qr.terminator()
# qr.padding()
# qr.data_codewords()

# ## ERROR CODEWORDS
# qr.get_eccodewords()
# qr.place_eccodewords()
# -> For larger QR Codes (those which have more than one block) it is necessary to interleave the data and the
#   error correction codewords. For now, this step is going to be skipped

## QR CODE STRUCTURE
qr.finder_pattern()
qr.show_code()
pprint.pprint(qr.matrix)
