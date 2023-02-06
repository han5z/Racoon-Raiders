"""A1: Raccoon Raiders game objects (all tasks)

CSC148, Winter 2022

This code is provided solely for the personal and private use of students
taking the CSC148 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of this
code, whether as given or with any changes, are expressly prohibited.

Authors: Diane Horton, Sadia Sharmin, Dina Sabie, Jonathan Calver, and
Sophia Huynh.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Diane Horton, Sadia Sharmin, Dina Sabie, Jonathan Calver,
and Sophia Huynh.

=== Module Description ===
This module contains all of the classes necessary for a1_game.py to run.
"""

from __future__ import annotations

from random import shuffle
from typing import List, Tuple, Optional

# Each raccoon moves every this many turns
RACCOON_TURN_FREQUENCY = 20

# Directions dx, dy
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [LEFT, UP, RIGHT, DOWN]


def get_shuffled_directions() -> List[Tuple[int, int]]:
    """
    Provided helper that returns a shuffled copy of DIRECTIONS.
    You should use this where appropriate
    """
    to_return = DIRECTIONS[:]
    shuffle(to_return)
    return to_return


class GameBoard:
    """A game board on which the game is played.

    === Public Attributes ===
    ended:
        whether this game has ended or not
    turns:
        how many turns have passed in the game
    width:
        the number of squares wide this board is
    height:
        the number of squares high this board is

    === Representation Invariants ===
    turns >= 0
    width > 0
    height > 0
    No tile in the game contains more than 1 character, except that a tile
    may contain both a Raccoon and an open GarbageCan.

    === Sample Usage ===
    See examples in individual method docstrings.
    """
    # === Private Attributes ===
    # _player:
    #   the player of the game
    # _board:
    #   the rows on the board in the game
    # _raccoons:
    #   list containing every raccoon in the game
    # _recycling:
    #   list containing every recycling bin in the game

    ended: bool
    turns: int
    width: int
    height: int
    _player: Optional[Player]
    _board: List[List[List[Character]]]
    _raccoons: List[Raccoon]
    _recycling: List[RecyclingBin]

    def __init__(self, w: int, h: int) -> None:
        """Initialize this Board to be of the given width <w> and height <h> in
        squares. A board is initially empty (no characters) and no turns have
        been taken.

        >>> b = GameBoard(3, 3)
        >>> b.width == 3
        True
        >>> b.height == 3
        True
        >>> b.turns == 0
        True
        >>> b.ended
        False
        """

        self.ended = False
        self.turns = 0

        self.width = w
        self.height = h

        self._player = None

        self._board = []
        i = 0
        while i < self.height:
            row = []
            j = 0
            while j < self.width:
                row.append([])
                j += 1
            self._board.append(row)
            i += 1

        self._raccoons = []
        self._recycling = []

    def move(self, x: int, y: int, nx: int, ny: int) -> None:
        """Move a character from their current spot in x and y to a
        new location at nx and ny

        >>> b = GameBoard(3, 2)
        >>> p = Player(b, 1, 1)
        >>> b.move(1, 1, 1, 0)
        >>> b.at(1, 0) == [p]
        True
        >>> b.at(1, 1) == []
        True
        """
        change = self._board[y][x].pop()
        self._board[ny][nx].append(change)

    def place_character(self, c: Character) -> None:
        """Record that character <c> is on this board.

        This method should only be called from Character.__init__.

        The decisions you made about new private attributes for class GameBoard
        will determine what you do here.

        Preconditions:
        - c.board == self
        - Character <c> has not already been placed on this board.
        - The tile (c.x, c.y) does not already contain a character, with the
        exception being that a Raccoon can be placed on the same tile where
        an unlocked GarbageCan is already present.

        Note: The testing will depend on this method to set up the board,
        as the Character.__init__ method calls this method.

        >>> b = GameBoard(3, 2)
        >>> r = Raccoon(b, 1, 1)  # when a Raccoon is created, it is placed on b
        >>> b.at(1, 1)[0] == r  # requires GameBoard.at be implemented to work
        True
        """
        if isinstance(c, Player):
            self._player = c
        elif isinstance(c, Raccoon):
            self._raccoons.append(c)
        elif isinstance(c, RecyclingBin):
            self._recycling.append(c)
        self._board[c.y][c.x].append(c)

    def at(self, x: int, y: int) -> List[Character]:
        """Return the characters at tile (x, y).

        If there are no characters or if the (x, y) coordinates are not
        on the board, return an empty list.
        There may be as many as two characters at one tile,
        since a raccoon can climb into a garbage can.

        Note: The testing will depend on this method to allow us to
        access the Characters on your board, since we don't know how
        you have chosen to store them in your private attributes,
        so make sure it is working properly!

        >>> b = GameBoard(3, 2)
        >>> r = Raccoon(b, 1, 1)
        >>> b.at(1, 1)[0] == r
        True
        >>> p = Player(b, 0, 1)
        >>> b.at(0, 1)[0] == p
        True
        """
        return self._board[y][x]

    def to_grid(self) -> List[List[chr]]:
        """
        Return the game state as a list of lists of chrs (letters) where:

        'R' = Raccoon
        'S' = SmartRaccoon
        'P' = Player
        'C' = closed GarbageCan
        'O' = open GarbageCan
        'B' = RecyclingBin
        '@' = Raccoon in GarbageCan
        '-' = Empty tile

        Each inner list represents one row of the game board.

        >>> b = GameBoard(3, 2)
        >>> _ = Player(b, 0, 0)
        >>> _ = Raccoon(b, 1, 1)
        >>> _ = GarbageCan(b, 2, 1, True)
        >>> b.to_grid()
        [['P', '-', '-'], ['-', 'R', 'C']]
        """
        output = []
        y = 0
        for row in self._board:
            temp = []
            for x in range(len(row)):
                if not self._board[y][x]:
                    temp.append('-')
                elif len(self._board[y][x]) == 2:
                    temp.append('@')
                else:
                    temp.append(self._board[y][x][0].get_char())
            y += 1
            output.append(temp)
        return output

    def __str__(self) -> str:
        """
        Return a string representation of this board.

        The format is the same as expected by the setup_from_grid method.

        >>> b = GameBoard(3, 2)
        >>> _ = Raccoon(b, 1, 1)
        >>> print(b)
        ---
        -R-
        >>> _ = Player(b, 0, 0)
        >>> _ = GarbageCan(b, 2, 1, False)
        >>> print(b)
        P--
        -RO
        >>> str(b)
        'P--\\n-RO'
        """
        output = ''
        temp = self.to_grid()
        for y in temp:
            for x in y:
                output += x
            output += '\n'
        return output.rstrip('\n')

    def setup_from_grid(self, grid: str) -> None:
        """
        Set the state of this GameBoard to correspond to the string <grid>,
        which represents a game board using the following chars:

        'R' = Raccoon not in a GarbageCan
        'P' = Player
        'C' = closed GarbageCan
        'O' = open GarbageCan
        'B' = RecyclingBin
        '@' = Raccoon in GarbageCan
        '-' = Empty tile

        There is a newline character between each board row.

        >>> b = GameBoard(4, 4)
        >>> b.setup_from_grid('P-B-\\n-BRB\\n--BB\\n-C--')
        >>> str(b)
        'P-B-\\n-BRB\\n--BB\\n-C--'
        """
        lines = grid.split("\n")
        width = len(lines[0])
        height = len(lines)
        self.__init__(width, height)  # reset the board to an empty board
        y = 0
        for line in lines:
            x = 0
            for char in line:
                if char == 'R':
                    Raccoon(self, x, y)
                elif char == 'S':
                    SmartRaccoon(self, x, y)
                elif char == 'P':
                    Player(self, x, y)
                elif char == 'O':
                    GarbageCan(self, x, y, False)
                elif char == 'C':
                    GarbageCan(self, x, y, True)
                elif char == 'B':
                    RecyclingBin(self, x, y)
                elif char == '@':
                    GarbageCan(self, x, y, False)
                    Raccoon(self, x, y)  # always makes it a Raccoon
                    # Note: the order mattered above, as we have to place the
                    # Raccoon BEFORE the GarbageCan (see the place_character
                    # method precondition)
                x += 1
            y += 1

    # a helper method you may find useful in places
    def on_board(self, x: int, y: int) -> bool:
        """Return True iff the position x, y is within the boundaries of this
        board (based on its width and height), and False otherwise.
        """
        return 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1

    def give_turns(self) -> None:
        """Give every turn-taking character one turn in the game.

        The Player should take their turn first and the number of turns
        should be incremented by one. Then each other TurnTaker
        should be given a turn if RACCOON_TURN_FREQUENCY turns have occurred
        since the last time the TurnTakers were given their turn.

        After all turns are taken, check_game_end should be called to
        determine if the game is over.

        Precondition:
        self._player is not None

        >>> b = GameBoard(4, 3)
        >>> p = Player(b, 0, 0)
        >>> r = Raccoon(b, 1, 1)
        >>> b.turns
        0
        >>> for _ in range(RACCOON_TURN_FREQUENCY - 1):
        ...     b.give_turns()
        >>> b.turns == RACCOON_TURN_FREQUENCY - 1
        True
        >>> (r.x, r.y) == (1, 1)  # Raccoon hasn't had a turn yet
        True
        >>> (p.x, p.y) == (0, 0)  # Player hasn't had any inputs
        True
        >>> p.record_event(RIGHT)
        >>> b.give_turns()
        >>> (r.x, r.y) != (1, 1)  # Raccoon has had a turn!
        True
        >>> (p.x, p.y) == (1, 0)  # Player moved right!
        True
        """
        self._player.take_turn()
        self.turns += 1  # PROVIDED, DO NOT CHANGE

        if self.turns % RACCOON_TURN_FREQUENCY == 0:  # PROVIDED, DO NOT CHANGE
            for raccoon in self._raccoons:
                raccoon.take_turn()

        self.check_game_end()  # PROVIDED, DO NOT CHANGE

    def handle_event(self, event: Tuple[int, int]) -> None:
        """Handle a user-input event.

        The board's Player records the event that happened, so that when the
        Player gets a turn, it can make the move that the user input indicated.
        """
        self._player.record_event(event)

    def check_game_end(self) -> Optional[int]:
        """Check if this game has ended. A game ends when all the raccoons on
        this game board are either inside a can or trapped.

        If the game has ended:
        - update the ended attribute to be True
        - Return the score, where the score is given by:
            (number of raccoons trapped) * 10 + the adjacent_bin_score
        If the game has not ended:
        - update the ended attribute to be False
        - return None

        >>> b = GameBoard(3, 2)
        >>> _ = Raccoon(b, 1, 0)
        >>> _ = Player(b, 0, 0)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> b.check_game_end() is None
        True
        >>> b.ended
        False
        >>> _ = RecyclingBin(b, 2, 0)
        >>> b.check_game_end()
        11
        >>> b.ended
        True
        >>> b2 = GameBoard(4, 4)
        >>> r = Raccoon(b2, 0, 0)
        >>> p = Player(b2, 1, 0)
        >>> b = RecyclingBin(b2, 0, 1)
        >>> s = SmartRaccoon(b2, 2, 3)
        >>> o = GarbageCan(b2, 3, 3, False)
        >>> s.take_turn()
        >>> b2.check_game_end()
        11
        >>> b2.ended
        True
        """
        c = 0
        trapped = 0
        # Game will not end if there are no raccoons
        if not self._raccoons:
            return None

        for raccoon in self._raccoons:
            if raccoon.check_trapped():
                c += 1
                trapped += 1
            elif raccoon.inside_can:
                c += 1

        if c == len(self._raccoons):
            self.ended = True
            return 10 * trapped + self.adjacent_bin_score()
        else:
            self.ended = False
            return None

    def adjacent_bin_score(self) -> int:
        """
        Return the size of the largest cluster of adjacent recycling bins
        on this board.

        Two recycling bins are adjacent when they are directly beside each other
        in one of the four directions (up, down, left, right).

        See Task #5 in the handout for ideas if you aren't sure how
        to approach this problem.

        >>> b = GameBoard(3, 3)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 0, 0)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> print(b)
        B--
        -B-
        --B
        >>> b.adjacent_bin_score()
        1
        >>> _ = RecyclingBin(b, 2, 1)
        >>> print(b)
        B--
        -BB
        --B
        >>> b.adjacent_bin_score()
        3
        >>> _ = RecyclingBin(b, 0, 1)
        >>> print(b)
        B--
        BBB
        --B
        >>> b.adjacent_bin_score()
        5
        """
        # Return 0 if there are no recycling bins
        if not self._recycling:
            return 0

        lengths = []
        all_bins = self._recycling[:]
        while all_bins != []:
            bin1 = all_bins[0]
            cluster = [bin1]
            self.get_cluster(bin1.x, bin1.y, cluster)
            lengths.append(len(cluster))
            for c in cluster:
                all_bins.remove(c)
        return max(lengths)

    def find_neighbour_bins(self, x: int, y: int) -> List[Character]:
        """Find every neighbour of the inputted <x> and <y> coordinate that
        is a recycling bin
        >>> b = GameBoard(3, 3)
        >>> r = RecyclingBin(b, 1, 1)
        >>> r1 = RecyclingBin(b, 1, 0)
        >>> r2 = RecyclingBin(b, 0, 1)
        >>> r3 = RecyclingBin(b, 2, 1)
        >>> r4 = RecyclingBin(b, 1, 2)
        >>> len(b.find_neighbour_bins(1, 1)) == 4
        True
        >>> b.find_neighbour_bins(1, 1) \
        == [r2, r1, r3, r4]
        True
        >>> len(b.find_neighbour_bins(0, 0)) == 2
        True
        """
        neighbours = []
        for d in DIRECTIONS:
            new_x = x + d[0]
            new_y = y + d[1]
            if self.on_board(new_x, new_y):
                if (len(self.at(new_x, new_y)) == 1) and \
                        (isinstance(self.at(new_x, new_y)[0], RecyclingBin)):
                    neighbours.append(self.at(new_x, new_y)[0])
        return neighbours

    def get_cluster(self, x: int, y: int, checked: List[Character]) -> None:
        """Return a list of every recycling bin in the cluster starting from
        the initial inputted recycling bin at checked at the location x, y
        >>> b = GameBoard(4, 3)
        >>> r = RecyclingBin(b, 1, 1)
        >>> r1 = RecyclingBin(b, 0, 1)
        >>> r2 = RecyclingBin(b, 1, 0)
        >>> r3 = RecyclingBin(b, 2, 1)
        >>> r4 = RecyclingBin(b, 1, 2)
        >>> c = [r]
        >>> b.get_cluster(1, 1, c)
        >>> len(c) == 5
        True
        >>> b2 = GameBoard(6, 6)
        >>> r5 = RecyclingBin(b2, 2, 0)
        >>> r6 = RecyclingBin(b2, 1, 1)
        >>> r7 = RecyclingBin(b2, 2, 1)
        >>> r8 = RecyclingBin(b2, 3, 1)
        >>> r9 = RecyclingBin(b2, 1, 2)
        >>> r10 = RecyclingBin(b2, 2, 2)
        >>> r11 = RecyclingBin(b2, 3, 2)
        >>> r12 = RecyclingBin(b2, 4, 2)
        >>> r13 = RecyclingBin(b2, 3, 3)
        >>> r14 = RecyclingBin(b2, 4, 3)
        >>> r15 = RecyclingBin(b2, 3, 4)
        >>> r16 = RecyclingBin(b2, 5, 3)
        >>> c = [r7]
        >>> b2.get_cluster(2, 1, c)
        >>> len(c) == 12
        True
        """
        neighbours = self.find_neighbour_bins(x, y)
        not_checked = []
        for n in neighbours:
            if n not in checked:
                checked.append(n)
                not_checked.append(n)

        for n in not_checked:
            self.get_cluster(n.x, n.y, checked)

    def find_can(self, x: int, y: int, direction: Tuple[int, int]) -> int:
        """Finds every open bin along the directions surrounding
        SmartRaccoon S
        >>> b = GameBoard(5, 5)
        >>> s = SmartRaccoon(b, 2, 2)
        >>> _ = GarbageCan(b, 0, 2, False)
        >>> r = RecyclingBin(b, 1, 2)
        >>> _ = GarbageCan(b, 2, 0, True)
        >>> _ = GarbageCan(b, 3, 2, True)
        >>> b.find_can(s.x, s.y, DIRECTIONS[0])
        -1
        >>> b.find_can(s.x, s.y, DIRECTIONS[1])
        2
        >>> b.find_can(s.x, s.y, DIRECTIONS[2])
        1
        >>> b.find_can(s.x, s.y, DIRECTIONS[3])
        -1
        """
        rows = self.to_grid()
        counter = 1
        x += direction[0]
        y += direction[1]
        while self.on_board(x, y):
            if rows[y][x] == 'B' or rows[y][x] == 'R' or rows[y][x] == 'S' \
                    or rows[y][x] == '@':
                return -1
            if rows[y][x] == 'C' or rows[y][x] == 'O':
                return counter
            x += direction[0]
            y += direction[1]
            counter += 1
        return -1


