# Brian Beard 2024
# title: Con-Four
# author: Kurtsley
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or distribute
# this software, either in source code form or as a compiled binary, for any
# purpose, commercial or non-commercial, and by any means.

import pyxel

SCREEN_HEIGHT = 180
SCREEN_WIDTH = 180

CHARACTER_WIDTH = 2

PADDING_Y = 40

TOKEN_SIZE = 17
TOKEN_CIRC = 8
TOKEN_GRAVITY = 4

BOARD_WIDTH = 133
BOARD_HEIGHT = 119
BOARD_OFFSET = 6
BOARD_BOTTOM = BOARD_HEIGHT + PADDING_Y - TOKEN_SIZE
BOARD_RIGHT_EDGE = 138
BOARD_LEFT_EDGE = 29

TABLE_HEIGHT = BOARD_HEIGHT + PADDING_Y

INITIAL_SPAWN_X = 80
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
                # Subtract 1 from slot_x to fix grid offset
                self.slot_x = self.padding_x + BOARD_OFFSET + col * TOKEN_SIZE - 1
                self.slot_y = PADDING_Y + row * TOKEN_SIZE
                self.slot_id = (self.slot_x, self.slot_y)
                col_slots.append(self.slot_id)
            self.slots.append(col_slots)

    def checkGrid(self, tokens):
        for token in tokens:
            if token.landed and token not in self.landedTokens:
                self.landedTokens.append(token)

    def checkVictory(self, tokens):
        for row in range(len(self.slots)):
            for col in range(len(self.slots[row])):
                slot_x = self.slots[row][col][0]
                slot_y = self.slots[row][col][1]
                slot_color = pyxel.pget(
                    slot_x + TOKEN_CIRC, slot_y + TOKEN_CIRC)
                # Increment by one to line up the victory check
                slot_x += 1

                if slot_color == 0:
                    continue

                if col <= len(self.slots[row]) - 4:
                    if all(pyxel.pget(self.slots[row][col + i][0] + TOKEN_CIRC, self.slots[row][col + i][1] + TOKEN_CIRC)
                           == slot_color for i in range(4)):
                        for token in tokens:
                            if token.x == slot_x and token.y == slot_y and token.landed:
                                return True

                if row <= len(self.slots) - 4:
                    if all(pyxel.pget(self.slots[row + i][col][0] + TOKEN_CIRC, self.slots[row + i][col][1] + TOKEN_CIRC)
                           == slot_color for i in range(4)):
                        for token in tokens:
                            if token.x == slot_x and token.y == slot_y and token.landed:
                                return True

                if row <= len(self.slots) - 4 and col <= len(self.slots[row]) - 4:
                    if all(pyxel.pget(self.slots[row + i][col + i][0] + TOKEN_CIRC, self.slots[row + i][col + i][1] + TOKEN_CIRC)
                           == slot_color for i in range(4)):
                        for token in tokens:
                            if token.x == slot_x and token.y == slot_y and token.landed:
                                return True

                if row <= len(self.slots) - 4 and col >= 3:
                    if all(pyxel.pget(self.slots[row + i][col - i][0] + TOKEN_CIRC, self.slots[row + i][col - i][1] + TOKEN_CIRC)
                           == slot_color for i in range(4)):
                        for token in tokens:
                            if token.x == slot_x and token.y == slot_y and token.landed:
                                return True

        return False

    def hasSpawnToken(self, tokens):
        for token in tokens:
            if token.freshSpawn:
                return True

        return False

    def canDrop(self, token):
        topSlots = []
        for col in range(7):
            slot = self.slots[col][0]
            topSlots.append(slot)

        for other_token in self.landedTokens:
            tokenTuple = (other_token.x - 1, other_token.y)
            if tokenTuple in topSlots and token.x == other_token.x:
                return False

        return True

    def updateMovement(self, token):
        canDrop = self.canDrop(token)
        if (pyxel.btnp(pyxel.KEY_RIGHT) and
                token.x <= BOARD_RIGHT_EDGE - TOKEN_SIZE and not
                token.dropped and not token.landed and not token.fallingToken
                ):
            token.x += TOKEN_SIZE

        elif (pyxel.btnp(pyxel.KEY_LEFT) and
                token.x >= BOARD_LEFT_EDGE + TOKEN_SIZE and not
                token.dropped and not token.landed and not token.fallingToken
              ):
            token.x -= TOKEN_SIZE

        elif pyxel.btnp(pyxel.KEY_SPACE) and canDrop:
            token.dropped = True
            token.freshSpawn = False

    def drawBackground(self):
        pyxel.text(BOARD_OFFSET, BOARD_OFFSET, "Connect 4", 7)
        # Subtract board width by 2 to fix grid offset
        pyxel.rect(self.padding_x, PADDING_Y, BOARD_WIDTH - 2, BOARD_HEIGHT, 5)
        pyxel.rect(0, TABLE_HEIGHT, pyxel.width, pyxel.height, 9)

    def drawGrid(self):
        for row in range(len(self.slots)):
            for col in range(len(self.slots[row])):
                slot_x = self.slots[row][col][0]
                slot_y = self.slots[row][col][1]
                pyxel.rect(slot_x + 1, slot_y, TOKEN_SIZE, TOKEN_SIZE, 0)


