
import numpy as np


def translation(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ], dtype=float)


def scaling(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ], dtype=float)


def rotation_x(angle):
    a = np.radians(angle)
    c, s = np.cos(a), np.sin(a)

    return np.array([
        [1, 0, 0, 0],
        [0, c, -s, 0],
        [0, s, c, 0],
        [0, 0, 0, 1]
    ])


def rotation_y(angle):
    a = np.radians(angle)
    c, s = np.cos(a), np.sin(a)

    return np.array([
        [c, 0, s, 0],
        [0, 1, 0, 0],
        [-s, 0, c, 0],
        [0, 0, 0, 1]
    ])


def rotation_z(angle):
    a = np.radians(angle)
    c, s = np.cos(a), np.sin(a)

    return np.array([
        [c, -s, 0, 0],
        [s, c, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])


def transform_points(points, matrix):
    homogeneous = np.column_stack(
        (points, np.ones(len(points)))
    )

    transformed = (matrix @ homogeneous.T).T
    return transformed[:, :3]
