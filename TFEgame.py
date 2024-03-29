import sys
import random
import numpy as np
from msvcrt import getwch


class TFEgame:
    
    def __init__(self, dims:tuple[int]=(4, 4)):
        assert dims[0] == dims[1], 'Dimensions must be square'
        self._dims = dims
        self._board = np.array([[0] * dims[0]] * dims[1])
        self._score = 0
        self._moves = 0
        self._albums = {0:None, 2:'TaylorSwift', 4:'Fearless', 8:'SpeakNow', \
                       16:'Red', 32:'1989', 64:'Reputation', 128:'Lover', \
                        256:'Folklore', 512:'Evermore', 1024:'Midnights', \
                        2048:'END'}
        self._max_tile = 2
        self._gen_starting_tiles()
        self.keys = {'w', 'a', 's', 'd'}
        self.directions = {'w':'up()', 'a':'left()', 's':'down()', 'd':'right()'}

    
    def __repr__(self) -> str:
        """ returns a string representing the current state of the board """
        return '\n'.join([' '.join([str(self._board[i][j]) for j in range(self._dims[1])]) for i in range(self._dims[0])])
    
    def board(self) -> np.array:
        """ returns a copy of the game's board"""
        return self._board.copy()
    
    def dims(self) -> tuple[int]:
        """ returns a tuple of ints representing the dimensions of the board """
        return self._dims
    
    def max_tile(self) -> int:
        """ returns the largest tile on the board """
        return self._max_tile
    
    def _gen_starting_tiles(self) -> None:
        self._board = np.zeros_like(self._board)
        for i in range(2):
            empty_spaces = np.argwhere(self._board == 0)
            r, c = empty_spaces[random.randint(0, len(empty_spaces)-1)]
            self._board[r][c] = 2 if random.random() < 0.9 else 4
        # the max tile will be 4 if it exists, otherwise it will be 2
        if 4 in self._board:
            self._max_tile = 4
        else:
            self._max_tile = 2
    
    def score(self) -> int:
        """ returns the game's score """
        return self._score
    
    def _get_key_input(self) -> str:
        keys = {'w', 'a', 's', 'd'}
        while True:
            key = getwch()
            if key in keys:
                return key
            if key == 'q':
                print('quiting game...')
                sys.exit()
            
    def _do_move(self, m) -> bool:
        """ calls the appropriate method to execute a given move input """                
        def collapse(row:np.array) -> np.array:
            """ inplace collapse of a row or column """
            # move all nonzero elements to the left 
            # ('left' is relative to the direction of the move and is accounted for by the caller)
            nonzeros = list(np.nonzero(row)[0])
            for i in range(len(row)):
                if not nonzeros:
                    break
                index = nonzeros.pop(0)
                row[i] = row[index]
                if i != index:
                    row[index] = 0

            # combine like terms and shift accordingly
            for i in range(len(row)):
                elem = row[i]
                if elem == 0:
                    continue
                if i != len(row)-1 and elem == row[i+1]:
                    elem *= 2
                    row[i+1] = 0
                    self._score += elem
                    self._max_tile = max(elem, self._max_tile)

                row[i] = 0
                first_zero = np.where(row == 0)[0][0]
                row[first_zero] = elem

            return row
    
        def left() -> bool:
            changed = False
            for i, row in enumerate(self._board):
                orig = row.copy()
                self._board[i] = collapse(row)
                if not np.array_equal(orig, self._board[i]):
                    changed = True
            return changed

        def right() -> bool:
            changed = False
            for i, row in enumerate(self._board):
                orig = row.copy()
                self._board[i] = np.flip(collapse(np.flip(row)))
                if not np.array_equal(orig, self._board[i]):
                    changed = True
            return changed
        
        def up() -> bool:
            changed = False
            for i in range(len(self._board)):
                orig = self._board[:,i].copy()
                self._board[:,i] = collapse(self._board[:,i])
                if not np.array_equal(orig, self._board[:,i]):
                    changed = True
            return changed
        
        def down() -> bool:
            changed = False
            for i in range(len(self._board)):
                orig = self._board[:,i].copy()
                self._board[:,i] = np.flip(collapse(np.flip(self._board[:,i])))
                if not np.array_equal(orig, self._board[:,i]):
                    changed = True
            return changed

        return eval(self.directions[m])

    def move(self, key=None) -> str:
        """ gets user input for the next move """
        if key is None:
            key = self._get_key_input()
        changed = self._do_move(key)
        if changed:
            self._add_random()
            self._moves += 1
        return key

    def _add_random(self) -> None:
        if self._is_full():
            return
        empty_spaces = np.argwhere(self._board == 0)
        r, c = empty_spaces[random.randint(0, len(empty_spaces)-1)]
        value = 2 if random.random() < 0.9 else 4
        self._board[r][c] = value

    def _is_full(self) -> bool:
        """ returns a boolean indicating whether the board is full """
        return self._board.all()
    
    def can_move(self) -> bool:
        """ returns a boolean indicating whether the player can move """
        if not self._is_full():
            return True
        def check_adjacent(arr) -> bool:
            """ returns boolean representing two same elements are next to each other """
            for i in range(1, len(arr)):
                if arr[i] == arr[i-1]:
                    return True
            return False
        for i in range(self._dims[0]):  # dims must be square so we can check rows and cols together
            row = self._board[i]
            col = self._board[:,i]
            if check_adjacent(row) or check_adjacent(col):
                return True
        return False
    
    def is_playable(self) -> bool:
        """ returns a boolean indicating whether the game is playable """
        return self.can_move() and not self.won()
    
    def won(self) -> bool:
        """ returns a boolean indicating whether the game has been won, 10/2048 has been reached """
        return np.amax(self._board) == 2048
    
    def lost(self) -> bool:
        """ returns a boolean indicating whether the game as been lost """
        return not self.can_move() and not self.won()
    
    def play(self) -> bool:
        """ the game loop """
        self._gen_starting_tiles()
        while self.is_playable():
            print(f'Score: {self._score} \t Moves: {self._moves}')
            print(self, '\n')
            self.move()
        if self.won():
            print(f'You won with a score of {self._score} in {self._moves} moves!')
            return True
        print(f'You lost with a score of {self._score} in {self._moves} moves.')
        return False

if __name__ == '__main__':
    game = TFEgame()
    game.play()