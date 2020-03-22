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
    def factoradic(lex_code):
        q = lex_code
        coeffs = []
        for i in itertools.count(start=1):
            q, r = divmod(q, i)
            coeffs.append(r)
            if q == 0 and len(coeffs) == 52:
                break
        coeffs.reverse()
        return coeffs

    # Takes a String containing a message, and returns an array of Strings representing
    # a deck of playing cards ordered to hide the message, or None if the message is invalid.
    @staticmethod
    def encode(message):
        lex_code = PlayingCards.lex(message)
        if lex_code is None:
            return None
        f = PlayingCards.factoradic(lex_code)
        return PlayingCards.perm(f)

    @staticmethod
    def perm(f):
        d = PlayingCards.deck.copy()
        res = []
        for p in f:
            res.append(d[p])
            del d[p]
        return res

    # Takes an array of Strings representing a deck of playing cards, and returns
    # the message that is hidden inside, or None if the deck is invalid.
    @staticmethod
    def decode(deck):
        return None

    @staticmethod
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


print(PlayingCards.encode('ABC?DEF'))
#lex_code = lex('ATTACK TONIGHT ON CODEWARS')
#lex_code = lex('A')
#f = factoradic(lex_code)
#printdeck(f, perm(f), test_deck_attack)
#lex_code = PlayingCards.lex('DGWBJJDTKUUVXWQNFNWVSEEVDVOHDMUVMDQMCRXDQZZZZZZZ')
#f = PlayingCards.factoradic(lex_code)
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
