from Tkinter import *
import math
import time

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
        self.position = Vector(x, y)
        self.velocity = Vector()
        self.acceleration = Vector()
        self._cachedForce = Vector()
        self.canvas_obj=canvas.create_oval(self.position.x, self.position.y,
                                           self.position.x+3, self.position.y+3,
                                           fill = "red" if q > 0 else "blue")

    def tick(self, dt):
        self.acceleration.x = self._cachedForce.x / self.mass
        self.acceleration.y = self._cachedForce.y / self.mass
        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt
        oldx = self.position.x
        oldy = self.position.y
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        canvas.move(self.canvas_obj, self.position.x - oldx, self.position.y - oldy)


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
            p._cachedForce.x = 0
            p._cachedForce.y = 0
            for q in self.particles:
                if p != q:
                    x = q.position.x - p.position.x
                    y = q.position.y - p.position.y
                    r = math.sqrt(x**2 + y**2)
                    F = -self.chargeForce(p.charge, q.charge, r) + \
                         self.gravityForce(p.mass, q.mass, r)
                    Fx = F*x / r
                    Fy = F*y / r
                    p._cachedForce.x += Fx
                    p._cachedForce.y += Fy
        for p in self.particles:
            p.tick(dt)

        self.ticks += 1



root = Tk()
root.title("Simulation")

frame = Frame(root, bd=5)
frame.pack()
canvas = Canvas(frame, width=400, height=300)
canvas.pack()
root.update()


s = System()
s.addParticle(Particle(25, 25, -5e-3, 30))
s.addParticle(Particle(50, 50, 3e-3, 70))
s.addParticle(Particle(75, 25, 3e-3, 50))
s.addParticle(Particle(25, 50, -8e-3, 130))
s.addParticle(Particle(50, 25, 4e-3, 70))
s.addParticle(Particle(75, 50, 1e-3, 10))

last_tick_time = time.time()

while(True):
    tick_start_time = time.time()
    dt = tick_start_time - last_tick_time
    s.tick(dt)
    last_tick_time = tick_start_time
    for p in s.particles:
        print p.position.x, p.position.y
    print "dt", dt
    root.update()
    time.sleep(1.0/60)





