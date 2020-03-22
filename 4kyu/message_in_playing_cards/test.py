from solution import message_to_lex, lex_to_message


def test_message_to_lex():
    assert message_to_lex('A ') == 27;
    assert message_to_lex('AA') == 28;
    assert message_to_lex('AB') == 29;
    assert message_to_lex('ABC') == 786;

def test_lex_to_message():
    assert lex_to_message(1075557286316151030417832078639107526) == 'ATTACK TONIGHT ON CODEWARS'

# def test_a_encode():
#     message = "A"
#     deck = [
#         "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC",
#         "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD",
#         "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "TH", "JH", "QH", "KH",
#         "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "TS", "JS", "KS", "QS"
#     ]
#     assert playingCards.encode(message) == deck


# def test_attack_tonight_on_codewars_encode():
#     message = "ATTACK TONIGHT ON CODEWARS"
#     deck = [
#         "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC",
#         "AD", "2D", "3D", "4D", "5D", "6D", "JD", "9D", "7S", "9S", "QD", "5S", "TH",
#         "7D", "TS", "QS", "2H", "JS", "6H", "3S", "6S", "TD", "8S", "2S", "8H", "7H",
#         "4S", "4H", "3H", "5H", "AS", "KH", "QH", "9H", "KD", "KS", "JH", "8D", "AH"
#     ]
#     assert playingCards.encode(message) == deck


# def test_a_decode():
#     deck = [
#         "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC",
#         "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD",
#         "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "TH", "JH", "QH", "KH",
#         "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "TS", "JS", "KS", "QS"
#     ]
#     message = "A"
#     assert playingCards.decode(deck) == message


# def test_attack_approved_decode():
#     deck = [
#         "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC",
#         "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD",
#         "AH", "2H", "3H", "4H", "8H", "9S", "3S", "2S", "8S", "TS", "QS", "9H", "7H",
#         "KH", "AS", "JH", "4S", "KS", "JS", "5S", "TH", "7S", "6S", "5H", "QH", "6H"
#     ]
#     message = "ATTACK APPROVED"
#     assert playingCards.decode(deck) == message
