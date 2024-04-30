"""
6.101 Lab 7:
Six Double-Oh Mines
"""
#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    keys = ("board", "dimensions", "state", "visible")
    # ^ Uses only default game keys. If you modify this you will need
    # to update the docstrings in other functions!
    for key in keys:
        val = game[key]
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def in_bound(nrows, ncolumns, row, col):
    """
    Return True if (row, col) represents a location
    that is in bounds of the board, with dimensions (nrows, ncolumns).
    """
    return 0 <= row < nrows and 0 <= col < ncolumns


def make_2d_board(nrows, ncolumns, type_of_board, mines=[]):
    """
    Return a list of lists with dimensions (nrows, ncolumns) and
    initialize elements in the list according to the type of board
    inputed.
    """
    board = []
    if type_of_board == "mine_field":
        for r in range(nrows):
            row = []
            for c in range(ncolumns):
                val = 0
                if (r, c) in mines:
                    val = "."
                row.append(val)
            board.append(row)
    elif type_of_board == "visible_field":
        board = [[False] * ncolumns for _ in range(nrows)]
    return board


def num_valid_neighbor_tiles(nrows, ncolumns, row, col, tile_check):
    """
    Return a list of tuples in the form (row, col) representing the locations that
    satisfy the tile_check function, which returns true if a
    tile, that is (row, col), contains a desired value.
    """
    neighbor_tiles = []
    for delta_r in range(-1, 2):
        for delta_c in range(-1, 2):
            neighbor_tiles.append((row + delta_r, col + delta_c))
    # list of valid (row, col) tuples that are within the board
    # dimensions and satsify the tile_check function
    return len(
        [
            tile
            for tile in neighbor_tiles
            if in_bound(nrows, ncolumns, *tile) and tile_check(tile)
        ]
    )


