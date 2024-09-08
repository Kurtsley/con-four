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
        self.slots = []
        self.landedTokens = []
        self.victory = False

    def createGrid(self):
        self.slots = []

        for col in range(7):
            col_slots = []
            for row in range(6):
                self.slot_x = self.padding_x + BOARD_OFFSET + col * TOKEN_SIZE
                self.slot_y = PADDING_Y + row * TOKEN_SIZE
                self.slot_id = (self.slot_x, self.slot_y)
                col_slots.append(self.slot_id)
            self.slots.append(col_slots)

    def checkGrid(self,tokens):
        for token in tokens:
            if token.landed and token not in self.landedTokens:
                self.landedTokens.append(token)

    def checkVictory(self):
        pass

    def drawBackground(self):
        pyxel.text(BOARD_OFFSET, BOARD_OFFSET, "Connect 4", 7)
        pyxel.rect(self.padding_x, PADDING_Y, BOARD_WIDTH, BOARD_HEIGHT, 5)
        pyxel.rect(0, TABLE_HEIGHT, pyxel.width, pyxel.height, 9)

    def drawGrid(self, slots):
        for row in range(len(slots)):
            for col in range(len(slots[row])):
                slot_x = slots[row][col][0]
                slot_y = slots[row][col][1]
                pyxel.rect(slot_x, slot_y, TOKEN_SIZE, TOKEN_SIZE, 0)


class Token:    
    def __init__(self, x, y, count):
        self.x = x
        self.y = y
        self.freshSpawn = True
        self.dropped = False
        self.landed = False
        self.player_color = PLAYER_COLOR_2 if count % 2 == 0 else PLAYER_COLOR_1

    def update(self, tokens, board):
        if not self.landed:
            self.updateFalling(tokens)
            self.updateMovement(board)

    def updateFalling(self, tokens):
        if self.dropped:
            self.y += TOKEN_GRAVITY
            self.checkCollisions(tokens)
    
    def hasLanded(self):
        return self.y >= BOARD_BOTTOM - TOKEN_SIZE
    
    def canSpawn(self, board):
        topSlots = []
        for col in range(7):
            slot = board.slots[col][0]
            topSlots.append(slot)

        for token in board.landedTokens:
            tokenTuple = (token.x, token.y)
            if tokenTuple in topSlots and self.x == token.x:
                    return False

        return True
    
    def checkCollisions(self, tokens):
        if self.hasLanded():
            self.y = BOARD_BOTTOM - TOKEN_SIZE
            self.dropped = False
            self.landed = True

        for other_token in tokens:
            if (self != other_token and 
                self.dropped and not 
                other_token.dropped and not 
                other_token.freshSpawn
            ):
                if self.y + TOKEN_SIZE >= other_token.y and self.x == other_token.x:
                    self.y = other_token.y - TOKEN_SIZE
                    self.dropped = False
                    self.landed = True

    def updateMovement(self, board):
        canSpawn = self.canSpawn(board)
        if (pyxel.btnp(pyxel.KEY_RIGHT) and 
            self.x <= BOARD_RIGHT_EDGE - TOKEN_SIZE and not 
            self.dropped
        ):
            self.x += TOKEN_SIZE

        elif (pyxel.btnp(pyxel.KEY_LEFT) and 
              self.x >= BOARD_LEFT_EDGE + TOKEN_SIZE and not 
              self.dropped):
            self.x -= TOKEN_SIZE

        elif pyxel.btnp(pyxel.KEY_SPACE) and canSpawn:
            self.dropped = True
            self.freshSpawn = False

    def draw(self):
        pyxel.rect(self.x, self.y, TOKEN_SIZE, TOKEN_SIZE, self.player_color)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Connect 4", fps=60)

        self.tokens = []
        self.token_count = 1

        self.board = Board()
        self.board.createGrid()

        self.spawnToken()
        
        pyxel.run(self.update, self.draw)

    def spawnToken(self):
        token = Token(INITIAL_SPAWN_X, INITIAL_SPAWN_Y, self.token_count)
        self.token_count += 1
        self.tokens.append(token)
        return token

    def update(self):
        for token in self.tokens:
            token.update(self.tokens, self.board)
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.spawnToken()
        self.board.checkGrid(self.tokens)

    def draw(self):
        pyxel.cls(0)
        self.board.drawBackground()
        self.board.drawGrid(self.board.slots)
        for token in self.tokens:
            token.draw()


App()