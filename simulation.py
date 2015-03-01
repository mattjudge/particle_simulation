from Tkinter import *
import math


class Vector(object):
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


class Particle(object):
    def __init__(self, x, y, q = 1, m = 100):
        self.charge = q # charge in Coulombs
        self.mass = m # mass in kg
        self.position = Vetor(x, y)
        self.velocity = Vector()
        self.acceleration = Vector()
        self._cachedForce = Vector()
        self.canvas_obj=canvas.create_oval(self.position.x,self.position.y,self.position.x+3,self.position.y+3,fill="blue")

    def tick(self, dt):
        self.acceleration.x += self._cachedForce.x / self.mass
        self.acceleration.y += self._cachedForce.y / self.mass
        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        canvas.move(self.canvas_obj,self.position.x, self.position.y)


class System(object):
    def __init__(self):
        self.particles = []
        self.ticks = 0

    def addParticle(self, particle):
        self.particles.append(particle)

    def chargeForce(self, Q, q, R):
        return 8.988e9 * Q * q / R ** 2

    def gravityForce(self, M, m, R):
        return 6.67e-34 * M * m / R ** 2

    def tick(self, dt):

        for p in self.particles:
            for q in self.particles:
                if p != q:
                    fx = self.chargeForce(p.charge, q.charge, q.position.x - p.position.x) + \
                         self.gravityForce(p.mass, q.mass, q.position.x - p.position.x)
                    fy = self.chargeForce(p.charge, q.charge, q.position.y - p.position.y) + \
                         self.gravityForce(p.mass, q.mass, q.position.y - p.position.y)
                    p._cachedForce.x += fx
                    p._cachedForce.y += fy

        for p in self.particles:
            p.tick()

        self.ticks += 1



window = Tk()
canvas = Canvas(window, width = 400, height = 300)
canvas.pack()


s = System()
s.addParticle(Particle(25, 25))
s.addParticle(Particle(50, 25))

while(True):
    s.tick(1)


