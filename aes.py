Nb = 4      # Block size in Words
Nr = 14     # Number of Rounds
Nk = 8      # Key Length in Words

SBox = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

def KeyExpansion(key):
    w = [None] * Nb*(Nr+1)
    for i in xrange(0, Nk):
        w[i]    = [key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]]

    for i in xrange(Nk, Nb*(Nr+1)):
        temp = [None] * 4
        temp[0] = w[i-1][0]
        temp[1] = w[i-1][1]
        temp[2] = w[i-1][2]
        temp[3] = w[i-1][3]

        if(i % Nk == 0):
            RotWord(temp)
            SubWord(temp)
            temp = XorWords(temp, RCon(i/Nk))
        elif(Nk > 6 and i % Nk == 4):
            SubWord(temp)
        w[i] = XorWords(w[i-Nk], temp)
    return w

def RCon(i):
    c = 1
    if(i == 0):
        return 0
    for j in xrange(0, i-1):
        c = GaloisMultiply(0x02, c)
    return [c, 0x0, 0x0, 0x0]

def XorWords(a, b):
    c = [None] * 4
    for i in xrange(0, 4):
        c[i] = a[i] ^ b[i]
    return c

def SubWord(word):
    for i in xrange(0, 4):
        word[i] = SBox[word[i]]

def RotWord(word):
    first = word[0]
    for i in xrange(0, 3):
        word[i] = word[i+1]
    word[3] = first

def Cipher(plaintext, key):
    w = KeyExpansion(key)

    state = [None] * 4
    for row in xrange(0, 4):
        state[row] = [None]*Nb
        for col in xrange(0, Nb):
            state[row][col] = plaintext[row + 4*col]

    AddRoundKey(state, w, 0)   # Sec 5.1.4

    for r in xrange(1, Nr):
        SubBytes(state)             # Sec 5.1.1
        ShiftRows(state)            # Sec 5.1.2
        MixColumns(state)           # Sec 5.1.3
        AddRoundKey(state, w, r)

    SubBytes(state)
    ShiftRows(state)
    AddRoundKey(state, w, Nr)

    out = [None] * Nb*4
    for row in xrange(0, 4):
        for col in xrange(0, Nb):
            out[row + 4*col] = state[row][col]
    return out

def SubBytes(state):
    for row in xrange(0, 4):
        for col in xrange(0, Nb):
            state[row][col] = SBox[state[row][col]]

def ShiftRows(state):
    for row in xrange(1, 4):
        for i in xrange(0, row):
            first = state[row][0]
            for col in xrange(0, Nb - 1):
                state[row][col] = state[row][col+1]
            state[row][Nb-1] = first

def MixColumns(state):
    temp = [None] * 4
    for col in xrange(0, Nb):
        temp[0] = GaloisMultiply(0x02, state[0][col]) ^ GaloisMultiply(0x03, state[1][col]) ^ \
                  GaloisMultiply(0x01, state[2][col]) ^ GaloisMultiply(0x01, state[3][col])

        temp[1] = GaloisMultiply(0x01, state[0][col]) ^ GaloisMultiply(0x02, state[1][col]) ^ \
                  GaloisMultiply(0x03, state[2][col]) ^ GaloisMultiply(0x01, state[3][col])

        temp[2] = GaloisMultiply(0x01, state[0][col]) ^ GaloisMultiply(0x01, state[1][col]) ^ \
                  GaloisMultiply(0x02, state[2][col]) ^ GaloisMultiply(0x03, state[3][col])

        temp[3] = GaloisMultiply(0x03, state[0][col]) ^ GaloisMultiply(0x01, state[1][col]) ^ \
                  GaloisMultiply(0x01, state[2][col]) ^ GaloisMultiply(0x02, state[3][col])

        state[0][col] = temp[0]
        state[1][col] = temp[1]
        state[2][col] = temp[2]
        state[3][col] = temp[3]

# Multiplication GF(2^8) where a in {01, 02, 03}
def GaloisMultiply(a, b):
    if a == 0x01: return b
    if a == 0x02:
        if b & 0x80:
            return ((b << 1) % 256) ^ 0x1B
        else:
            return (b << 1) % 256
    if a == 0x03:
        tmp = b
        if b & 0x80:
            b = (b << 1) % 256
            b ^= 0x1B
        else:
            b = (b << 1) % 256
        return tmp ^ b


def AddRoundKey(state, w, r):
    for col in xrange(0, Nb):
        column = [state[0][col],state[1][col],state[2][col],state[3][col]]
        temp = XorWords(column, w[r*Nb+col])
        state[0][col] = temp[0]
        state[1][col] = temp[1]
        state[2][col] = temp[2]
        state[3][col] = temp[3]


#######################################
#### TESTS TESTS TESTS TESTS TESTS ####
#######################################
def Test_SubWord():
    word = [0x30,0x21,0x12,0x03]
    sub  = [0x04,0xFD,0xC9,0x7B]
    SubWord(word)
    assert word == sub

def Test_RotWord():
    word = [0x30,0x21,0x12,0x03]
    sub  = [0x21,0x12,0x03,0x30]
    RotWord(word)
    assert word == sub

def Test_KeyExpansion():
    key = [0x60, 0x3d, 0xeb, 0x10, 0x15, 0xca, 0x71, 0xbe, 0x2b, 0x73, 0xae, 0xf0, 0x85, 0x7d, 0x77, 0x81,
           0x1f, 0x35, 0x2c, 0x07, 0x3b, 0x61, 0x08, 0xd7, 0x2d, 0x98, 0x10, 0xa3, 0x09, 0x14, 0xdf, 0xf4]
    w = KeyExpansion(key)
    assert w[59] == [0x70, 0x6c, 0x63, 0x1e]
    assert w[26] == [0x24, 0x36, 0x0a, 0xf2]
    assert w[40] == [0xde, 0x13, 0x69, 0x67]

