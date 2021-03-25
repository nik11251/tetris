import pygame
from board import *
from piece import *


class Game:

    def __init__(self, width, height, fps):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Tetris')

        self.running = True
        self.FPS = pygame.time.Clock()
        self.frames = fps

        self.H = height
        self.W = width
        self.screen = pygame.display.set_mode((self.W, self.H))

        self.score = 0
        self.font = pygame.font.Font(pygame.font.get_default_font(), 30)

        self.block_size = 20

        self.background = Board(100, 0, 10, 24, self.block_size)
        self.next_board = Board(360, self.block_size * 3, 4, 4, self.block_size)
        self.hold_board = Board(360, 240, 4, 4, self.block_size)

        self.piece = Piece(self.block_size, self.FPS, self.background)
        self.next_piece = Piece(self.block_size, self.FPS, self.next_board)
        self.hold_piece = Piece(self.block_size, self.FPS, self.hold_board)

        self.instructions = ["E - hold", "A - left", "D - right"]

    def update_score(self, rows):
        if rows == 1:
            self.score += 40
        elif rows == 2:
            self.score += 100
        elif rows == 3:
            self.score += 300
        elif rows == 4:
            self.score += 1200

    def write_text(self, s, x, y):
        text = self.font.render("{}".format(s), False, (225, 225, 225))
        self.screen.blit(text, (x, y))

    def update(self):
        if self.piece.update(self.background):
            self.piece.kill(self.background, self.next_piece)
            self.hold_piece.can_hold = True
            self.next_piece = Piece(self.block_size, self.FPS, self.next_board)
        rows = self.background.update()
        self.update_score(rows)

    def draw(self):
        self.screen.fill((0, 0, 0))

        self.background.draw(self.screen)
        self.next_board.draw(self.screen)
        self.hold_board.draw(self.screen)

        self.piece.draw(self.screen)
        self.next_piece.draw(self.screen)
        self.hold_piece.draw(self.screen)

        self.write_text(self.score, 0, 0)
        self.write_text("next", 360, 0)
        self.write_text("hold", 360, 180)
        i = 0
        while i < 3:
            self.write_text("{}".format(self.instructions[i]), 360, 360 + i * self.block_size*2)
            i += 1

    def tick(self):
        self.FPS.tick(self.frames)

    def hold(self):
        if not self.hold_piece.can_hold:
            return
        self.piece.x = self.hold_piece.x
        self.piece.y = self.hold_piece.y
        self.piece.can_hold = False
        temp_piece = Piece(self.block_size, self.FPS, self.background)
        temp_piece.color = self.hold_piece.color
        temp_piece.shape = self.hold_piece.shape
        temp_piece.state = self.hold_piece.state
        self.hold_piece = self.piece
        self.piece = temp_piece

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.piece.update_key(1, True)
            elif event.key == pygame.K_d:
                self.piece.update_key(0, True)
            elif event.key == pygame.K_w:
                self.piece.update_key(2, True)
            elif event.key == pygame.K_s:
                self.piece.update_key(3, True)
            elif event.key == pygame.K_SPACE:
                self.piece.update_key(4, True)
            elif event.key == pygame.K_e:
                self.hold()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.piece.update_key(1, False)
            elif event.key == pygame.K_d:
                self.piece.update_key(0, False)
            elif event.key == pygame.K_w:
                self.piece.update_key(2, False)
            elif event.key == pygame.K_s:
                self.piece.update_key(3, False)
            elif event.key == pygame.K_SPACE:
                self.piece.update_key(4, False)

    def game_over(self):
        if self.background.full():
            return True
        return False

    def run(self):

        while self.running:
            if self.game_over():
                self.running = False
            for event in pygame.event.get():
                self.handle_event(event)
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()
            self.update()
            self.draw()
            self.tick()

        pygame.quit()