class Character:
    """A character that has (x,y) coordinates and is associated with a given
    board.

    This class is abstract and should not be directly instantiated.

    NOTE: To reduce the amount of documentation in subclasses, we have chosen
    not to repeat information about the public attributes in each subclass.
    Remember that the attributes are not inherited, but only exist once we call
    the __init__ of the parent class.

    === Public Attributes ===
    board:
        the game board that this Character is on
    x, y:
        the coordinates of this Character on the board

    === Representation Invariants ===
    x, y are valid coordinates in board (i.e. board.on_board(x, y) is True)
    """
    board: GameBoard
    x: int
    y: int

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Character with board <b>, and
        at tile (<x>, <y>).

        When a Character is initialized, it is placed on board <b>
        by calling the board's place_character method. Refer to the
        preconditions of place_character, which must be satisfied.
        """
        self.board = b
        self.x, self.y = x, y
        self.board.place_character(self)  # this associates self with the board!

    def move(self, direction: Tuple[int, int]) -> bool:
        """
        Move this character to the tile

        (self.x + direction[0], self.y + direction[1]) if possible. Each child
        class defines its own version of what is possible.

        Return True if the move was successful and False otherwise.

        """
        raise NotImplementedError

    def get_char(self) -> chr:
        """
        Return a single character (letter) representing this Character.
        """
        raise NotImplementedError


# Note: You can safely ignore PyCharm's warning about this class
# not implementing abstract method(s) from its parent class.
class TurnTaker(Character):
    """
    A Character that can take a turn in the game.

    This class is abstract and should not be directly instantiated.
    """

    def take_turn(self) -> None:
        """
        Take a turn in the game. This method must be implemented in any subclass
        """
        raise NotImplementedError


class RecyclingBin(Character):
    """A recycling bin in the game.

    === Sample Usage ===
    >>> rb = RecyclingBin(GameBoard(4, 4), 2, 1)
    >>> rb.x, rb.y
    (2, 1)
    """

    def move(self, direction: Tuple[int, int]) -> bool:
        """Move this recycling bin to tile:
                (self.x + direction[0], self.y + direction[1])
        if possible and return whether or not this move was successful.

        If the new tile is occupied by another RecyclingBin, push
        that RecyclingBin one tile away in the same direction and take
        its tile (as described in the Assignment 1 handout).

        If the new tile is occupied by any other Character or if it
        is beyond the boundaries of the board, do nothing and return False.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> rb = RecyclingBin(b, 0, 0)
        >>> rb.move(UP)
        False
        >>> rb.move(DOWN)
        True
        >>> b.at(0, 1) == [rb]
        True
        """
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]
        if self.board.on_board(new_x, new_y):
            if not self.board.at(new_x, new_y):
                self.board.move(self.x, self.y, new_x, new_y)
                self.x = self.x + direction[0]
                self.y = self.y + direction[1]
                return True
            elif isinstance(self.board.at(new_x, new_y)[0], RecyclingBin):
                placeholder = self.board.at(new_x, new_y)[0].move(direction)
                if placeholder is True:
                    self.board.move(self.x, self.y, new_x, new_y)
                    self.x = self.x + direction[0]
                    self.y = self.y + direction[1]
                    return True
        return False

    def get_char(self) -> chr:
        """
        Return the character 'B' representing a RecyclingBin.
        """
        return 'B'


class Player(TurnTaker):
    """The Player of this game.

    === Sample Usage ===
    >>> b = GameBoard(3, 1)
    >>> p = Player(b, 0, 0)
    >>> p.record_event(RIGHT)
    >>> p.take_turn()
    >>> (p.x, p.y) == (1, 0)
    True
    >>> g = GarbageCan(b, 0, 0, False)
    >>> p.move(LEFT)
    True
    >>> g.locked
    True
    """
    # === Private Attributes ===
    # _last_event:
    #   The direction corresponding to the last keypress event that the user
    #   made, or None if there is currently no keypress event left to process
    _last_event: Optional[Tuple[int, int]]

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Player with board <b>,
        and at tile (<x>, <y>)."""

        TurnTaker.__init__(self, b, x, y)
        self._last_event = None

    def record_event(self, direction: Tuple[int, int]) -> None:
        """Record that <direction> is the last direction that the user
        has specified for this Player to move. Next time take_turn is called,
        this direction will be used.
        Precondition:
        direction is in DIRECTIONS
        """
        self._last_event = direction

    def take_turn(self) -> None:
        """Take a turn in the game.

        For a Player, this means responding to the last user input recorded
        by a call to record_event.
        """
        if self._last_event is not None:
            self.move(self._last_event)
            self._last_event = None

    def move(self, direction: Tuple[int, int]) -> bool:
        """Attempt to move this Player to the tile:
                (self.x + direction[0], self.y + direction[1])
        if possible and return True if the move is successful.

        If the new tile is occupied by a Racooon, a locked GarbageCan, or if it
        is beyond the boundaries of the board, do nothing and return False.

        If the new tile is occupied by a movable RecyclingBin, the player moves
        the RecyclingBin and moves to the new tile.

        If the new tile is unoccupied, the player moves to that tile.

        If a Player attempts to move towards an empty, unlocked GarbageCan, the
        GarbageCan becomes locked. The player's position remains unchanged in
        this case. Also return True in this case, as the Player has performed
        the action of locking the GarbageCan.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> p = Player(b, 0, 0)
        >>> p.move(UP)
        False
        >>> p.move(DOWN)
        True
        >>> b.at(0, 1) == [p]
        True
        >>> _ = RecyclingBin(b, 1, 1)
        >>> p.move(RIGHT)
        True
        >>> b.at(1, 1) == [p]
        True
        >>> p.move(RIGHT)
        True
        >>> b.at(2, 1) == [p]
        True
        """
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]
        temp = self.board.to_grid()
        placeholder = True
        if not self.board.on_board(new_x, new_y) or temp[new_y][new_x] == 'R' \
                or temp[new_y][new_x] == 'C' or temp[new_y][new_x] == 'S' \
                or temp[new_y][new_x] == '@':
            return False
        elif temp[new_y][new_x] == 'B':
            placeholder = self.board.at(new_x, new_y)[0].move(direction)
        elif temp[new_y][new_x] == 'O':
            # noinspection PyUnresolvedReferences
            self.board.at(new_x, new_y)[0].locked = True
            return True

        if placeholder is True:
            self.board.move(self.x, self.y, new_x, new_y)
            self.x += direction[0]
            self.y += direction[1]
            return True
        else:
            return False

    def get_char(self) -> chr:
        """
        Return the character 'P' representing this Player.
        """
        return 'P'