def Test_SubBytes():
    state = [[0x30,0x21,0x12,0x03],
             [0x74,0x65,0x56,0x47],
             [0xB8,0xA9,0x9A,0x8B],
             [0xFC,0xED,0xDE,0xCF]]
    SubBytes(state)
    sub   = [[0x04,0xFD,0xC9,0x7B],
             [0x92,0x4D,0xB1,0xA0],
             [0x6C,0xD3,0xB8,0x3D],
             [0xB0,0x55,0x1D,0x8A]]
    assert state == sub

def Test_ShiftRows():
    state = [[0x00,0x01,0x02,0x03],
             [0x04,0x05,0x06,0x07],
             [0x08,0x09,0x0A,0x0B],
             [0x0C,0x0D,0x0E,0x0F]]
    shift = [[0x00,0x01,0x02,0x03],
             [0x05,0x06,0x07,0x04],
             [0x0A,0x0B,0x08,0x09],
             [0x0F,0x0C,0x0D,0x0E]]
    ShiftRows(state)
    assert state == shift

def Test_GaloisMultiply():
    assert GaloisMultiply(0x02, 0xD4) == 0xB3
    assert GaloisMultiply(0x03, 0xBF) == 0xDA
    assert GaloisMultiply(0x01, 0x5D) == 0x5D
    assert GaloisMultiply(0x01, 0x30) == 0x30

def Test_MixColumns():
    state = [[0xdb,0xF2,0x01,0xc6],
             [0x13,0x0A,0x01,0xc6],
             [0x53,0x22,0x01,0xc6],
             [0x45,0x5C,0x01,0xc6]]
    mixed = [[0x8e,0x9F,0x01,0xc6],
             [0x4d,0xDC,0x01,0xc6],
             [0xa1,0x58,0x01,0xc6],
             [0xbc,0x9D,0x01,0xc6]]
    MixColumns(state)
    assert state == mixed

def Test_Cipher():
    plaintext = [0x00,0x11,0x22,0x33,
                 0x44,0x55,0x66,0x77,
                 0x88,0x99,0xaa,0xbb,
                 0xcc,0xdd,0xee,0xff]
    key       = [0x00,0x01,0x02,0x03,
                 0x04,0x05,0x06,0x07,
                 0x08,0x09,0x0a,0x0b,
                 0x0c,0x0d,0x0e,0x0f,
                 0x10,0x11,0x12,0x13,
                 0x14,0x15,0x16,0x17,
                 0x18,0x19,0x1a,0x1b,
                 0x1c,0x1d,0x1e,0x1f]
    output = Cipher(plaintext, key)
    ciphertext= [0x8e,0xa2,0xb7,0xca,
                 0x51,0x67,0x45,0xbf,
                 0xea,0xfc,0x49,0x90,
                 0x4b,0x49,0x60,0x89]
    assert output == ciphertext

def TestApp(verbose = True):
    count = 0
    if verbose: print "Running tests..."
    try:
        Test_ShiftRows()
    except AssertionError:
        count += 1
        if verbose: print "-\tShiftRows: FAIL"
    else:
        if verbose: print "+\tShiftRows: PASS"

    try:
        Test_SubBytes()
    except AssertionError:
        count += 1
        if verbose: print "-\tSubBytes: FAIL"
    else:
        if verbose: print "+\tSubBytes: PASS"

    try:
        Test_GaloisMultiply()
    except AssertionError:
        count += 1
        if verbose: print "-\tGaloisMultiply: FAIL"
    else:
        if verbose: print "+\tGaloisMultiply: PASS"

    try:
        Test_MixColumns()
    except AssertionError:
        count += 1
        if verbose: print "-\tMixColumns: FAIL"
    else:
        if verbose: print "+\tMixColumns: PASS"

    try:
        Test_SubWord()
    except AssertionError:
        count += 1
        if verbose: print "-\tSubWord: FAIL"
    else:
        if verbose: print "+\tSubWord: PASS"

    try:
        Test_RotWord()
    except AssertionError:
        count += 1
        if verbose: print "-\tRotWord: FAIL"
    else:
        if verbose: print "+\tRotWord: PASS"

    try:
        Test_KeyExpansion()
    except AssertionError:
        count += 1
        if verbose: print "-\tKeyExpansion: FAIL"
    else:
        if verbose: print "+\tKeyExpansion: PASS"

    try:
        Test_Cipher()
    except AssertionError:
        count += 1
        if verbose: print "-\tCipher: FAIL"
    else:
        if verbose: print "+\tCipher: PASS"

    if(count > 0):
        print "%d tests failed" % count
        exit()
    else:
        print "All tests passed!"

def _printState(state):
    for row in xrange(0, 4):
        for col in xrange(0, Nb):
            print "%s " % format(state[row][col], '02x'),
        print "\n",

def _printExpandedKey(w):
    for i in xrange(0, Nb*(Nr+1)):
        print "%d: " % i,
        for j in xrange(0, 4):
            print "%s" % format(w[i][j], '02x'),
        print "\n",

def _printText(input):
    for i in xrange(0, Nb*4):
        print "%s" % format(input[i], '02x'),
    print

TestApp()
