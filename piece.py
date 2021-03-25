import pygame
from shapes import *
import random
import time

WHITE = (225, 225, 255)


class Piece:

    def __init__(self, block_size, clock, board):

        ind = random.randint(0, 6)
        self.color = colors[ind]
        self.shape = shapes[ind]
        self.state = 0

        self.block_size = block_size

        self.x = board.x + (board.W / 2 - 3) * block_size
        self.y = board.y

        self.clock = clock
        self.fall_time = 0
        self.fall_speed = 0.1  # 0.27

        self.can_hold = True

        self.velx = block_size
        self.vely = block_size

        self.keys = [False, False, False, False, False, False]

    def translate(self, x, y, board):
        x = (self.x - board.x) / self.block_size + (x - self.x) / self.block_size
        y = (self.y - board.y) / self.block_size + (y - self.y) / self.block_size
        x = int(x)
        y = int(y)
        return x, y

    def add(self, x, y, board):
        x, y = self.translate(x, y, board)
        board.colors[x][y] = self.color

    def kill(self, board, next_piece):
        self.check_piece(self.add, board)

        self.color = next_piece.color
        self.shape = next_piece.shape
        self.state = next_piece.state

        self.x = board.x + (board.W / 2 - 3) * self.block_size
        self.y = board.y - 1 * self.block_size

        self.keys = [False, False, False, False, False, False]
        time.sleep(0)

    def board_collision(self, x, y, board):
        x, y = self.translate(x, y, board)
        if y > board.H-1:
            return True
        if board.colors[x][y] != WHITE:
            return True
        return False

    def bottom_collision(self, board):
        return not self.check_piece(self.board_collision, board)

    def drop(self, board):
        self.fall_time += self.clock.get_rawtime()
        if self.fall_time/1000 > self.fall_speed:
            self.fall_time = 0
            self.y += self.vely
            if self.bottom_collision(board):
                self.y -= self.vely
                return True
        return False

    def draw_rect(self, x, y, screen):
        rect = pygame.Rect(x, y, self.block_size, self.block_size)
        pygame.draw.rect(screen, self.color, rect, 0)
        return False  # is there any mistakes while functioning?

    def border_collision(self, x, y, board):
        if x <= board.x - board.block_size or x >= board.x + board.W * board.block_size:
            return True
        return False

    def check_piece(self, func, arg):
        shape = self.shape[self.state]
        y = 0
        while y < len(shape):
            x = 0
            while x < len(shape[y]):
                if shape[y][x] == "0":
                    res = func(self.x + x * self.block_size, self.y + y * self.block_size, arg)
                    if res:
                        return False  # something is wrong
                x += 1
            y += 1
        return True

    def valid_space(self, board):
        return self.check_piece(self.border_collision, board) and not self.bottom_collision(board)

    def next_state(self):
        self.state += 1
        if self.state == len(self.shape):
            self.state = 0

    def prev_state(self):
        self.state -= 1
        if self.state == -1:
            self.state = len(self.shape) - 1

    def move_right(self):
        self.x += self.velx

    def move_left(self):
        self.x -= self.velx

    def update(self, board):

        if self.keys[0]:
            self.move_right()
            if not self.valid_space(board):
                self.move_left()
            self.keys[0] = False
        elif self.keys[1]:
            self.move_left()
            if not self.valid_space(board):
                self.move_right()
            self.keys[1] = False

        if self.keys[2]:
            self.next_state()
            if not self.valid_space(board):
                self.prev_state()
            self.keys[2] = False
        elif self.keys[3]:
            self.prev_state()
            if not self.valid_space(board):
                self.next_state()
            self.keys[3] = False

        if self.keys[4]:
            prev_speed = self.fall_speed
            self.fall_speed = 0.01
            res = self.drop(board)
            self.fall_speed = prev_speed
            return res
        else:
            return self.drop(board)

    def update_key(self, ind, p):
        self.keys[ind] = p

    def draw(self, screen):
        self.check_piece(self.draw_rect, screen)
