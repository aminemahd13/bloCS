import random
import os
import sys

SIZE = 4
WINNING_TILE = 2048

class Game2048:
    def __init__(self):
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def reset_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def add_new_tile(self):
        empty_tiles = [(i, j) for i in range(SIZE) for j in range(SIZE) if self.board[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.board[i][j] = 4 if random.random() > 0.9 else 2

    def compress(self, row):
        """Compresses non-zero tiles to the left"""
        new_row = [i for i in row if i != 0]
        new_row += [0] * (SIZE - len(new_row))
        return new_row

    def merge(self, row):
        """Merges tiles if they are the same, doubling the tile's value"""
        for i in range(SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        moved = False
        new_board = []
        for row in self.board:
            compressed_row = self.compress(row)
            merged_row = self.merge(compressed_row)
            new_row = self.compress(merged_row)
            new_board.append(new_row)
            if new_row != row:
                moved = True
        self.board = new_board
        return moved

    def rotate_board(self):
        """Rotates the board counterclockwise"""
        self.board = [list(row) for row in zip(*self.board[::-1])]

    def move_right(self):
        self.rotate_board()
        self.rotate_board()
        moved = self.move_left()
        self.rotate_board()
        self.rotate_board()
        return moved

    def move_up(self):
        self.rotate_board()
        moved = self.move_left()
        self.rotate_board()
        self.rotate_board()
        self.rotate_board()
        return moved

    def move_down(self):
        self.rotate_board()
        self.rotate_board()
        self.rotate_board()
        moved = self.move_left()
        self.rotate_board()
        return moved

    def can_move(self):
        """Checks if any move is possible"""
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == 0:
                    return True
                if j < SIZE - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return True
                if i < SIZE - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return True
        return False

    def check_win(self):
        for row in self.board:
            if WINNING_TILE in row:
                return True
        return False

    def print_board(self):
        self.reset_screen()
        print(f"Score: {self.score}\n")
        for row in self.board:
            print(" | ".join(f"{num or '.'}".center(5) for num in row))
            print("-" * (SIZE * 7))

    def play(self):
        self.print_board()
        while True:
            move = input("Use W/A/S/D to move (Q to quit): ").lower()
            if move == 'q':
                print("Thanks for playing!")
                break
            elif move in ['w', 'a', 's', 'd']:
                if move == 'a' and self.move_left() or \
                   move == 'd' and self.move_right() or \
                   move == 's' and self.move_up() or \
                   move == 'w' and self.move_down():
                    self.add_new_tile()
                    self.print_board()

                    if self.check_win():
                        print("Congratulations! You've reached 2048!")
                        break
                    if not self.can_move():
                        print("Game over! No moves left.")
                        break
                else:
                    print("Move not possible. Try a different direction.")
            else:
                print("Invalid input. Use W/A/S/D to move.")

if __name__ == "__main__":
    game = Game2048()
    game.play()