class Raccoon(TurnTaker):
    """A raccoon in the game.

    === Public Attributes ===
    inside_can:
        whether or not this Raccoon is inside a garbage can

    === Representation Invariants ===
    inside_can is True iff this Raccoon is on the same tile as an open
    GarbageCan.

    === Sample Usage ===
    >>> r = Raccoon(GameBoard(11, 11), 5, 10)
    >>> r.x, r.y
    (5, 10)
    >>> r.inside_can
    False
    """
    inside_can: bool

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Raccoon with board <b>, and
        at tile (<x>, <y>). Initially a Raccoon is not inside
        of a GarbageCan, unless it is placed directly inside an open GarbageCan.

        >>> r = Raccoon(GameBoard(11, 11), 5, 10)
        """
        self.inside_can = False
        # since this raccoon may be placed inside an open garbage can,
        # we need to initially set the inside_can attribute
        # BEFORE calling the parent init, which is where the raccoon is actually
        # placed on the board.
        TurnTaker.__init__(self, b, x, y)

    def check_trapped(self) -> bool:
        """Return True iff this raccoon is trapped. A trapped raccoon is
        surrounded on 4 sides (diagonals don't matter) by recycling bins, other
        raccoons (including ones in garbage cans), the player, and/or board
        edges. Essentially, a raccoon is trapped when it has nowhere it could
        move.

        Reminder: A racooon cannot move diagonally.

        >>> b = GameBoard(3, 3)
        >>> r = Raccoon(b, 2, 1)
        >>> _ = Raccoon(b, 2, 2)
        >>> _ = Player(b, 2, 0)
        >>> r.check_trapped()
        False
        >>> _ = RecyclingBin(b, 1, 1)
        >>> r.check_trapped()
        True
        """
        # Check if raccoon is already in garbage can
        if self.inside_can is True:
            return False

        for direction in DIRECTIONS:
            new_x = self.x + direction[0]
            new_y = self.y + direction[1]
            temp = self.board.to_grid()
            if self.board.on_board(new_x, new_y):
                if temp[new_y][new_x] == '-' or temp[new_y][new_x] == 'O' or \
                        temp[new_y][new_x] == 'C':
                    return False
        return True

    def move(self, direction: Tuple[int, int]) -> bool:
        """Attempt to move this Raccoon in <direction> and return whether
        or not this was successful.

        If the tile one tile over in that direction is occupied by the Player,
        a RecyclingBin, or another Raccoon, OR if the tile is not within the
        boundaries of the board, do nothing and return False.

        If the tile is occupied by an unlocked GarbageCan that has no Raccoon
        in it, this Raccoon moves there and we have two characters on one tile
        (the GarbageCan and the Raccoon). If the GarbageCan is locked, this
        Raccoon uses this turn to unlock it and return True.

        If a Raccoon is inside of a GarbageCan, it will not move. Do nothing and
        return False.

        Return True if the Raccoon unlocks a GarbageCan or moves from its
        current tile.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> r = Raccoon(b, 0, 0)
        >>> r.move(UP)
        False
        >>> r.move(DOWN)
        True
        >>> b.at(0, 1) == [r]
        True
        >>> g = GarbageCan(b, 1, 1, True)
        >>> r.move(RIGHT)
        True
        >>> r.x, r.y  # Raccoon didn't change its position
        (0, 1)
        >>> not g.locked  # Raccoon unlocked the garbage can!
        True
        >>> r.move(RIGHT)
        True
        >>> r.inside_can
        True
        >>> len(b.at(1, 1)) == 2  # Raccoon and GarbageCan are both at (1, 1)!
        True
        """
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]
        temp = self.board.to_grid()
        if not self.board.on_board(new_x, new_y) or temp[new_y][new_x] == 'P' \
                or temp[new_y][new_x] == 'B':
            return False
        elif temp[new_y][new_x] == 'R' or \
                temp[new_y][new_x] == 'S' or temp[new_y][new_x] == '@':
            return False
        elif temp[self.y][self.x] == '@':
            return False
        elif temp[new_y][new_x] == 'C':
            # noinspection PyUnresolvedReferences
            self.board.at(new_x, new_y)[0].locked = False
            return True
        elif temp[new_y][new_x] == 'O':
            self.inside_can = True

        self.board.move(self.x, self.y, new_x, new_y)
        self.x += direction[0]
        self.y += direction[1]
        return True

    def take_turn(self) -> None:
        """Take a turn in the game.

        If a Raccoon is in a GarbageCan, it stays where it is.

        Otherwise, it randomly attempts (if it is not blocked) to move in
        one of the four directions, with equal probability.

        >>> b = GameBoard(3, 4)
        >>> r1 = Raccoon(b, 0, 0)
        >>> r1.take_turn()
        >>> (r1.x, r1.y) in [(0, 1), (1, 0)]
        True
        >>> r2 = Raccoon(b, 2, 1)
        >>> _ = RecyclingBin(b, 2, 0)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> r2.take_turn()  # Raccoon is trapped
        >>> r2.x, r2.y
        (2, 1)
        """
        if len(self.board.at(self.x, self.y)) == 2:
            return None
        temp = False
        counter = 0
        random_dir = DIRECTIONS[:]
        shuffle(random_dir)

        while temp is False and counter < len(random_dir):
            temp = self.move(random_dir[counter])
            counter += 1

    def get_char(self) -> chr:
        """
        Return '@' to represent that this Raccoon is inside a garbage can
        or 'R' otherwise.
        """
        if self.inside_can:
            return '@'
        return 'R'


class SmartRaccoon(Raccoon):
    """A smart raccoon in the game.

    Behaves like a Raccoon, but when it takes a turn, it will move towards
    a GarbageCan if it can see that GarbageCan in its line of sight.
    See the take_turn method for details.

    SmartRaccoons move in the same way as Raccoons.

    === Sample Usage ===
    >>> b = GameBoard(8, 2)
    >>> s = SmartRaccoon(b, 4, 0)
    >>> s.x, s.y
    (4, 0)
    >>> s.inside_can
    False
    """

    def take_turn(self) -> None:
        """Take a turn in the game.

        If a SmartRaccoon is in a GarbageCan, it stays where it is.

        A SmartRaccoon checks along the four directions for
        the closest non-occupied GarbageCan that has nothing blocking
        it from reaching that GarbageCan (except possibly the Player).

        If there is a tie for the closest GarbageCan, a SmartRaccoon
        will prioritize the directions in the order indicated in DIRECTIONS.

        If there are no GarbageCans in its line of sight along one of the four
        directions, it moves exactly like a Raccoon. A GarbageCan is in its
        line of sight if there are no other Raccoons, RecyclingBins, or other
        GarbageCans between this SmartRaccoon and the GarbageCan. The Player
        may be between this SmartRaccoon and the GarbageCan though.

        >>> b = GameBoard(8, 2)
        >>> s = SmartRaccoon(b, 4, 0)
        >>> _ = GarbageCan(b, 3, 1, False)
        >>> _ = GarbageCan(b, 0, 0, False)
        >>> _ = GarbageCan(b, 7, 0, False)
        >>> s.take_turn()
        >>> s.x == 5
        True
        >>> s.take_turn()
        >>> s.x == 6
        True
        """
        cans = []
        if len(self.board.at(self.x, self.y)) == 2:
            return None
        for d in DIRECTIONS:
            cans.append(self.board.find_can(self.x, self.y, d))

        closest = max(cans)
        for option in cans:
            if 0 < option < closest:
                closest = option
        if closest == -1:
            super().take_turn()
        else:
            self.move(DIRECTIONS[cans.index(closest)])
        return None

    def get_char(self) -> chr:
        """
        Return '@' to represent that this SmartRaccoon is inside a Garbage Can
        and 'S' otherwise.
        """
        if self.inside_can:
            return '@'
        return 'S'


class GarbageCan(Character):
    """A garbage can in the game.

    === Public Attributes ===
    locked:
        whether or not this GarbageCan is locked.

    === Sample Usage ===
    >>> b = GameBoard(2, 2)
    >>> g = GarbageCan(b, 0, 0, False)
    >>> g.x, g.y
    (0, 0)
    >>> g.locked
    False
    """
    locked: bool

    def __init__(self, b: GameBoard, x: int, y: int, locked: bool) -> None:
        """Initialize this GarbageCan to be at tile (<x>, <y>) and store
        whether it is locked or not based on <locked>.
        """

        Character.__init__(self, b, x, y)
        self.locked = locked

    def get_char(self) -> chr:
        """
        Return 'C' to represent a closed garbage can and 'O' to represent
        an open garbage can.
        """
        if self.locked:
            return 'C'
        return 'O'

    def move(self, direction: Tuple[int, int]) -> bool:
        """
        Garbage cans cannot move, so always return False.
        """
        return False


# A helper function you may find useful for Task #5, depending on how
# you implement it.
def get_neighbours(tile: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Return the coordinates of the four tiles adjacent to <tile>.

    This does NOT check if they are valid coordinates of a board.

    >>> ns = set(get_neighbours((2, 3)))
    >>> {(2, 2), (2, 4), (1, 3), (3, 3)} == ns
    True
    """
    rslt = []
    for direction in DIRECTIONS:
        rslt.append((tile[0] + direction[0], tile[1] + direction[1]))
    return rslt


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': [],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', '__future__', 'math'],
        'disable': ['E1136'],
        'max-attributes': 15,
        'max-module-lines': 1600
    })
