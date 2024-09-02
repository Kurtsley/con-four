# Brian Beard 2024

import pyxel

BOARD_WIDTH = 160
BOARD_HEIGHT = 152
BOARD_OFFSET = 6

TOKEN_WIDTH = 16
TOKEN_HEIGHT = 16
TOKEN_GRAVITY = 4

PLAYER_START_X = 190
PLAYER1_START_Y = 40
PLAYER2_START_Y = 66

PLAYER1_COLOR = 8
PLAYER2_COLOR = 6

PADDING_X = 10
PADDING_Y = 40


class Board:
    def __init__(self):
        self.slot_x = 0
        self.slot_y = 0
        self.slot_id = (0, 0)
        self.slots = []

    def drawBackground(self):
        pyxel.rect(PADDING_X, PADDING_Y, BOARD_WIDTH, BOARD_HEIGHT, 10)

    def drawGrid(self):
        for row in range(6):
            for col in range(7):
                self.slot_x = PADDING_X + BOARD_OFFSET + col * (TOKEN_WIDTH + BOARD_OFFSET)
                self.slot_y = PADDING_Y + BOARD_OFFSET + row * (TOKEN_HEIGHT + BOARD_OFFSET)
                self.slot_id = (self.slot_x, self.slot_y)
                pyxel.rect(self.slot_x, self.slot_y, TOKEN_WIDTH, TOKEN_HEIGHT, 0)
                self.slots.append(self.slot_id)


class Token:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.last_x, self.last_y = None, None
        self.dragging = False
        self.dropped = False
        self.player_color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR

    def update(self):
        if self.isWithin() and pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            if not self.dragging:
                self.dragging = True
                self.x, self.y = pyxel.mouse_x - BOARD_OFFSET, pyxel.mouse_y - BOARD_OFFSET
                self.last_x, self.last_y = pyxel.mouse_x, pyxel.mouse_y

            else:
                delta_x = pyxel.mouse_x - self.last_x
                delta_y = pyxel.mouse_y - self.last_y

                self.x += delta_x
                self.y += delta_y

                self.last_x, self.last_y = pyxel.mouse_x, pyxel.mouse_y

        else:
            if self.dragging:
                self.dragging = False
                self.dropped = True
        
        self.updateFalling()

    def updateFalling(self):
        if self.dropped:
            self.y += TOKEN_GRAVITY

    def isWithin(self) -> bool:
        mouse_within_x = self.x <= pyxel.mouse_x and pyxel.mouse_x <= (self.x + TOKEN_WIDTH)
        mouse_within_y = self.y <= pyxel.mouse_y and pyxel.mouse_y <= (self.y + TOKEN_HEIGHT)
        return mouse_within_x and mouse_within_y

    def draw(self):
        pyxel.rect(self.x, self.y, TOKEN_WIDTH, TOKEN_HEIGHT, self.player_color)


class App:
    def __init__(self):
        pyxel.init(220, 220, "Connect 4")
        pyxel.mouse(True)

        self.board = Board()
        self.token_1 = Token(PLAYER_START_X, PLAYER1_START_Y, 1)
        self.token_2 = Token(PLAYER_START_X, PLAYER2_START_Y, 2)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.token_1.update()
        self.token_2.update()

    def draw(self):
        pyxel.cls(0)
        self.board.drawBackground()
        self.board.drawGrid()
        self.token_1.draw()
        self.token_2.draw()        


App()