class Token:
    def __init__(self, x, y, count):
        self.x = x
        self.y = y
        self.freshSpawn = True
        self.dropped = False
        self.landed = False
        self.player_color = PLAYER_COLOR_2 if count % 2 == 0 else PLAYER_COLOR_1
        self.fallingToken = None

    def update(self, tokens, board):
        if not self.landed:
            self.updateFalling(tokens)
            board.updateMovement(self)

    def updateFalling(self, tokens):
        if self.dropped:
            self.fallingToken = self
            self.y += TOKEN_GRAVITY
            self.checkCollisions(tokens)

    def hasLanded(self):
        return self.y >= BOARD_BOTTOM - TOKEN_SIZE

    def checkCollisions(self, tokens):
        if self.hasLanded():
            pyxel.play(0, 0)
            self.y = BOARD_BOTTOM - TOKEN_SIZE
            self.dropped = False
            self.landed = True
            self.fallingToken = None

        for other_token in tokens:
            if (self != other_token and
                    self.dropped and not
                    other_token.dropped and not
                    other_token.freshSpawn
                    ):
                if self.y + TOKEN_SIZE >= other_token.y and self.x == other_token.x:
                    pyxel.play(0, 0)
                    self.y = other_token.y - TOKEN_SIZE
                    self.dropped = False
                    self.landed = True
                    self.fallingToken = None

    def draw(self):
        pyxel.circ(self.x + TOKEN_CIRC, self.y + TOKEN_CIRC,
                   TOKEN_CIRC, self.player_color)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Connect 4", fps=60)

        self.set_sounds()

        self.new_game = True
        self.game_over = False

        self.tokens = []
        self.token_count = 1

        self.board = Board()
        self.board.createGrid()

        self.spawnToken()

        pyxel.run(self.update, self.draw)

    def spawnToken(self):
        token = Token(INITIAL_SPAWN_X, INITIAL_SPAWN_Y, self.token_count)
        if token not in self.tokens:
            self.token_count += 1
            self.tokens.append(token)

    def resetGame(self):
        self.tokens.clear()
        self.token_count = 3 - self.token_count
        self.game_over = False
        self.new_game = True
        self.spawnToken()

    def update(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.new_game = False
        if not self.game_over:
            for token in self.tokens:
                token.update(self.tokens, self.board)
                if not token.fallingToken and not self.board.hasSpawnToken(self.tokens) \
                        and not token.landed:
                    self.spawnToken()
                    break
            self.board.checkGrid(self.tokens)
            if self.board.checkVictory(self.tokens):
                self.game_over = True
        else:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.resetGame()

    def draw(self):
        pyxel.cls(0)
        if self.new_game:
            instructions_text = "Arrows to move, space to drop"
            pyxel.text(pyxel.width // 2 - len(instructions_text),
                       BOARD_OFFSET, instructions_text, pyxel.COLOR_WHITE)
        if self.game_over:
            for token in self.tokens:
                if token.freshSpawn:
                    color = token.player_color
                    player1_victory = "Player 1 Wins!"
                    player2_victory = "Player 2 Wins!"

                    # The color is reversed becuase I am checking for
                    # the color of the spawn token, which is the opposite
                    # of the winning color...
                    if color == PLAYER_COLOR_1:
                        pyxel.text(pyxel.width // 2 - (len(player2_victory) * CHARACTER_WIDTH), BOARD_OFFSET,
                                   player2_victory, PLAYER_COLOR_2)

                    else:
                        pyxel.text(pyxel.width // 2 - (len(player1_victory) * CHARACTER_WIDTH), BOARD_OFFSET,
                                   player1_victory, PLAYER_COLOR_1)

            pyxel.text(pyxel.width // 2 + 20, BOARD_OFFSET + 15,
                       "SPACE to reset", pyxel.COLOR_LIME)

        self.board.drawBackground()
        self.board.drawGrid()
        for token in self.tokens:
            token.draw()

    def set_sounds(self):
        pyxel.sounds[0].set("c3", "s", "3", "n", 1)


App()
