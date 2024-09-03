# Brian Beard 2024

import pyxel

PADDING_Y = 40

BOARD_WIDTH = 160
BOARD_HEIGHT = 152
BOARD_OFFSET = 6
BOARD_BOTTOM = 172
BOARD_RIGHT_EDGE = 168
BOARD_LEFT_EDGE = 36

TABLE_HEIGHT = BOARD_HEIGHT + PADDING_Y

TOKEN_WIDTH = 16
TOKEN_HEIGHT = 16
TOKEN_GRAVITY = 4
TOKEN_OFFSET_X = TOKEN_WIDTH + BOARD_OFFSET

INITIAL_SPAWN_X = 102
INITIAL_SPAWN_Y = 18

PLAYER_COLOR_1 = 8
PLAYER_COLOR_2 = 6


class Board:
    def __init__(self):
        self.padding_x = (pyxel.width - BOARD_WIDTH) // 2
        self.slot_x = 0
        self.slot_y = 0
        self.slot_id = (0, 0)
        self.topSlot_id = (0, 0)        
        self.slots = []
        self.topSlots = []

    def drawBackground(self):
        pyxel.text(BOARD_OFFSET, BOARD_OFFSET, "Connect 4", 7)
        pyxel.rect(self.padding_x, PADDING_Y, BOARD_WIDTH, BOARD_HEIGHT, 10)
        pyxel.rect(0, TABLE_HEIGHT, pyxel.width, pyxel.height, 9)

    def drawGrid(self):
        for row in range(6):
            for col in range(7):
                self.slot_x = self.padding_x + BOARD_OFFSET + col * TOKEN_OFFSET_X
                self.slot_y = PADDING_Y + BOARD_OFFSET + row * (TOKEN_HEIGHT + BOARD_OFFSET)
                self.slot_id = (self.slot_x, self.slot_y)
                pyxel.rect(self.slot_x, self.slot_y, TOKEN_WIDTH, TOKEN_HEIGHT, 0)
                self.slots.append(self.slot_id)

    def createTopTokenSlots(self):
        for col in range(7):
            self.slot_x = self.padding_x + BOARD_OFFSET + col * TOKEN_OFFSET_X
            self.slot_y = (PADDING_Y - TOKEN_HEIGHT) - BOARD_OFFSET
            self.topSlot_id = (self.slot_x, self.slot_y)
            self.topSlots.append(self.topSlot_id)



class Token:    
    def __init__(self, x, y, count):
        self.x = x
        self.y = y
        self.dropped = False
        self.landed = False
        self.player_color = PLAYER_COLOR_2 if count % 2 == 0 else PLAYER_COLOR_1

    def update(self):
        if not self.landed:
            self.updateFalling()
            self.updateMovement()

    def updateFalling(self):
        if self.dropped:
            self.y += TOKEN_GRAVITY

            if self.isLanded():
                self.y = BOARD_BOTTOM - TOKEN_HEIGHT
                self.dropped = False
                self.landed = True

    def isLanded(self):
        return self.y >= BOARD_BOTTOM - TOKEN_HEIGHT

    def updateMovement(self):
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.x <= BOARD_RIGHT_EDGE - TOKEN_WIDTH:
            self.x += TOKEN_OFFSET_X
        elif pyxel.btnp(pyxel.KEY_LEFT) and self.x >= BOARD_LEFT_EDGE + TOKEN_WIDTH:
            self.x -= TOKEN_OFFSET_X
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.dropped = True


    def draw(self):
        pyxel.rect(self.x, self.y, TOKEN_WIDTH, TOKEN_HEIGHT, self.player_color)


class App:
    def __init__(self):
        pyxel.init(220, 220, title="Connect 4")

        self.tokens = []
        self.landedTokens = []
        self.token_count = 0

        self.board = Board()

        self.spawnToken()
        
        pyxel.run(self.update, self.draw)

    def spawnToken(self):
        self.token_count += 1
        token = Token(INITIAL_SPAWN_X, INITIAL_SPAWN_Y, self.token_count)
        self.tokens.append(token)
        return token

    def update(self):
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.spawnToken()
        for token in self.tokens:
            token.update()



    def draw(self):
        pyxel.cls(0)
        self.board.drawBackground()
        self.board.drawGrid()
        for token in self.tokens:
            token.draw()


App()