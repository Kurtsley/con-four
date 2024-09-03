# Brian Beard 2024

import pyxel

PADDING_Y = 40

BOARD_WIDTH = 160
BOARD_HEIGHT = 152
BOARD_OFFSET = 6
TABLE_HEIGHT = BOARD_HEIGHT + PADDING_Y

TOKEN_WIDTH = 16
TOKEN_HEIGHT = 16
TOKEN_GRAVITY = 4

PLAYER1_START_X = 160
PLAYER2_START_X = PLAYER1_START_X + (TOKEN_WIDTH + BOARD_OFFSET)
PLAYER_START_Y = BOARD_OFFSET

PLAYER1_COLOR = 8
PLAYER2_COLOR = 6


class Board:
    def __init__(self):
        self.padding_x = (pyxel.width - BOARD_WIDTH) // 2
        self.slot_x = 0
        self.slot_y = 0
        self.slot_id = (0, 0)
        self.slots = []

    def drawBackground(self):
        pyxel.text(BOARD_OFFSET, BOARD_OFFSET, "Connect 4", 7)
        pyxel.rect(self.padding_x, PADDING_Y, BOARD_WIDTH, BOARD_HEIGHT, 10)
        pyxel.rect(0, TABLE_HEIGHT, pyxel.width, pyxel.height, 9)

    def drawGrid(self):
        for row in range(6):
            for col in range(7):
                self.slot_x = self.padding_x + BOARD_OFFSET + col * (TOKEN_WIDTH + BOARD_OFFSET)
                self.slot_y = PADDING_Y + BOARD_OFFSET + row * (TOKEN_HEIGHT + BOARD_OFFSET)
                self.slot_id = (self.slot_x, self.slot_y)
                pyxel.rect(self.slot_x, self.slot_y, TOKEN_WIDTH, TOKEN_HEIGHT, 0)
                self.slots.append(self.slot_id)


class Token:    
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.dropped = False
        self.player_color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR

    def update(self):
        self.updateFalling()

    def updateFalling(self):
        if self.dropped:
            self.y += TOKEN_GRAVITY

            if self.y >= TABLE_HEIGHT - TOKEN_HEIGHT:
                self.y = TABLE_HEIGHT - TOKEN_HEIGHT
                self.dropped = False

    def draw(self):
        pyxel.rect(self.x, self.y, TOKEN_WIDTH, TOKEN_HEIGHT, self.player_color)


class App:
    def __init__(self):
        pyxel.init(220, 220, title="Connect 4", fps=60)

        self.board = Board()

        self.tokens = [
            Token(PLAYER1_START_X, PLAYER_START_Y, 1),
            Token(PLAYER2_START_X, PLAYER_START_Y, 2)
        ]

        pyxel.run(self.update, self.draw)

    def update(self):
        for token in self.tokens:
            token.update()

    def draw(self):
        pyxel.cls(0)
        self.board.drawBackground()
        self.board.drawGrid()


App()