import re
import itertools
import math
import string


class PlayingCards:

    # LEXICALLY_ORDERED_DECK contains the lexical ordering of the playing card deck
    # In python 3.8 we could create the deck like this, but not in python 3.6
    # LEXICALLY_ORDERED_DECK = [ f'{rank}{suit}' for suit in 'CDHS' for rank in 'A23456789TJQK' ]
    LEXICALLY_ORDERED_DECK = [
        "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC",
        "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD",
        "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "TH", "JH", "QH", "KH",
        "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "TS", "JS", "QS", "KS"
    ]

    # ALPHABET is the list of characters we are allowed to use in the message
    ALPHABET = " " + string.ascii_uppercase[:26]

    # FACTORIALS is a memoized list of factorials so we will only have to compute it once
    FACTORIALS = [ math.factorial(i) for i in range(0, 53) ]

    # Given a message, determine which permutation of the deck will represent it
    # The permutation will be the base 27 representation converted to decimal.
    # To calculate this, we create an array of digits representing the values of each
    # letter in the message. We build up the base 27 number by multiplying by 27^place
    # (much like in base 10, you would multiply by 10^place). If the result is less
    # than the maximum allowable, return it.
    @staticmethod
    def to_permutation_number(message):
        if message == '':
            return 0
        if not re.fullmatch('[ A-Z]+', message):
            return None
        place = 0
        result = 0
        digits = [PlayingCards.ALPHABET.index(letter) for letter in message]
        for digit in reversed(digits):
            result += digit * pow(27, place)
            place += 1
        if result > PlayingCards.FACTORIALS[52]:
            return None
        return result

    # Get a message from the permutation number. Build up a list of place values and iterate
    # Build up the message when we find a digit by taking the value of the alphabet for that
    # digit. Remove the digit and continue.
    @staticmethod
    def from_permutation_number(permutation_number):
        message = ''
        for place in reversed([ pow(27, r) for r in range(0, 52) ]):
            digit = math.floor(permutation_number / place)
            if digit >= 0:
                message = message + PlayingCards.ALPHABET[digit]
                permutation_number = permutation_number - digit * place
        return message.lstrip()

    # Compute the factoradic from an integer. For the algorithm and background, see
    # https://en.wikipedia.org/wiki/Factorial_number_system
    @staticmethod
    def to_factoradic(permutation_number):
        coeffs = []
        for idx in itertools.count(start=1):
            permutation_number, remainder = divmod(permutation_number, idx)
            coeffs.append(remainder)
            if permutation_number == 0 and len(coeffs) == 52:
                break
        coeffs.reverse()
        return coeffs

    # Much easier to compute the integer from the factoradic, just multiply by the factorial
    # at it's place and sum the results.
    @staticmethod
    def from_factoradic(coeffs):
        return sum(PlayingCards.FACTORIALS[idx] * elt
                   for idx, elt in enumerate(reversed(coeffs)))

    # Convert a deck to a factoradic. Start with the lexically ordered deck and pick off the
    # element matching the first factoradic digit. Then remove the element from the lexically
    # ordered deck. Repeat the process until the lexically ordered deck is empty.
    @staticmethod
    def deck_to_factoradic(encoded_deck):
        coeffs = []
        ordered_deck = PlayingCards.LEXICALLY_ORDERED_DECK.copy()
        for elt in encoded_deck:
            digit = ordered_deck.index(elt)
            coeffs.append(digit)
            ordered_deck.remove(elt)
        return coeffs

    # Get the kth permutation of the deck from the factoradic. Once we know the factoradic
    # the kth permutation is calculated by taking the element from the ordered deck indexed
    # by the factoradic, then removing the element from the ordered deck. Repeat until the
    # deck is empty.
    @staticmethod
    def kth_permutation_of_deck(factoradic):
        ordered_deck = PlayingCards.LEXICALLY_ORDERED_DECK.copy()
        permuted_deck = []
        for lehman_code in factoradic:
            permuted_deck.append(ordered_deck[lehman_code])
            del ordered_deck[lehman_code]
        return permuted_deck

    # Test if the deck is valid by making sure each card in the lexically ordered deck
    # shows up exactly once
    @staticmethod
    def is_deck_valid(deck):
        for card in PlayingCards.LEXICALLY_ORDERED_DECK:
            if deck.count(card) != 1:
                return False
        return True

    # To encode we translate the message into an base 27 integer. We then convert the base 27 integer
    # into a factoradic / lehman code. Using the lehman code we build up the permutation that
    # cooresponds with the desired message.
    @staticmethod
    def encode(message):
        permutation_number = PlayingCards.to_permutation_number(message)
        if permutation_number is None:
            return None
        factoradic = PlayingCards.to_factoradic(permutation_number)
        return PlayingCards.kth_permutation_of_deck(factoradic)

    # To decode we translate the deck to a factoradic / lehman code. Using the lehman code we calculate
    # the base 27 integer representing the message. Finally, we translate that base 27 integer back to
    # the message.
    @staticmethod
    def decode(deck):
        if not PlayingCards.is_deck_valid(deck):
            return None
        factoradic = PlayingCards.deck_to_factoradic(deck)
        permutation_number = PlayingCards.from_factoradic(factoradic)
        return PlayingCards.from_permutation_number(permutation_number)

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
e = p.encode('DGWBJJDTKUUVXWQNFNWVSEEVDVOHDMUVMDQMCRXDQZZZZZZZ')
d = p.decode(e)
print(d)
print()
