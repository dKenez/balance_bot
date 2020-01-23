from graphics import *
from math import sqrt, atan, inf, degrees, cos, sin, radians
import time


class Stick:
    __slots__ = ["mass", "vel", "acc", "ang_vel", "ang_acc", "ang", "center", "length",
                 "theta", "prev_acc", "prev_ang_acc"]

    def __init__(self, p1, p2, mass=float(1), vel=None, acc=None, ang_vel=0, ang_acc=0):
        # initialize defined values
        self.mass = mass if mass > 0 else 1
        self.vel = [0, 0] if vel is None else vel
        self.acc = [0, 0] if acc is None else acc
        self.ang_vel = ang_vel
        self.ang_acc = ang_acc

        self.prev_acc = [0, 0]
        self.prev_ang_acc = 0

        # initialize calculated values
        d_x = p1[0] - p2[0]
        d_y = p1[1] - p2[1]
        self.ang = atan(inf if not d_x else d_y/d_x)
        self.center = [p2[0] + d_x/2, p2[1] + d_y/2]
        self.length = sqrt(d_x**2 + d_y**2)
        self.theta = (mass * (self.length**2)) / 12

    def clear_accs(self):
        self.acc = [0, 0]
        self.ang_acc = 0

    def apply_force(self, force, point=None):
        point = self.center if point is None else point
        self.acc[0] += force[0] / self.mass
        self.acc[1] += force[1] / self.mass

        torque_x = (self.center[1] - point[1]) * force[0]
        torque_y = -(self.center[0] - point[0]) * force[1]

        self.ang_acc = (torque_x + torque_y)/self.theta

    def get_points(self):
        p1_x = self.center[0] - cos(self.ang)*self.length/2
        p1_y = self.center[1] - sin(self.ang) * self.length / 2
        p2_x = self.center[0] + cos(self.ang) * self.length / 2
        p2_y = self.center[1] + sin(self.ang) * self.length / 2
        return (p1_x, p1_y), (p2_x, p2_y)

    def update(self, delta_t):
        for dim in (0, 1):
            xpp_2 = self.prev_acc[dim]
            xpp_1 = self.acc[dim]
            xp_1 = self.vel[dim]
            x_1 = self.center[dim]

            xp_0 = xp_1 + ((3 * xpp_1 - xpp_2) / 2) * delta_t
            x_0 = x_1 + ((xp_0 + xp_1) / 2) * delta_t

            self.prev_acc[dim] = xpp_1

            self.vel[dim] = xp_0
            # self.center[dim] = 250
            self.center[dim] = x_0

        epp_2 = self.prev_ang_acc
        epp_1 = self.ang_acc
        ep_1 = self.ang_vel
        e_1 = self.ang

        ep_0 = ep_1 + ((3 * epp_1 - epp_2) / 2) * delta_t
        e_0 = e_1 + ((ep_0 + ep_1) / 2) * delta_t

        self.prev_ang_acc = epp_1

        self.ang_vel = ep_0
        self.ang = e_0


win_w = 500
win_h = 500
win = GraphWin("balance_bot", win_w, win_h)
win.setBackground("black")
win.setCoords(0, 0, win_w, win_h)

g = -9.81
t_inc = 0.01

P1 = (50, 50)
P2 = (150, 150)

my_stick = Stick(P1, P2, mass=0.1)
# print(vars(my_stick))
# print(my_stick.acc)
# print(my_stick.ang_acc)

G = (0, my_stick.mass * g)

# my_stick.apply_force(G)
#
# print(my_stick.acc)
# print(my_stick.ang_acc)
#
N = [3, 5]
# my_stick.apply_force(N, P1)
#
# print(my_stick.acc)
# print(my_stick.ang_acc)

line = Line(Point(P1[0], P1[1]), Point(P2[0], P2[1]))
line.draw(win)
line.setFill("white")
line.setWidth(3)

start_t = time.time()
curr_t = start_t
while win.checkMouse() is None:  # main program loop
    dt = time.time() - curr_t
    if dt > t_inc:
        win.delete("all")
        curr_t = time.time()
        my_stick.update(dt)
        P1, P2 = my_stick.get_points()
        line = Line(Point(P1[0], P1[1]), Point(P2[0], P2[1]))
        line.draw(win)
        line.setFill("white")
        line.setWidth(3)

        my_stick.clear_accs()
        my_stick.apply_force(G)
        my_stick.apply_force(N, P1) if time.time()-start_t < 1 else my_stick.apply_force((0, 0), P1)
        # print(my_stick.acc)

# win.getMouse() # Pause to view result
win.close()    # Close window when done