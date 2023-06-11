import numpy as np

def scale(scalar):
    return np.array([[scalar,      0,      0, 0],
                     [0     , scalar,      0, 0],
                     [0     ,      0, scalar, 0],
                     [0     ,      0,      0, 1]])

def rotateX(angle):
    return np.array([[1,             0,              0, 0],
                     [0, np.cos(angle), -np.sin(angle), 0],
                     [0, np.sin(angle),  np.cos(angle), 0],
                     [0,             0,              0, 1]])

def rotateY(angle):
    return np.array([[ np.cos(angle), 0, np.sin(angle), 0],
                     [0             , 1,             0, 0],
                     [-np.sin(angle), 0, np.cos(angle), 0],
                     [0             , 0,             0, 1]])

def rotateZ(angle):
    return np.array([[np.cos(angle), -np.sin(angle), 0, 0],
                     [np.sin(angle),  np.cos(angle), 0, 0],
                     [0            ,              0, 1, 0],
                     [0            ,              0, 0, 1]])

def translate(pos):
        tx, ty, tz = pos
        return np.array([
            [1 , 0 , 0 , 0],
            [0 , 1 , 0 , 0],
            [0 , 0 , 1 , 0],
            [tx, ty, tz, 1]
        ])