from PIL import Image
import turtle
import math
import fractions
import random
import datetime
import argparse
import sys

class Spiro:
    def __init__(self, xc, yc, turtle_color, R, r, l):
        self.turtle = turtle.Turtle()
        self.turtle.shape('turtle')
        self.step = 5
        self.DrawningComplete = False

        self.set_params(xc, yc, turtle_color, R, r, l)
        self.restart()

    def set_params(self, xc, yc, turtle_color, R, r, l):
        self.xc = xc
        self.yc = yc  # współrzędne początkowe rysika
        self.turtle_color = turtle_color
        self.R = int(R)    # promień większego okręgu
        self.r = int(r)    # promień mniejszego
        self.l = l         # stosunek odcinka rysik-centrum mniejszego do r

        # największy wspólny dzielnik promieni
        NWDprom = fractions._gcd(self.r, self.R)
        self.nRot = self.r//NWDprom

        # stosunek promieni
        self.k = r/float(R)

        self.turtle.color(*turtle_color)
        self.alpha = 0

    def restart(self):
        self.DrawningComplete = False
        self.turtle.showturtle()
        self.turtle.up()
        r, k, l = self.R, self.k, self.l
        a = 0.0
        x = r*((1-k)*math.cos(a) + l*k*math.cos((l-k)*a/k))
        y = r*((1-k)*math.sin(a) - l*k*math.sin((l-k)*a/k))
        self.turtle.setpos(self.xc + x, self.yc + y)
        self.turtle.down()

    def draw(self):
        r, l, k = self.R, self.l, self.k
        for point in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(point)
            x = r * ((1 - k) * math.cos(a) + l * k * math.cos((l - k)*a/k))
            y = r * ((1 - k) * math.sin(a) - l * k * math.sin((l - k)*a/k))
            self.turtle.setpos(self.xc + x, self.yc + y)
        self.turtle.hideturtle()    # kończymy rysowanie

    def update(self):
        if self.DrawningComplete:
            return
        self.alpha += self.step
        r, k, l = self.R, self.k, self.l
        a = math.radians(self.alpha)
        x = r * ((1 - k) * math.cos(a) + l * k * math.cos((l - k) / k * a))
        y = r * ((1 - k) * math.sin(a) + l * k * math.sin((l - k) / k * a))
        self.turtle.setpos(self.xc + x, self.yc + y)
        if self.alpha > 360*self.nRot:
            self.DrawningComplete = True
            self.turtle.hideturtle()

    def clear(self):
        self.turtle.clear()


class SpiroAnimator():
    def __init__(self, N):
        self.delatTime = 10
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        self.spirografy = []
        for i in range(N):
            randomparams = self.genRandomParams()   # tutaj otrzymujemy krotkę randomparams
            spiro = Spiro(*randomparams)    # spino oczekuje listy więc Python poprzez znak * konwertuje krotkę do niej
            self.spirografy.append(spiro)
        #timer
        turtle.ontimer(self.update, self.delatTime)

    def genRandomParams(self):
        height = self.height
        width = self.width
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)     # // zwraca liczbe całkowitą dzielnie 9//7 = 1
        l = random.uniform(0.1, 0.9)    # randint dla zmiennoprzecinkowych
        xc = random.randint(-width//2, height//2)
        yc = random.randint(-height//2, width//2)
        color = (random.random(), random.random(), random.random())
        return (xc, yc, color, R, r, l)

    def mass_restart(self):
        for spiro in self.spirografy:
            spiro.clear()
            random_params = self.genRandomParams()
            spiro.set_params(*random_params)
            spiro.restart()

    def update(self):
        nComplete = 0
        for spiro in self.spirografy:
            spiro.update()
            if spiro.DrawningComplete:
                nComplete += 1
        if nComplete == len(self.spirografy):
            self.mass_restart()
        turtle.ontimer(self.update(), self.delatTime)

    def toogle_turtle(self):
        for sprio in self.spirografy:
            if sprio.turtle.isvisible():
                sprio.turtle.hideturtle()
            else:
                sprio.turtle.showturtle

def saving_sprio():
    turtle.hideturtle()
    # generowanie nazwy pliku
    date_string = (datetime.datetime.now()).strftime("%d%b%Y - %H%M%S")     # TODO sprawdzi czy wielkość liter ma znaczenie
    file_name = 'spiro-' + date_string
    print('zapisywanie do pliku %s.png' % file_name)
    canvas = turtle.getcanvas()
    canvas.postscript(file=file_name + '.eps')
    # użycie modułu pillow do zapisu jako png
    img = Image.open(file_name + '.eps')
    #img.save(file_name + '.png', 'png')
    turtle.showturtle()


def main():
    user_descryption = ''
    parser = argparse.ArgumentParser(description=user_descryption)
    parser.add_argument('-sparams', nargs=4, required=False, dest='sparams', help='Trzy argumenty w sparams: \
                        R, k, l')
    args=parser.parse_args()
    turtle.setup(width=0.8)
    turtle.shape('turtle')
    turtle.title('TURTLE')
    turtle.onkey(saving_sprio(), 's')
    turtle.listen()     # okno nasłuchuje zdarzeń uzytkownika
    turtle.hideturtle()

    if args.sparams:
        params = [float(x) for x in args.sparams]
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0.0, 0.0, col, *params)   # * konwertuje listę na parametry
        spiro.draw()
    else:
        spiro = SpiroAnimator(6)
        turtle.onkey(spiro.toogle_turtle(), 't')
        turtle.onkey(spiro.mass_restart(), 'space')

    turtle.mainloop()

if __name__ == '__main__':
    main()