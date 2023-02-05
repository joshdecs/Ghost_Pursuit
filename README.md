Pasta Pursuit
import pyxel

class Personnage:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1
        if pyxel.btn(pyxel.KEY_SPACE) and self.vy == 0:
            self.vy = -5
        self.y += self.vy
        if self.y >= 100:
            self.y = 100
            self.vy = 0

class App:
    def __init__(self):
        pyxel.init(200, 200)
        self.personnage = Personnage(100, 100)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.personnage.update()

    def draw(self):
        pyxel.cls(0)
        pyxel.circ(self.personnage.x, self.personnage.y, 5, 9)

App()
