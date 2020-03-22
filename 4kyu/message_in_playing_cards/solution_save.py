import itertools
import math
import string
import pdb;

# Create a lexical ordering of cards
deck = [ f'{rank}{suit}' for suit in 'CDHS' for rank in 'A23456789TJQK' ]
chars = " " + string.ascii_uppercase[:26]
places = [ pow(27, place) for place in range(0, 52) ]

test_deck_attack = [
         "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC",
         "AD", "2D", "3D", "4D", "5D", "6D", "JD", "9D", "7S", "9S", "QD", "5S", "TH",
         "7D", "TS", "QS", "2H", "JS", "6H", "3S", "6S", "TD", "8S", "2S", "8H", "7H",
         "4S", "4H", "3H", "5H", "AS", "KH", "QH", "9H", "KD", "KS", "JH", "8D", "AH"
]

test_deck_a = [
    "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC",
    "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD",
    "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "TH", "JH", "QH", "KH",
    "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "TS", "JS", "KS", "QS"
]

test_deck_approved = [
    "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC",
    "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD",
    "AH", "2H", "3H", "4H", "8H", "9S", "3S", "2S", "8S", "TS", "QS", "9H", "7H",
    "KH", "AS", "JH", "4S", "KS", "JS", "5S", "TH", "7S", "6S", "5H", "QH", "6H"
]


# Translate a message to the lexical ordering
def lex(msg):
    place = 0
    lex_code = 0
    digits = [chars.index(letter) for letter in msg]
    for digit in reversed(digits):
        lex_code += digit * pow(27, place)
        place += 1
    return lex_code


# Translate a lexical ordering to message
def message(lex_code):
    message_str = ''
    for place in reversed(places):
        digit = math.floor(lex_code / place)
        if digit >= 0:
            message_str = message_str  + chars[digit]
            lex_code = lex_code - digit * place
    return message_str.lstrip()


def deck_to_lex(deck):
    pass


# Translate lex to a lehmer code
def lehmer(lex_code):
    lehmer_code = []
    started = False
    for place in reversed(places):
        digit = math.floor(lex_code / place)
        if digit >= 1 or started:
            started = True
            lehmer_code.append(digit)
            lex_code = lex_code - digit * place
    for i in range(1, len(lehmer_code)):
        print(lehmer_code)
        lehmer_code =  [ elt-1 if idx > i and elt > 0 else elt
                         for idx, elt in enumerate(lehmer_code) ]
    while len(lehmer_code) < len(deck):
        lehmer_code.insert(0, 0)
    return lehmer_code


def lstrip(lst):
    res = lst.copy()
    for idx, elt in enumerate(res):
        if elt > 0:
            return res
        del res[idx]


def factoradic(lex_code):
    factoradic = []
    for place in range(1, 52):
        factoradic.insert(0, lex_code % place)
        lex_code = math.floor(lex_code / place)
    factoradic.insert(0, 0)
    return factoradic


def factoradic_str(lex_code):
    f = factoradic(lex_code)
    return ",".join(str(elt) for elt in f)

# subtract 1 from all elements in a list after i
def sub_one(lst, i):
    return [ elt-1 if idx > i and elt > 0 else elt for idx, elt in enumerate(lst) ]


# Takes a String containing a message, and returns an array of Strings representing
# a deck of playing cards ordered to hide the message, or None if the message is invalid.
def encode(message):
    lex_code = lex(message)
    fac = factoradic(lex_code)
    print(fac)
    d = deck.copy()
    res = []
    for f in fac:
        res.append(d[f])
        del d[f]
    return res


def kth_perm(s, f):
    sl = s.copy()
    res = []
    for p in f:
        print('p: ' + str(p))
        print('res: ' + ' '.join(res))
        print('sl: ' + ' '.join(sl))
        res.append(sl[p])
        del sl[p]
        pdb.set_trace()
    return res

# Takes an array of Strings representing a deck of playing cards, and returns
# the message that is hidden inside, or None if the deck is invalid.
def decode(deck):
    return None


def printdeck(fd, deck, testdeck):
    errors=' '
    print('place  -> ', end=' ')
    for i in range(0, 52):
        print('{:02d}'.format(i), end=' ')
    print()
    print('factor -> ', end=' ')
    for i, f in enumerate(fd):
        print('{:02d}'.format(f), end=' ')
        errors += '-- ' if deck[i] != testdeck[i] else '   '
    print()
    print('errors -> ' + errors)
    count = 0
    test_str = 'test   ->  '
    print('result -> ', end=' ')
    for elt in deck:
        print(f'{str(elt)}', end=' ')
        test_str += testdeck[count] + ' '
        count += 1
    print()
    print(test_str)
    print()
    test_str = ''


lex_code = lex('ATTACK TONIGHT ON CODEWARS')
#lex_code = lex('A')
f = factoradic(lex_code)
printdeck(f, kth_perm(deck, f), test_deck_attack)
#printdeck(f, kth_perm(deck, f), deck)
print(chars)
#lex_code = lex('ATTACK APPROVED')
#f = factoradic(lex_code)
#printdeck(f, kth_perm(deck, f), test_deck_approved)

#print(message_to_lex('A'))
#print(message_to_lex('ATTACK TONIGHT ON CODEWARS'))
#lehmercode = lehmer(lexcode)
#factoradic_lst = factoradic(lexcode)
#message_str = message(lexcode)
#print(message_str)
#print(lexcode)
#print(lehmercode)
#print(deck)
#print(factoradic_lst)
#print(factoradic(463))
#d = encode('ATTACK TONIGHT ON CODEWARS')
#print(d)
#print(len(d))
#print(len(deck))
#per = [''.join(str(x) for x in p) for p in itertools.permutations('1234')]
#print(per)
#f = [factoradic_str(i)[-4:] for i in range(0, 24)]
#print(f)
#print(len(f))
#print(kth_perm('1234', f[7]))
