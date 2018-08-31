import PIL
import turtle
import math
import fractions

class Spiro:
    def __init__(self, xc, yc, col, R, r, l):
        self.turtle = turtle.Turtle()
        self.turtle.shape('turtle')
        self.step = 5
        self.DrawningComplete = False

        # ustawienie parametrów
        self.set_params(xc, yc, col, R, r, l)
        # start programu
        self.restart()

    def set_params(self, xc, yc, col, R, r, l):
        self.xc = xc, self.yc = yc  # współrzędne rysika
        self.col = col
        self.R = int(R)    # promień większego okręgu
        self.r = int(r)    # promień mniejszego
        self.l = l         # stosunek odcinka rysik-centrum mniejszego do r

        # największy wspólny dzielnik promieni
        NWDprom = fractions._gcd(self.r, self.R)
        self.nRot = self.r//NWDprom

        # stosunek promieni
        self.k = r/float(R)
        # ustawienie koloru
        self.turtle.color(*col)
        self.alpha = 0

    def restart(self):
        self.DrawningComplete = False
        self.turtle.showturtle()
        self.turtle.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((l-k)/k*a))
        y = R*((1-k)*math.sin(a) + l*k*math.sin((l-k)/k*a))
