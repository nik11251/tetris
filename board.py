import pygame

WHITE = (225, 225, 255)
GRAY = (128, 128, 128)


class Board:

    def __init__(self, x, y, width, height, block_size):

        self.x = x
        self.y = y
        self.W = width
        self.H = height
        self.block_size = block_size

        self.colors = []

        for i in range(self.W):
            a = []
            for j in range(self.H):
                a.append(WHITE)
            self.colors.append(a)

    def draw_rect(self, x, y, screen, color, bold):
        rect = pygame.Rect(self.x + x * self.block_size, self.y + y * self.block_size,
                           self.block_size, self.block_size)
        pygame.draw.rect(screen, color, rect, bold)

    def find_row(self):
        for i in range(self.H):
            row = True
            for j in range(self.W):
                if self.colors[j][i] == WHITE:
                    row = False
            if row:
                return i
        return -1

    def delete_row(self, ind):
        for i in range(self.W):
            j = ind
            while j > 0:
                self.colors[i][j] = self.colors[i][j-1]
                j -= 1
        for i in range(self.W):
            self.colors[i][0] = WHITE

    def full(self):
        i = 0
        for j in range(self.W):
            if self.colors[j][i] != WHITE:
                return True
        return False

    def update(self):
        res = 0
        ind = self.find_row()
        while ind != -1:
            self.delete_row(ind)
            ind = self.find_row()
            res += 1
        return res

    def draw(self, screen):

        for y in range(self.H):
            x = -1
            self.draw_rect(x, y, screen, GRAY, 0)
            x = self.W
            self.draw_rect(x, y, screen, GRAY, 0)

        for x in range(self.W):
            y = -1
            self.draw_rect(x, y, screen, GRAY, 0)
            y = self.H
            self.draw_rect(x, y, screen, GRAY, 0)

        for x in range(self.W):
            for y in range(self.H):
                if self.colors[x][y] == WHITE:
                    self.draw_rect(x, y, screen, WHITE, 1)
                else:
                    self.draw_rect(x, y, screen, self.colors[x][y], 0)
