
import numpy as np


def orthographic_projection(points, width, height, scale=90):
    projected = []

    for x, y, z in points:
        sx = width // 2 + x * scale
        sy = height // 2 - y * scale
        projected.append((int(sx), int(sy)))

    return projected


def perspective_projection(
    points, width, height, focal_length=500, camera_distance=6
):
    projected = []

    for x, y, z in points:
        depth = z + camera_distance

        if depth <= 0.1:
            projected.append(None)
            continue

        sx = width / 2 + (x * focal_length / depth)
        sy = height / 2 - (y * focal_length / depth)

        projected.append((int(sx), int(sy)))

    return projected