def new_game_2d(nrows, ncolumns, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Parameters:
       nrows (int): Number of rows
       ncolumns (int): Number of columns
       mines (list): List of mines, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: ongoing
    visible:
        [False, False, False, False]
        [False, False, False, False]
    """
    # create two list of lists representing the mine field and visible field
    dimensions = nrows, ncolumns
    new_game = new_game_nd(dimensions, mines)

    return new_game


def get_2d_board_value(board, row, col):
    """
    Return the value contained at (row, col) using list of lists, board.
    """
    return board[row][col]


def set_2d_board_value(board, value, row, col):
    """
    Set element at (row, col) to value.
    """
    board[row][col] = value


def victory_check(game_board, visible_board, nrows, ncolumns):
    """
    Return True if all tiles in visible_board contain True, False otherwise.
    """
    for r in range(nrows):
        for c in range(ncolumns):
            if not visible_board[r][c] and game_board[r][c] != ".":
                return False
    return True


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['visible'] to reveal (row, col).  Then, if (row, col) has no
    adjacent mines (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one mine
    is visible on the board after digging (i.e. game['visible'][mine_location]
    == True), 'victory' when all safe squares (squares that do not contain a
    mine) and no mines are visible, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    state: victory
    visible:
        [False, True, True, True]
        [False, False, True, True]

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible': [[False, True, False, False],
    ...                  [False, False, False, False]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    state: defeat
    visible:
        [True, True, False, False]
        [False, False, False, False]
    """
    return dig_nd(game, coordinates=(row, col))


def render_2d_locations(game, all_visible=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  game['visible'] indicates which squares should be visible.  If
    all_visible is True (the default is False), game['visible'] is ignored
    and all cells are shown.

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                    by game['visible']

    Returns:
       A 2D array (list of lists)

    >>> game = {'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'visible':  [[False, True, True, False],
    ...                   [False, False, True, False]]}
    >>> render_2d_locations(game, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations(game, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, all_visible)


def render_2d_board(game, all_visible=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'visible':  [[True, True, True, False],
    ...                            [False, False, True, False]]})
    '.31_\\n__1_'
    """
    string_based_rep = ""
    twod_locations = render_2d_locations(game, all_visible)
    # loop through each tile in twod_locations and
    # concanate that value to string_based_rep
    for i in range(len(twod_locations)):
        for j in range(len(twod_locations[0])):
            string_based_rep += str(twod_locations[i][j])
        # no new line after last line
        if i < len(twod_locations) - 1:
            string_based_rep += "\n"
    return string_based_rep


# N-D IMPLEMENTATION
def equal_ndlocation(location1, location2):
    """
    Return True if all the coordinates of location1 is
    equal to location2's coordinates.
    """
    for coord1, coord2 in zip(location1, location2):
        if coord1 != coord2:
            return False
    return True


def in_mines(location1, mines):
    """
    Return True if mines contains location1.
    """
    for location in mines:
        if equal_ndlocation(location, location1):
            return True
    return False


def all_possible_locations(dimensions):
    """
    Return a set of all the possible coordinates in a board
    with dimensions given by "dimensions".
    """
    if not dimensions:
        return

    # retrieve the first coordinate
    first_dimension = dimensions[0]

    # combine all the possible values of first coordinate with other coordinates
    if len(dimensions) == 1:
        for i in range(first_dimension):
            yield (i,)
    else:
        for i in range(first_dimension):
            for location in all_possible_locations(dimensions[1:]):
                new_location = (i,) + location
                yield new_location


def get_nd_value(board, location):
    """
    Return the value at location in nd-board.
    """
    if not isinstance(board, list):
        return board
    first_coordinate = location[0]
    first_board = board[first_coordinate]
    return get_nd_value(first_board, location[1:])


def set_nd_value(board, location, value):
    """
    Set the nd-board at location to value.
    Returns the value.
    """
    if not isinstance(board[location[0]], list):
        board[location[0]] = value
        return value
    first_coordinate = location[0]
    first_board = board[first_coordinate]
    set_nd_value(first_board, location[1:], value)


def assign_values_to_board(dimensions, board, type_board, mines=[]):
    """
    Mutate the board so that locations in nd-board as specified
    by the list of locations in the mines (list).
    contain '.', a mine.
    """
    for location in all_possible_locations(dimensions):
        if type_board == "visible":
            set_nd_value(board, location, False)
        elif location in mines:
            set_nd_value(board, location, ".")


def make_nd_board(dimensions, mines=[]):
    """
    Return an nd game board with dimensions given by "dimensions".
    """
    if not dimensions:
        return 0

    first_dimension = dimensions[0]
    first_list = [0] * first_dimension

    for i in range(first_dimension):
        rest_list = make_nd_board(dimensions[1:], mines)
        first_list[i] = rest_list

    return first_list


def nd_in_bound(dimensions, location):
    """
    Return True if location is in bounds by checking if each
    coordinate in location is in between 0 and the corresponding
    dimension in dimensions.
    """
    for dim_coord, loc_coord in zip(dimensions, location):
        if loc_coord < 0 or loc_coord >= dim_coord:
            return False
    return True


def num_nd_neighbor_tiles(dimensions, location):
    """
    Return a list of tuples in the form (c1, c2,...) representing the locations that
    satisfy the tile_check function, which returns true if a
    tile contains a desired value.
    """

    def all_neighbors(location):
        if not location:
            return
        first_coord = location[0]
        # neighbor_tiles = []
        if len(location) == 1:
            for delta_coord in range(-1, 2):
                yield (location[0] + delta_coord,)
            # return [(location[0] + delta_coord,) for delta_coord in range(-1, 2)]

        for delta_coord in range(-1, 2):
            new_first_coord = first_coord + delta_coord
            for smaller_neighbor in all_neighbors(location[1:]):
                new_coord = (new_first_coord,) + smaller_neighbor
                yield new_coord

    # list of valid location tuples that are within the board
    # dimensions and satsify the tile_check function
    neighbors = all_neighbors(location)
    for neighbor in neighbors:
        if nd_in_bound(dimensions, neighbor):
            yield neighbor


def new_game_nd(dimensions, mines):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'visible' fields adequately initialized.

    Args:
       dimensions (tuple): Dimensions of the board
       mines (list): mine locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, False], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """

    # create two list of lists representing the mine field and visible field
    game_board = make_nd_board(dimensions)
    visible_board = make_nd_board(dimensions)

    # Initialize locations in both game board and visible board to contain the right items
    assign_values_to_board(dimensions, game_board, "mines", mines)
    assign_values_to_board(dimensions, visible_board, "visible")

    # go through each mine location and its neighboring tiles not containing a mine
    # and set the value at that those tiles to the number of neighboring mines
    mines_set = set(mines)
    for location in mines_set:
        for neighbor in num_nd_neighbor_tiles(dimensions, location):
            if neighbor not in mines_set:
                neighboring_mines = get_nd_value(game_board, neighbor)
                set_nd_value(game_board, neighbor, neighboring_mines + 1)

    return {
        "dimensions": dimensions,
        "board": game_board,
        "visible": visible_board,
        "state": "ongoing",
    }

def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the visible to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    mine.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one mine is visible on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a mine) and no mines are visible, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: ongoing
    visible:
        [[False, False], [False, True], [True, True], [True, True]]
        [[False, False], [False, False], [True, True], [True, True]]
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [False, False],
    ...                [False, False]],
    ...               [[False, False], [False, False], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    state: defeat
    visible:
        [[False, True], [False, True], [False, False], [False, False]]
        [[False, False], [False, False], [False, False], [False, False]]
    """

    def nd_victory_check(game_board, visible_board):
        """
        Return True if all the locations in board that don't contain a mine
        are marked as revealed (True) in visible_board.
        """
        for location in all_possible_locations(dimensions):
            visible = get_nd_value(visible_board, location)
            if not visible and get_nd_value(game_board, location) != ".":
                return False
        return True

    def reveal_neighbors(location):
        """
        Return the total number of tiles revealed as a result of
        revealing location.
        """
        if get_nd_value(game_board, location) == 0:
            # loop through each neighbor of location
            num_revealed = 1
            for neighbor in num_nd_neighbor_tiles(dimensions, location):
                # given location is in bounds and not already visible
                # set it to visible to True and increment num_revealed
                if not get_nd_value(visible_board, neighbor):
                    set_nd_value(visible_board, neighbor, True)
                    num_revealed += reveal_neighbors(neighbor)
            # the number of neighbors revealed for this (row, col)
            return num_revealed
        return 1

    game_board = game["board"]
    visible_board = game["visible"]
    dimensions = game["dimensions"]

    # zero tiles were revealed if game state is "defeat" or "victory" or tile already visible
    if game["state"] != "ongoing" or get_nd_value(visible_board, coordinates):
        return 0

    # keep track of tiles revealed
    set_nd_value(visible_board, coordinates, True)
    revealed = 1

    # number of neighbors revealed
    revealed = reveal_neighbors(coordinates)

    # if object at location is a mine only one tile revealed
    if get_nd_value(game_board, coordinates) == ".":
        game["state"] = "defeat"
    # if all locations not containing a mine are visible, game state victory
    elif not nd_victory_check(game_board, visible_board):
        game["state"] = "ongoing"
    else:
        game["state"] = "victory"
    return revealed


def render_nd(game, all_visible=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (mines), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    mines).  The game['visible'] array indicates which squares should be
    visible.  If all_visible is True (the default is False), the game['visible']
    array is ignored and all cells are shown.

    Args:
       all_visible (bool): Whether to reveal all tiles or just the ones allowed
                           by game['visible']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'visible': [[[False, False], [False, True], [True, True],
    ...                [True, True]],
    ...               [[False, False], [False, False], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """

    # list of lists representing current game state
    game_board = game["board"]
    # list of lists showing what location values seen to the player
    visible_board = game["visible"]
    dimensions = game["dimensions"]

    # copy and represent values in original game board
    # according to specifications
    board = make_nd_board(dimensions)
    for location in all_possible_locations(dimensions):
        # all locations or visible or this location is visible
        if get_nd_value(visible_board, location) or all_visible:
            if get_nd_value(game_board, location) == 0:
                set_nd_value(board, location, " ")
            else:
                game_board_val = get_nd_value(game_board, location)
                set_nd_value(board, location, str(game_board_val))
        # value at location is hidden
        else:
            set_nd_value(board, location, "_")
    return board


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    dimensions = (10, 20, 20)
    # board_game = make_nd_board(dimensions)
    # visible_board = make_nd_board(dimensions)
    # print("GAME: ", board_game)
    # print("VISIBLE: ", visible_board )

    # mines=[(0,0), (1,0), (1,1)]
    # assign_values_to_board(dimensions, visible_board, "visible")
    # assign_values_to_board(dimensions, board_game, "mines", mines)
    # dump(new_game_nd(dimensions, mines))
    # print(visible_board)
    # print(board_game)

    # print("Neighbors: ", num_nd_neighbor_tiles(dimensions, (3,10,7)))

    # dimensions = (2, 2, 2)
    # mines = [(0, 0, 0), (1, 1, 1)]
    # result = new_game_nd(dimensions, mines)
    # dump(result)
    # expected = {
    #     'dimensions': (3,3),
    #     'board': [[1, '.', 2], [0, 2, '.'], [0, 1, 1]],
    #     'visible': [
    #         [True, True, False],
    #         [True, True, False],
    #         [True, True, True]
    #     ],
    #     'state': 'ongoing',
    # }

    # visible = [[[False, True], [False, True], [False, False], [False, False]],
    #         [[False, False], [False, False], [False, False], [False, False]]
    #         ]

    # game = [
    #      [[3, '.'], [3, 3], [1, 1], [0, 0]],
    #     [['.', 3], [3, '.'], [1, 1], [0, 0]]
    # ]

    # print(nd_victory_check(game, visible))
    # game =  {
    #     'dimensions': (3,3),
    #     'board': [[1, '.', 2], [1, 2, '.'], [0, 1, 1]],
    #     'visible': [
    #         [False, False, False],
    #         [False, False, False],
    #         [False, False, False]
    #     ],
    #     'state': 'ongoing',
    #     }
    # coordinates = (2,0)
    # revealed = dig_nd(game, coordinates)
    # dump(game)
    # print("Revealed: ", revealed)
    # doctest.run_docstring_examples(
    #    render_2d_board,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=True
    # )
