from solution import Solution


def test_move_up_success():
    board = '412503'
    next_board = Solution.move(board, Solution.Direction.UP)
    assert '402513' == next_board


def test_move_up_fail():
    board = '402513'
    next_board = Solution.move(board, Solution.Direction.UP)
    assert '402513' == next_board


def test_move_right_success():
    board = '402513'
    next_board = Solution.move(board, Solution.Direction.RIGHT)
    assert '420513' == next_board


def test_move_right_fail():
    board = '420513'
    next_board = Solution.move(board, Solution.Direction.RIGHT)
    assert '420513' == next_board

    
def test_move_left_success():
    board = '402513'
    next_board = Solution.move(board, Solution.Direction.LEFT)
    assert '042513' == next_board


def test_move_left_fail():
    board = '042513'
    next_board = Solution.move(board, Solution.Direction.LEFT)
    assert '042513' == next_board


def test_move_down_success():
    board = '402513'
    next_board = Solution.move(board, Solution.Direction.DOWN)
    assert '412503' == next_board


def test_move_down_fail():
    board = '412503'
    next_board = Solution.move(board, Solution.Direction.DOWN)
    assert '412503' == next_board
