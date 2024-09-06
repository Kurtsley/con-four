# Brian Beard 2024

import pyxel

SCREEN_HEIGHT = 180
SCREEN_WIDTH = 180

PADDING_Y = 40

TOKEN_SIZE = 16
TOKEN_GRAVITY = 4

BOARD_WIDTH = 124
BOARD_HEIGHT = 112
BOARD_OFFSET = 6
BOARD_BOTTOM = BOARD_HEIGHT + PADDING_Y - TOKEN_SIZE
BOARD_RIGHT_EDGE = 138
BOARD_LEFT_EDGE = 28

TABLE_HEIGHT = BOARD_HEIGHT + PADDING_Y

INITIAL_SPAWN_X = 82
INITIAL_SPAWN_Y = 18

PLAYER_COLOR_1 = 8
PLAYER_COLOR_2 = 10


class Board:
    def __init__(self):
        self.padding_x = (pyxel.width - BOARD_WIDTH) // 2
        self.slot_x = 0
        self.slot_y = 0
        self.slot_id = (0, 0)
        self.topSlot_id = (0, 0)        
        self.slots = []
        self.topSlots = []
        self.takenSlots = []

    def drawBackground(self):
        pyxel.text(BOARD_OFFSET, BOARD_OFFSET, "Connect 4", 7)
        pyxel.rect(self.padding_x, PADDING_Y, BOARD_WIDTH, BOARD_HEIGHT, 5)
        pyxel.rect(0, TABLE_HEIGHT, pyxel.width, pyxel.height, 9)

    def drawGrid(self):
        for row in range(6):
            for col in range(7):
                self.slot_x = self.padding_x + BOARD_OFFSET + col * TOKEN_SIZE
                self.slot_y = PADDING_Y + row * TOKEN_SIZE
                pyxel.rect(self.slot_x, self.slot_y, TOKEN_SIZE, TOKEN_SIZE, 0)


class Token:    
    def __init__(self, x, y, count):
        self.x = x
        self.y = y
        self.dropped = False
        self.landed = False
        self.player_color = PLAYER_COLOR_2 if count % 2 == 0 else PLAYER_COLOR_1
        self.landedTokens = []


    def update(self, tokens):
        if not self.landed:
            self.updateFalling(tokens)
            self.updateMovement()

    def updateFalling(self, tokens):
        if self.dropped:
            self.y += TOKEN_GRAVITY
            self.checkCollision(tokens)
        
    def checkCollision(self, tokens):
        for token in tokens:
          if token != self and token.landed and self.hasCollided(token):
                self.y = token.y - TOKEN_SIZE
                self.dropped = False
                self.landed = True
                self.landedTokens.append(self)
        
    def hasCollided(self, token):
        return (
            self.x == token.x and
            self.y >= token.y - TOKEN_SIZE or
            self.y >= BOARD_BOTTOM - TOKEN_SIZE
        )
    
    def hasLanded(self):
        return self.y >= BOARD_BOTTOM - TOKEN_SIZE

    def updateMovement(self):
        if pyxel.btnp(pyxel.KEY_RIGHT) and self.x <= BOARD_RIGHT_EDGE - TOKEN_SIZE and not self.dropped:
            self.x += TOKEN_SIZE
        elif pyxel.btnp(pyxel.KEY_LEFT) and self.x >= BOARD_LEFT_EDGE + TOKEN_SIZE and not self.dropped:
            self.x -= TOKEN_SIZE
        elif pyxel.btnp(pyxel.KEY_SPACE):
            self.dropped = True


    def draw(self):
        pyxel.rect(self.x, self.y, TOKEN_SIZE - 1, TOKEN_SIZE -1, self.player_color)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Connect 4")

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
            token.update(self.tokens)

            



    def draw(self):
        pyxel.cls(0)
        self.board.drawBackground()
        self.board.drawGrid()
        for token in self.tokens:
            token.draw()


App()