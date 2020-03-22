import re
import itertools
import math
import string
import pdb

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

test_deck_52_m_1 = ['KS', 'QS', 'JS', 'TS', '9S', '8S', '7S', '6S', '5S', '4S', '3S', '2S', 'AS', 'KH', 'QH', 'JH', 'TH', '9H', '8H', '7H', '6H', '5H', '4H', '3H', '2H', 'AH', 'KD', 'QD', 'JD', 'TD', '9D', '8D', '7D', '6D', '5D', '4D', '3D', '2D', 'AD', 'KC', 'QC', 'JC', 'TC', '9C', '8C', '7C', '6C', '5C', '4C', '3C', '2C', 'AC']


class PlayingCards:

    # Create a lexical ordering of cards
    # deck = [ f'{rank}{suit}' for suit in 'CDHS' for rank in 'A23456789TJQK' ]
    deck = [
        "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC",
        "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD",
        "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "TH", "JH", "QH", "KH",
        "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "TS", "JS", "QS", "KS"
    ]
    chars = " " + string.ascii_uppercase[:26]
    places = [ pow(27, place) for place in range(0, 52) ]
    MAX_LEX_CODE = 80658175170943878571660636856403766975289505440883277824000000000000
    FACT = [ math.factorial(i) for i in range(0, 52) ]

    @staticmethod
    def lex(msg):
        place = 0
        lex_code = 0
        if msg == '':
            return 0
        if not re.fullmatch('[ A-Z]+', msg):
            return None
        digits = [PlayingCards.chars.index(letter) for letter in msg]
        for digit in reversed(digits):
            lex_code += digit * pow(27, place)
            place += 1
        if lex_code > PlayingCards.MAX_LEX_CODE:
            return None
        return lex_code

    @staticmethod
    def message(lex_code):
        message_str = ''
        for place in reversed(PlayingCards.places):
            digit = math.floor(lex_code / place)
            if digit >= 0:
                message_str = message_str + PlayingCards.chars[digit]
                lex_code = lex_code - digit * place
        return message_str.lstrip()

    @staticmethod
    def int_to_factoradic(lex_code):
        q = lex_code
        coeffs = []
        for i in itertools.count(start=1):
            q, r = divmod(q, i)
            coeffs.append(r)
            if q == 0 and len(coeffs) == 52:
                break
        coeffs.reverse()
        return coeffs

    @staticmethod
    def factoradic_to_int(coeffs):
        return sum(PlayingCards.FACT[i] * v for i, v in enumerate(reversed(coeffs)))

    @staticmethod
    def deck_to_factoradic(enc_deck):
        f = []
        cdeck = PlayingCards.deck.copy()
        for i in itertools.count(start=0):
            digit = cdeck.index(enc_deck[i]);
            f.append(digit)
            cdeck.remove(enc_deck[i])
            if len(cdeck) == 0:
                break
        return f

    @staticmethod
    def perm(f):
        d = PlayingCards.deck.copy()
        res = []
        for p in f:
            res.append(d[p])
            del d[p]
        return res

    @staticmethod
    def encode(message):
        lex_code = PlayingCards.lex(message)
        if lex_code is None:
            return None
        f = PlayingCards.int_to_factoradic(lex_code)
        return PlayingCards.perm(f)

    @staticmethod
    def decode(deck):
        f = PlayingCards.deck_to_factoradic(deck)
        PlayingCards.print_factoradic(f)
        lex_code = PlayingCards.factoradic_to_int(f)
        return PlayingCards.message(lex_code)

    @staticmethod
    def print_place():
        print('place  -> ', end=' ')
        for i in range(0, 52):
            print('{:02d}'.format(i), end=' ')
        print()

    @staticmethod
    def print_factoradic(fd):
        print('factor -> ', end=' ')
        for i, f in enumerate(fd):
            print('{:02d}'.format(f), end=' ')
        print()

    @staticmethod
    def print_deck(deck):
        print('result -> ', end=' ')
        for elt in deck:
            print(f'{str(elt)}', end=' ')
        print()

    @staticmethod
    def printdeck(fd, deck, testdeck):
        PlayingCards.print_place()
        PlayingCards.print_factoradic(fd)
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

print()
p = PlayingCards
# lex = p.lex('I CANT WAIT TO C MY QT BUT HES AT THE STORE')
# f = p.int_to_factoradic(lex)
# i = p.factoradic_to_int(f)
# e = p.encode('I CANT WAIT TO C MY QT BUT HES AT THE STORE')
# p.print_deck(e)
# f = p.deck_to_factoradic(e)
# p.print_factoradic(f)
e = p.encode('I CANT WAIT TO C MY QT BUT HES AT THE STORE')
d = p.decode(e)
print(d)
print()

#d = PlayingCards.encode('MY QT IS THE BEST')
#PlayingCards.print_deck(d)
#m = PlayingCards.decode(d)
#print(m)
#PlayingCards.decode(test_deck_a)
#f = PlayingCards.deck_to_factoradic(test_deck_52_m_1)
#PlayingCards.print_factoradic(f)
#l = PlayingCards.lex('DGWBJJDTKUUVXWQNFNWVSEEVDVOHDMUVMDQMCRXDQZZZZZZZ')
#print(lex_code)
#f = PlayingCards.deck_to_factoradic(test_deck_52_m_1)
#i = PlayingCards.factoradic_to_int(f)
#print(l)
#print(i)
#m = PlayingCards.message(i)
#print(m)
#print(PlayingCards.encode('ABC?DEF'))
#lex_code = lex('ATTACK TONIGHT ON CODEWARS')
#lex_code = lex('A')
#f = factoradic(lex_code)
#printdeck(f, perm(f), test_deck_attack)
#f = PlayingCards.lex_to_factoradic(lex_code)
#PlayingCards.printdeck(f, PlayingCards.perm(f), test_deck_52_m_1)
#printdeck(f, kth_perm(deck, f), deck)
#print(chars)
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
