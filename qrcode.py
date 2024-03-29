from matplotlib import pyplot as plt
import pprint
from math import floor, ceil, log2

WHITE = 0
BLACK = 1
GRAY = 0.5

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

EC_CODEWORDS = { # Number of EC Codewords
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

EC_BITS = { # Bits used to create the format string
    'L': 0b01,
    'M': 0b00,
    'Q': 0b11,
    'H': 0b10
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


def show_code(matrix):
    plt.imshow(matrix, interpolation='nearest', cmap='gray_r', vmin=0, vmax=1)
    plt.show()


class QRCode():
    def __init__(self, data, mode, version, ec_level):
        self.id = f'{version}-{ec_level}' # ID used to search the hashmaps
        self.version = version # Versio of the QR Code
        self.data = data # Data to be encoded
        self.datalen = len(data) # Lenght of data
        self.shape = VERSIONS_DIMENSIONS[self.version] # Dimension of the QR Code
        self.string = '' # Binary string representing data and error correction
        self.ec = ec_level # Level of error correction (L, M, Q, H)
        self.mode = mode # QR Code mode (Alphanumeric, Numeric, ...)
        self.n_eccodewords = EC_CODEWORDS.get(self.id) # Number of EC codewords
        self.blocksG1 = BLOCKS_G1.get(self.id) # Number of blocks in group 1
        self.datacodeG1 = DATACODEWORDS_G1.get(self.id) # Number of data codewords for each block
        self.blocksG2 = BLOCKS_G2.get(self.id) # Number of blocks in group 2
        self.totalbits = TOTALBITS_TABLE.get(self.id) # Total bits necessary
        self.g1 = [] # Codewords of G1 group
        self.g2 = [] # Codewords of G2 group
        self.ec_codewords = [] # Error correction codewords
        self.matrix = [] # Final matrix
        self.covered_area = []  # Area covered by mandatory patterns
                                # start_row, start_column, width, height
        self.mask_number = 0
        self.init_matrix()


    def init_matrix(self):
    # Initializes a gray matrix
        line = []
        for _ in range(self.shape):
            line.append(GRAY)
        for _ in range(self.shape):
            self.matrix.append(line.copy())


    #region ---- RAW DATA ENCODING ---- 

    def fill_zeros (self, string, amount):
        ## Fills the given string with ´amount´ zeros before it.
        new_s = '0' * (amount - len(string)) + string
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

        # TODO Add the other error correction levels
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
        for i in range(len(message)):
            message[i] = ANTI_GF[message[i] - 1]
        generator = self.generator_poly()

        #DEBBUGING
        # self.n_eccodewords = 10
        # message = [17, 236, 17, 236, 17, 236, 64, 67, 77, 220, 114, 209, 120, 11, 91, 32]
        # for _ in range(len(message)):
        #     message[_] = ANTI_GF[message[_] - 1]
        # generator = [45, 32, 94, 64, 70, 118, 61, 46, 67, 251, 0]

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
            message[len(message) - 1 - i] = ''

            # Turning the message back to integer            
            for k in range(len(message)):
                if message[k] != '':
                    message[k] = ANTI_GF[message[k] - 1]
            term = message[-2 - i]
            
            # Adjusting the generator to the exponents needed
            for k in range(len(generator) - 1):
                generator[k] = generator[k + 1]
            generator[len(generator) - 1] = ''

        
            # If there are no more iterations, get out of the function
            if i != n_messageterm - 1:
                aux.clear()

        # The error correction codewords are the remainder terms        
        index = 0 # Index where the remainder begins
        for k in range(len(message)):
            if message[k] == '':
                index += 1
            else:
                break

        eccodewords = message[index:self.n_eccodewords]

        for i in range(len(eccodewords) // 2): # Reversing the list and taking it back to integers
            eccodewords[i],  eccodewords[-i - 1] = GF(2 ** eccodewords[-i - 1]), GF(2 ** eccodewords[i])
 
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
        # plt.ion()
        plt.imshow(self.matrix, interpolation='nearest', cmap='gray_r', vmin=0, vmax=1)
        plt.show()
        # plt.pause(0.7)
        # plt.close("all") 


    def finder_pattern(self):
        # Creates the finder pattern for the QR Code
        # FIXED PATTERNS
        for i in range(self.shape):
            for j in range(self.shape):

                if (i == j == 0) or (i == 0 and j == self.shape - 7) or (i == self.shape - 7 and j == 0):
                    # Finder
                    for k in range(5):
                        self.matrix[i + 1][j + 1 + k] = WHITE
                        self.matrix[i + 5][j + 1 + k] = WHITE
                    
                    for k in range(3):
                        self.matrix[i + 2 + k][j + 1] = WHITE
                        self.matrix[i + 2 + k][j + 5] = WHITE
                    
                    # SEPARATOR
                    if j == 0:
                        # Right separator
                        for k in range(9):
                            if i + k != 0 and i + k - 1 != self.shape:
                                self.matrix[i + k - 1][j + 7] = WHITE

                        if i == 0:
                            # Bottom separator
                            for k in range(9):
                                if j + k != 0:
                                    self.matrix[i + 7][j - 1 + k] = WHITE

                        else:
                            # Top separator
                            for k in range(9):
                                if j + k != 0:
                                    self.matrix[i - 1][j + k - 1] = WHITE

                    else:     
                        # Left separator
                        for k in range(8):
                            self.matrix[i + k][j - 1] = WHITE
                        # Bottom separator
                        for k in range(8):
                            self.matrix[i + 7][j - 1 + k] = WHITE

                # TIMING PATTERN
                if (i == 6 and 8 <= j <= self.shape - 9):
                    if j % 2 == 0:
                        self.matrix[i][j] = BLACK
                    else:
                        self.matrix[i][j] = WHITE
                if (8 <= i <= self.shape - 9 and j == 6):
                    if i % 2 == 0:
                        self.matrix[i][j] = BLACK
                    else:
                        self.matrix[i][j] = WHITE
        
        if self.version <= 7:
            # Finder pattern + information reservation
            self.covered_area.append([0, 0, 8, 8]) # Top left
            self.covered_area.append([0, self.shape - 8, 7, 8]) # Top right
            self.covered_area.append([self.shape - 8, 0, 8, 7]) # Botton left

        if self.version >= 2:
            # Here goes the alignment patterns positions
            pass

        # DARK MODULE
        self.matrix[(4 * self.version) + 9][8] = BLACK # This goes into the same region as the version information


    def isCovered(self, row, column):

        for i in range(len(self.covered_area)):
            if self.covered_area[i][0] <= row <= self.covered_area[i][0] + self.covered_area[i][3] and self.covered_area[i][1] <= column <= self.covered_area[i][1] + self.covered_area[i][2]:
                return True
        return False


    def data_placement(self):

        counter = 0 # This is used to check whether the pattern goes up or down
                    # If the counter is even, the pattern goes up, if the counter is odd, the pattern goes down
        data_int = int((self.string[::-1]), 2)
        column = self.shape - 1

        while column >= 0:

            if column == 6: # Timing pattern for columns skips only one column
                column -= 1
                continue

            if counter % 2 == 0: # Going up

                for row in range(self.shape - 1, -1, -1):

                    if row == 6:
                        continue

                    if not self.isCovered(row, column):
                        self.matrix[row][column] = data_int & 0b1
                        data_int = data_int >> 1
                    if not self.isCovered(row, column - 1):
                        self.matrix[row][column - 1] = data_int & 0b1
                        data_int = data_int >> 1

                                
            else: # Going down
                for row in range(self.shape):

                    if row == 6: # Timing Pattern 
                        continue

                    if not self.isCovered(row, column):
                        self.matrix[row][column] = data_int & 0b1
                        data_int = data_int >> 1
                    if not self.isCovered(row, column - 1):
                        self.matrix[row][column - 1] = data_int & 0b1
                        data_int = data_int >> 1

            column -= 2 # Generally, skipping two columns
            counter += 1
            


    def evaluate(self, matrix):
        # This function evaluates a given function and returns its penalty score based on four evaluation conditions
        penalties = [0, 0, 0, 0]

        row_counter = 0
        column_counter = 0
        black_counter = 0
        for row in range(self.shape):
            for column in range(self.shape):

                # EVALUATION CONDITION 0
                # For every row and column, check 
                # If there are five consecutive modules of the same color, add 3 to the penalty. 
                # If there are more modules of the same color after the first five, add 1 for each additional module of the same color
                # Since this is a square, I can loop through row and column at the same time just by swapping them

                # Checking for rows
                bit = matrix[row][column]
                if bit == BLACK:
                    row_counter += 1

                    if row_counter == 3:
                        penalties[0] += 3

                    elif row_counter > 3:
                        penalties[0] += 1

                else:
                    row_counter == 0
            
                # Checking for columns
                bit = matrix[column][row]
                if bit == BLACK:
                    column_counter += 1

                    if column_counter == 3:
                        penalties[0] += 3

                    elif column_counter > 3:
                        penalties[0] += 1

                else:
                    column_counter == 0

                # EVALUATION CONDITION 1
                # Add 3 to the penalty score for every 2x2 block of the same color in the QR code, 
                # making sure to count overlapping 2x2 blocks
                # To do this, I'm only looking for even rows and columns for every bit verifying its adjacent bits
                if row % 2 == 0 and column % 2 == 0:
                    bit = matrix[row][column]

                    if column - 1 > 0 and column + 1 < self.shape and row - 1 > 0 and row + 1 < self.shape:
                        bit_l = matrix[row][column - 1]
                        bit_r = matrix[row][column + 1]

                        if bit_l == bit_r and bit != bit_r: # If there are no similar colors, there is no need to check
                            continue

                        bit_lu = matrix[row - 1][column - 1]
                        bit_ld = matrix[row + 1][column - 1]
                        bit_ru = matrix[row - 1][column + 1]
                        bit_rd = matrix[row + 1][column + 1]
                    
                    else:

                        if column - 1 > 0:
                            bit_l = matrix[row][column - 1] # bit left

                            if row - 1 > 0:
                                bit_u = matrix[row - 1][column] # bit up
                                bit_lu = matrix[row - 1][column - 1] # bit left up 
                            else:
                                bit_lu = bit_u = -1
                                
                            if row + 1 < self.shape:
                                bit_d = matrix[row + 1][column] # bit down           
                                bit_ld = matrix[row + 1][column - 1] # bit down left
                            else:
                                bit_d = bit_ld = -1

                        else:
                            bit_l = bit_lu = bit_ld = -1

                        if column + 1 < self.shape:
                            bit_r = matrix[row][column + 1] # bit right
                            if row - 1 > 0:
                                bit_u = matrix[row - 1][column] # bit up
                                bit_ru = matrix[row - 1][column + 1] # bit right up 
                            else:
                                bit_ru = bit_u = -1
                                
                            if row + 1 < self.shape:
                                bit_d = matrix[row + 1][column] # bit down           
                                bit_rd = matrix[row + 1][column + 1] # bit right down
                            else:
                                bit_d = bit_rd = -1

                        else:
                            bit_r = bit_ru = bit_rd = -1

                    # Checking 2x2 area
                    if bit_l != bit and bit != bit_r: # If there are no similar colors, there is no need to check
                        continue

                    if bit_l == bit and (bit_l == bit_lu == bit_u or bit_l == bit_ld == bit_d): # Left half
                        penalties[1] += 3
                    if bit_r == bit and (bit_r == bit_ru == bit_u or bit_r == bit_rd == bit_d): # Right half
                        penalties[1] += 3

                # EVALUATION CONDITION 2
                # This evaluation looks for patterns of BWBBBWBWWWW or WWWWBWBBBWB in rows or columns    
                    
                if row <= self.shape - 11 and column <= self.shape - 11:
                    
                    for i in range(2):
                        row_act = row
                        column_act = column
                        if i == 1: # Checking for the columns by inverting the rows
                            row_act = column
                            column_act = row

                    bit = matrix[row_act][column_act]
                    # Looking for the pattern
                    if bit == BLACK:
                        if matrix[row_act][column_act + 1] == matrix[row_act][column_act + 5] == matrix[row_act][column_act + 7] == matrix[row_act][column_act + 8] == matrix[row_act][column_act + 9] == matrix[row_act][column_act + 10] == WHITE and matrix[row_act][column_act + 2] == matrix[row_act][column_act + 3] == matrix[row_act][column_act + 4] == matrix[row_act][column_act + 6] == BLACK:
                            
                            penalties[2] += 40

                    else:
                        if matrix[row_act][column_act + 1] == matrix[row_act][column_act + 2] == matrix[row_act][column_act + 3] == matrix[row_act][column_act + 5] == matrix[row_act][column_act + 9] == WHITE and matrix[row_act][column_act + 4] == matrix[row_act][column_act + 6] == matrix[row_act][column_act + 7] == matrix[row_act][column_act + 8] == matrix[row_act][column_act + 10] == BLACK:

                            penalties[2] += 40

                # EVALUATION CONDICTION 3
                # This condition is based on the ratio of dark modules and white modules
                if matrix[row][column] == BLACK: black_counter += 1
        
        total_modules = self.shape ** 2
        black_perc = (black_counter / total_modules) * 100
        val_1 = abs((black_perc - (black_perc % 5)) - 50) / 5 # 50 - 'previous multiple of 50' / 5
        val_2 = abs((black_perc + (5 - black_perc % 5)) - 50) / 5 # 50 - 'next multiple of 50' / 5

        if val_1 < val_2:
            penalties[3] = int(val_1 * 10)
        else:
            penalties[3] = int(val_2 * 10)

        return sum(penalties)


    def data_mask(self):
        # After encoding the data, eight masks must be applied to it and evaluated based on four conditions
        # The evaluation gives it a penalty score. The lowest penalty score wins.
        # RETURNS THE MASK NUMBER and SETS THE BEST MATRIX TO SELF.MATRIX

        # Mask Number / If the formula below is true for a given row/column coordinate, switch the bit at that coordinate
        # 0	(row + column) mod 2 == 0
        # 1	(row) mod 2 == 0
        # 2	(column) mod 3 == 0
        # 3	(row + column) mod 3 == 0
        # 4	( floor(row / 2) + floor(column / 3) ) mod 2 == 0
        # 5	((row * column) mod 2) + ((row * column) mod 3) == 0
        # 6	( ((row * column) mod 2) + ((row * column) mod 3) ) mod 2 == 0
        # 7	( ((row + column) mod 2) + ((row * column) mod 3) ) mod 2 == 0
        # This table is available at https://www.thonky.com/qr-code-tutorial/mask-patterns

        # This is an array of matrices that are going to be altered at the same time, consuming memory but only going
        # through the matrix a single time: O(n^2)
        # Another option would be to have a single matrix and run through it multiple times, evaluating and reseting it
        # after each evaluation, which would cost time O(7 * n^2). This does simplify to O(n^2) for greater values of n,
        # but to keep the code more clear and save a little time, I chose the first option.
        matrices = []
        for _ in range(8):
            m = []
            for i in range(self.shape):
                m.append(self.matrix[i].copy())
            matrices.append(m)

        # DATA MASKS
        for row in range(self.shape):
            for column in range(self.shape):

                if self.isCovered(row, column): # The reserved areas should not be masked
                    continue

                if (row + column) % 2 == 0:                                 # Data mask 0
                    matrices[0][row][column] = 1 - matrices[0][row][column]
                if row % 2 == 0:                                            # Data mask 1
                    matrices[1][row][column] = 1 - matrices[1][row][column]
                if column % 3 == 0:                                         # Data mask 2
                    matrices[2][row][column] = 1 - matrices[2][row][column]
                if (row + column) % 3:                                      # Data mask 3
                    matrices[3][row][column] = 1 - matrices[3][row][column]
                if (floor(row / 2) + floor(column / 3)) % 2 == 0:           # Data mask 4
                    matrices[4][row][column] = 1 - matrices[4][row][column]
                if ((row * column) % 2) + ((row * column) % 3) == 0:        # Data mask 5
                    matrices[5][row][column] = 1 - matrices[5][row][column]
                if (((row * column) % 2) + ((row * column) % 3) ) % 2 == 0: # Data mask 6
                    matrices[6][row][column] = 1 - matrices[6][row][column]
                if (((row + column) % 2) + ((row * column) % 3) ) % 2 == 0: # Data mask 7
                    matrices[7][row][column] = 1 - matrices[7][row][column]

        # for m in matrices:
        #     show_code(m)

        penalties = []
        for i in range(8):
            penalties.append(self.evaluate(matrices[i]))


        best_matrix = matrices[penalties.index(min(penalties))]
        self.matrix = best_matrix
        self.mask_number = penalties.index(min(penalties))
        return self.mask_number


    def format_string(self):
        ec_bits = EC_BITS.get(self.ec)
        mask_number = self.mask_number
        format_bin = ((ec_bits << 3) + mask_number) << 10 # Concatenating the bits
        format_s = format((ec_bits << 3) + mask_number, 'b')

        generator = 0b10100110111

        while(ceil(log2(format_bin)) >= 11):
            
            generator_padded = generator << (ceil(log2(format_bin)) - ceil(log2(generator)))
            format_bin = format_bin ^ generator_padded

        aux = format(format_bin, 'b')
        aux = ('0' * (10 - len(aux))) + aux 
        format_s = format_s + aux

        format_s = format(int(format_s, base=2) ^ 0b101010000010010, 'b')          # XOR the result with the mask string
        return format_s


    def format_version(self):
        format_s = self.format_string()
        positions = {   # 0 are the most significant bytes positions and 14 the least significant one 
            0: [(8, 0), (self.shape - 1, 8)],
            1: [(8, 1), (self.shape - 2, 8)],
            2: [(8, 2), (self.shape - 3, 8)],
            3: [(8, 3), (self.shape - 4, 8)],
            4: [(8, 4), (self.shape - 5, 8)],
            5: [(8, 5), (self.shape - 6, 8)],
            6: [(8, 7), (self.shape - 7, 8)],
            7: [(8, 8), (8, self.shape - 8)],
            8: [(7, 8), (8, self.shape - 7)],
            9: [(5, 8), (8, self.shape - 6)],
            10: [(4, 8), (8, self.shape - 5)],
            11: [(3, 8), (8, self.shape - 4)],
            12: [(2, 8), (8, self.shape - 3)],
            13: [(1, 8), (8, self.shape - 2)],
            14: [(0, 8), (8, self.shape - 1)]
            }

        for i in range(len(format_s)):

            self.matrix[positions[i][0][0]][positions[i][0][1]] = int(format_s[i])
            self.matrix[positions[i][1][0]][positions[i][1][1]] = int(format_s[i])


    def quiet_zone(self):
        # Adds a required 4-module-wide area of white modules to the matrix
        final_matrix = []
        white_row = []
        for _ in range(self.shape + 8):
            white_row.append(WHITE)

        # 4 rows top padding
        for _ in range(4):
            final_matrix.append(white_row)

        # Left and right padding
        for i in range(self.shape):
            row = []
            for j in range(self.shape + 8):
                if j < 4 or j >= self.shape + 4:
                    row.append(WHITE)
                else:
                    row.append(self.matrix[i][j - 4])
            
            final_matrix.append(row)

        # 4 rows bottom padding
        for _ in range(4):
            final_matrix.append(white_row)

        self.matrix = final_matrix
        return final_matrix
    
    #endregion


qr = QRCode('HELLO WORLD', 'Alphanumeric', 1, 'L')

## ENCODING THE RAW DATA
qr.set_mode()
qr.character_count()
qr.alpha_conversion()
qr.terminator()
qr.padding()
qr.data_codewords()

## ERROR CODEWORDS
qr.get_eccodewords()
qr.place_eccodewords()

# TODO Add remainder bits
# -> For larger QR Codes (those which have more than one block) it is necessary to interleave the data and the
#   error correction codewords. For now, this step is going to be skipped

## QR CODE STRUCTURE
# For versions greater than 1, an alignment pattern is necessary. 
# https://www.thonky.com/qr-code-tutorial/alignment-pattern-locations

qr.finder_pattern()
qr.data_placement()
qr.data_mask()
qr.format_version()
qr.quiet_zone()
print(qr.mask_number)
qr.show_code()

# I've come up with three ways to avoid the occupied areas when adding the data to the QR Code
# - The first one is to keep an array with the covered areas (start, height, width), but that would make it necessary
#   to go thorough the array for every module of the QR Code, which would not be very fast.
# - The second option would be to create have a position and and occuppied boolean for every module of the QR Code
#   This would make it easier to make verifications, but would take up a lot of memory.
# For now, I think the array is a better ideia, since most of the covered areas are fixed.