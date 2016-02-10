from tkinter import *
import time
import subprocess
from os import makedirs


def charge_force(q1, q2, r):
    return 8.988e9 * q1 * q2 / r ** 2


def gravity_force(m1, m2, r):
    return 6.67e-34 * m1 * m2 / r ** 2


class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        # only works when other is of numeric type
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        # only works when other is of numeric type
        return Vector2(self.x / other, self.y / other)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def magnitude(self):
        return self.__abs__()


class Particle(object):
    def __init__(self, x, y, q=1, m=100):
        self.charge = q  # charge in Coulombs
        self.mass = m  # mass in kg
        self.radius = 4
        self.position = Vector2(x, y)
        self.velocity = Vector2()
        self.acceleration = Vector2()
        self._cachedForce = Vector2()
        self.canvas_obj = canvas.create_oval(self.position.x-self.radius, self.position.y-self.radius,
                                             self.position.x+self.radius, self.position.y+self.radius,
                                             fill="red" if q > 0 else "blue")

    def clear_cached_forces(self):
        self._cachedForce = Vector2()

    def add_cached_force(self, f):
        self._cachedForce += f

    def tick(self, dt):
        self.acceleration = self._cachedForce / self.mass
        self.velocity += self.acceleration * dt
        oldx = self.position.x
        oldy = self.position.y
        self.position += self.velocity * dt
        canvas.move(self.canvas_obj, self.position.x - oldx, self.position.y - oldy)

    def in_frame(self):
        return 0 <= self.position.x <= canvas.winfo_width() and 0 <= self.position.y <= canvas.winfo_height()


class System(object):
    def __init__(self):
        self.particles = []
        self.ticks = 0
        self.completed = False

    def add_particle(self, particle):
        self.particles.append(particle)

    def tick(self, dt):
        for p in self.particles:
            p.clear_cached_forces()
            for q in self.particles:
                if p != q:
                    pq = q.position - p.position
                    r = abs(pq)
                    force = -charge_force(p.charge, q.charge, r) + \
                        gravity_force(p.mass, q.mass, r)
                    p.add_cached_force(pq * force / r)

        for p in self.particles:
            p.tick(dt)
            for q in self.particles:
                if p != q:
                    # check for collisions
                    pass

        self.completed = len([p for p in self.particles if p.in_frame()]) == 0
        self.ticks += 1


def save_frame():
    makedirs('./frames/', exist_ok=True)
    if s.ticks % 5 == 0 or s.ticks == 1 or s.completed:
        ps = canvas.postscript(colormode='color', width=canvas.winfo_width(), height=canvas.winfo_height())
        with open('./frames/frame_{0:06d}.ps'.format(s.ticks), 'w') as f:
            f.write(ps)


def convert_frames():
    subprocess.check_call('convert -dispose background -delay 8 frame_*.ps anim.gif', shell=True)


if __name__ == "__main__":

    root = Tk()
    root.title("Simulation")

    frame = Frame(root, bd=0)
    frame.pack()
    canvas = Canvas(frame, width=400, height=300)
    canvas.pack()
    root.update()

    s = System()
    s.add_particle(Particle(50, 50, -3e-3, 50))
    s.add_particle(Particle(100, 100, 3e-3, 50))
    s.add_particle(Particle(150, 50, 3e-3, 50))
    s.add_particle(Particle(50, 100, -3e-3, 50))
    s.add_particle(Particle(100, 50, 3e-3, 50))
    s.add_particle(Particle(150, 100, -3e-3, 50))

    last_tick_time = time.time()
    frame = 0

    while not s.completed:
        tick_start_time = time.time()
        # dt = tick_start_time - last_tick_time  # realtime
        dt = 1.0/60  # 60 ticks a second
        s.tick(dt)
        last_tick_time = tick_start_time
        for p in s.particles:
            print(p.position.x, p.position.y)
        print("dt", dt)
        root.update()
        save_frame()
        time.sleep(1.0/60)
        frame += 1

    # convert_frames()
