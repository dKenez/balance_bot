from graphics import *
from math import sqrt, atan, inf, degrees, cos, sin, radians
import time
from collections import deque


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
        if d_x:
            self.ang = atan(d_y / d_x)
        elif d_y > 0:
            self.ang = atan(inf)
        else:
            self.ang = atan(-inf)
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

        self.ang_acc += (torque_x + torque_y)/self.theta
        # print(self.ang_acc)

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
            # x_0 = 250
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
        # print(self.prev_ang_acc)

        self.ang_vel = ep_0
        self.ang = e_0


def draw_force(force, f_point):
    global f_mag
    f_x1 = force[0]
    f_y1 = force[1]

    if f_x1:
        ang = atan(f_y1 / f_x1)
    elif f_y1 > 0:
        ang = atan(inf)
    else:
        ang = atan(-inf)

    arr_len = sqrt(f_x1**2 + f_y1**2) * f_mag

    f_s_x = f_point[0] - cos(ang) * arr_len
    f_s_y = f_point[1] - sin(ang) * arr_len
    f_line = Line(Point(f_s_x, f_s_y), Point(f_point[0], f_point[1]))
    f_line.setFill("blue")
    f_line.setWidth(2)
    f_line.setArrow("last")
    f_line.draw(win)


win_w = 500
win_h = 500
win = GraphWin("balance_bot", win_w, win_h)
win.setBackground("black")
win.setCoords(0, 0, win_w, win_h)

g = -10
t_inc = 0.01
f_mag = 30

P1 = (50, 200)
P2 = (150, 300)

my_stick = Stick(P1, P2, mass=0.11)
# print(vars(my_stick))
# print(my_stick.acc)
# print(my_stick.ang_acc)

G = (0, my_stick.mass * g)

# print(G)

# my_stick.apply_force(G)
#
# print(my_stick.acc)
# print(my_stick.ang_acc)
#
N_1 = [3, 2.7]
# N_2 = [2, -2]

N_1_time = 1
# N_2_time = 0.5
# my_stick.apply_force(N, P1)
#
# print(my_stick.acc)
# print(my_stick.ang_acc)

line = Line(Point(P1[0], P1[1]), Point(P2[0], P2[1]))
line.setFill("white")
line.setWidth(3)
line.draw(win)

com_line = deque([Point(my_stick.center[0], my_stick.center[1])], maxlen=100)
poly_com = Polygon(list(com_line))
poly_com.setOutline("red")
poly_com.setWidth(1)
poly_com.draw(win)

start_t = time.time()
curr_t = start_t
while win.checkMouse() is None:  # main program loop
    dt = time.time() - curr_t
    if dt > t_inc:
        win.delete("all")
        curr_t = time.time()
        my_stick.update(dt)

        com_line.extend([Point(my_stick.center[0], my_stick.center[1])])
        poly_com = Polygon(list(com_line))
        poly_com.setOutline("red")
        poly_com.setWidth(1)
        poly_com.draw(win)

        P1, P2 = my_stick.get_points()
        line = Line(Point(P1[0], P1[1]), Point(P2[0], P2[1]))
        line.setFill("white")
        line.setWidth(3)
        line.draw(win)

        my_stick.clear_accs()
        my_stick.apply_force(G)
        draw_force(G, my_stick.center)
        my_stick.apply_force(N_1, P1) if time.time() - start_t < N_1_time else my_stick.apply_force((0, 0), P1)
        draw_force(N_1, P1) if time.time() - start_t < N_1_time else my_stick.apply_force((0, 0), P1)
        # my_stick.apply_force(N_2, P2) if time.time() - start_t < N_2_time else my_stick.apply_force((0, 0), P2)
        # draw_force(N_2, P2) if time.time() - start_t < N_2_time else my_stick.apply_force((0, 0), P2)
        # print(my_stick.acc)

# win.getMouse() # Pause to view result
win.close()    # Close window when done