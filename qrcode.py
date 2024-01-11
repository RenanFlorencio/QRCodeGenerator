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

# Talvez criar uma classe string que contém as funções de acordo com a versão do QR code que está sendo usado
class QRCode():
    def __init__(self, data, mode, version):
        self._version = version
        self._data = data
        self._string = []
        self._mode = mode

    def set_mode(self):
        self._string.append(MODE_INDICATOR_TABLE.get(self._mode)) # 9 bits for versions 1 through 9

    def character_count(self):

        if self._version >= 1 and self._version <= 9:
            
            if self._mode == 'Alphanumeric':

                bin = format(len(self._data), 'b')
                self._string.append (('0' * (9 - len(bin)) + bin))
        

    def alpha_conversion(self):
        
        if self._mode != 'Alphanumeric':
            return

        for i in range(0, len(self._data), 2):
            pass



qr = QRCode('HELLO', 'Alphanumeric', 1)
qr.set_mode()
qr.character_count()
print(qr._string)