from Tkinter import *
import math
import time


class Vector(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


class Particle(object):
    def __init__(self, x, y, q=1, m=100):
        self.charge = q  # charge in Coulombs
        self.mass = m  # mass in kg
        self.position = Vector(x, y)
        self.velocity = Vector()
        self.acceleration = Vector()
        self._cachedForce = Vector()
        self.canvas_obj = canvas.create_oval(self.position.x, self.position.y,
                                             self.position.x+3, self.position.y+3,
                                             fill="red" if q > 0 else "blue")

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

    def add_particle(self, particle):
        self.particles.append(particle)

    def charge_force(self, q1, q2, r):
        return 8.988e9 * q1 * q2 / r ** 2

    def gravity_force(self, m1, m2, r):
        return 6.67e-34 * m1 * m2 / r ** 2

    def tick(self, dt):
        for p in self.particles:
            p._cachedForce.x = 0
            p._cachedForce.y = 0
            for q in self.particles:
                if p != q:
                    x = q.position.x - p.position.x
                    y = q.position.y - p.position.y
                    r = math.sqrt(x**2 + y**2)
                    F = -self.charge_force(p.charge, q.charge, r) + \
                        self.gravity_force(p.mass, q.mass, r)
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
s.add_particle(Particle(25, 25, -3e-3, 50))
s.add_particle(Particle(50, 50, 3e-3, 50))
s.add_particle(Particle(75, 25, 3e-3, 50))
s.add_particle(Particle(25, 50, -3e-3, 50))
s.add_particle(Particle(50, 25, 3e-3, 50))
s.add_particle(Particle(75, 50, -3e-3, 50))

last_tick_time = time.time()

while True:
    tick_start_time = time.time()
    dt = tick_start_time - last_tick_time
    s.tick(dt)
    last_tick_time = tick_start_time
    for p in s.particles:
        print p.position.x, p.position.y
    print "dt", dt
    root.update()
    time.sleep(1.0/60)
