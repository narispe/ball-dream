from random import randint, random
import numpy as np


def randcolor():
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    return (r, g, b)


def randdir():
    theta = random()*2*np.pi
    return np.array([np.cos(theta), np.sin(theta)])


def randpoint(XMAX, YMAX):
    x = randint(0, XMAX)
    y = randint(0, YMAX)
    return np.array([x, y])


def to_point(vect, CX, CY, s=1):
    return np.round((CX + vect[0]*s, CY - vect[1]*s))


def to_vect(point, CX, CY, s=1):
    return np.round(np.array([(point[0]-CX)/s, (CY-point[1])/s, 0]))


def int_vect(v):
    return (int(v[0]), int(v[1]))


def ang_vect(vec):
    ang = np.arctan2(vec[1], vec[0])
    return ang


def angle_bet(v1, v2):
    theta1 = ang_vect(v1)
    theta2 = ang_vect(v2)
    theta = theta1 - theta2
    if theta < 0:
        theta += 2*np.pi
    if theta > np.pi:
        theta -= 2*np.pi
    return theta


def vect_vel(vect_dir, rap):
    if np.linalg.norm(vect_dir) > 0:
        ang = ang_vect(vect_dir)
        return rap*np.array([np.cos(ang), np.sin(ang)])
    else:
        return np.array([0, 0])


def descomp(v, n):  # vector velocidad en coorderanas c/r eje normal
    ang = angle_bet(v, n)
    norm = np.linalg.norm(v)
    return norm*np.cos(ang), norm*np.sin(ang)


def impulse(n, c1, c2, e=1):
    v1_n, v1_t = descomp(c1.vel, n)
    v2_n, v2_t = descomp(c2.vel, n)
    m1 = c1.radio**2
    m2 = c2.radio**2
    p_ini = m1*v1_n + m2*v2_n
    i1 = (e*m2*(v2_n-v1_n) + p_ini) / (m1+m2)
    i2 = (e*m1*(v1_n-v2_n) + p_ini) / (m1+m2)
    v1_r = np.array([i1, v1_t])
    v2_r = np.array([i2, v2_t])
    rap_1 = np.linalg.norm(v1_r)
    rap_2 = np.linalg.norm(v2_r)
    ang = ang_vect(n)
    ang_1 = ang_vect(v1_r) + ang
    ang_2 = ang_vect(v2_r) + ang
    new_v1 = rap_1*np.array([np.cos(ang_1), np.sin(ang_1)])
    new_v2 = rap_2*np.array([np.cos(ang_2), np.sin(ang_2)])
    return new_v1, rap_1, new_v2, rap_2
