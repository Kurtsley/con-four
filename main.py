# Brian Beard 2024

import pyxel


TOKEN_WIDTH = 16
TOKEN_HEIGHT = 16

PLAYER_START_X = 196
PLAYER1_START_Y = 40
PLAYER2_START_Y = 66

PLAYER1_COLOR = 8
PLAYER2_COLOR = 6

PADDING_X = 10
PADDING_Y = 20


class Token:
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player_color = PLAYER1_COLOR if player == 1 else PLAYER2_COLOR
        self.dropped = False
        self.dragged = False
        self.isWithin = False

    def update(self):
        if self.x <= pyxel.mouse_x and pyxel.mouse_x <= (self.x + TOKEN_WIDTH) and self.y <= pyxel.mouse_y and pyxel.mouse_y <= (self.y + TOKEN_HEIGHT):
            print(f"within {self.player_color}")

    def isWithin(self):
        pass

    def isDragged(self):
        pass

    def draw(self):
        pyxel.rect(self.x, self.y, TOKEN_WIDTH, TOKEN_HEIGHT, self.player_color)


class App:
    def __init__(self):
        pyxel.init(220, 220, "Connect 4")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")

        self.token_1 = Token(PLAYER_START_X, PLAYER1_START_Y, 1)
        self.token_2 = Token(PLAYER_START_X, PLAYER2_START_Y, 2)

        pyxel.run(self.update, self.draw)

    def update(self):
        self.token_1.update()
        self.token_2.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(PADDING_X, PADDING_Y, 0, 0, 0, 200, 200)
        self.token_1.draw()
        self.token_2.draw()
        


App()