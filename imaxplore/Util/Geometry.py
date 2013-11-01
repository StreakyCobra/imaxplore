# -*- coding: utf-8 -*-

import numpy as np

# Check if a point lie into the triangle
def lieIntoTriangle(triangle, x, y):
    # Shortcut to access points
    x1, y1 = triangle[0]
    x2, y2 = triangle[1]
    x3, y3 = triangle[2]

    # Compute barycentric alpha
    alpha = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) /\
            ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))

    # If alpha smaller than 0 then outside the triangle
    if alpha <= 0:
        return False

    # Compute barycentric beta
    beta = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) /\
            ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))

    # If beta smaller than 0 then outside the triangle
    if beta <= 0:
        return False

    # Compute barycentric gamma
    gamma = 1.0 - alpha - beta

    # If gamma smaller than 0 then outside the triangle
    if gamma <= 0:
        return False

    # Else inside the triangle
    return True

# Check if a list of points are on the same side of a line formed by p1-p2
def allSameSide(p1, p2, points):
    # Verify array length
    if len(points) <= 1:
        return True

    # Transform to numpy vector
    np1 = point2DToVector(p1)
    np2 = point2DToVector(p2)
    plan = np2 - np1

    # Comparison point
    cp = None

    # Check all points
    for pt in points:
        # Transform to numpy vector
        npt = point2DToVector(pt)

        # Define comparison point if not existing
        if cp is None:
            cp = np.cross(plan, npt - np1)
            next

        # Compare point
        cp2 = np.cross(plan, npt - np2)

        if np.dot(cp, cp2) < 0:
            return False

    return True

# Transform a tuple to numpy vector
def point2DToVector(p):
    px, py = p
    return np.array([px, py])