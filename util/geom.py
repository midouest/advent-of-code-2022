Vec2D = tuple[int, int]
Vec3D = tuple[int, int, int]


def rotate_2d(v: Vec2D, z: int) -> Vec2D:
    x, y = v
    if z > 0:
        return (-y, x)
    elif z < 0:
        return (y, -x)
    return v


def absolute_2d(v: Vec2D) -> Vec2D:
    x, y = v
    return abs(x), abs(y)


def invert_2d(v: Vec2D) -> Vec2D:
    x, y = v
    return (-x, -y)


def irange_2d(start: Vec2D, stop: Vec2D, step: Vec2D):
    x, y = start
    dx, dy = step
    xn, yn = stop
    if (
        dx == 0
        and x != xn
        or dy == 0
        and y != yn
        or dx > 0
        and x > xn
        or dx < 0
        and x < xn
        or dy > 0
        and y > yn
        or dy < 0
        and y < yn
    ):
        raise ValueError("irange_2d start, stop and step must terminate")
    while (dx >= 0 and x <= xn or dx < 0 and x >= xn) and (
        dy >= 0 and y <= yn or dy < 0 and y >= yn
    ):
        yield x, y
        x += dx
        y += dy


def add_2d(a: Vec2D, b: Vec2D) -> Vec2D:
    ax, ay = a
    bx, by = b
    return (ax + bx, ay + by)


def test_rotate_2d_cw():
    assert rotate_2d((1, 0), 1) == (0, 1)
    assert rotate_2d((0, 1), 1) == (-1, 0)
    assert rotate_2d((-1, 0), 1) == (0, -1)
    assert rotate_2d((0, -1), 1) == (1, 0)


def test_rotate_2d_ccw():
    assert rotate_2d((1, 0), -1) == (0, -1)
    assert rotate_2d((0, -1), -1) == (-1, 0)
    assert rotate_2d((-1, 0), -1) == (0, 1)
    assert rotate_2d((0, 1), -1) == (1, 0)


def absolute_3d(v: Vec3D) -> Vec3D:
    x, y, z = v
    return (abs(x), abs(y), abs(z))


def invert_3d(v: Vec3D) -> Vec3D:
    x, y, z = v
    return (-x, -y, -z)


def rotate_3d(v: Vec3D, r: Vec2D) -> Vec3D:
    x, y, z = v
    rx, ry, rz = r
    if rx > 0:
        return (x, -z, y)
    elif rx < 0:
        return (x, z, -y)
    elif ry > 0:
        return (-z, y, x)
    elif ry < 0:
        return (z, y, -x)
    elif rz > 0:
        return (-y, x, z)
    elif rz < 0:
        return (y, -x, z)
    return v


def test_rotate_3d_cw_x():
    assert rotate_3d((1, 1, 0), (1, 0, 0)) == (1, 0, 1)
    assert rotate_3d((1, 0, 1), (1, 0, 0)) == (1, -1, 0)
    assert rotate_3d((1, -1, 0), (1, 0, 0)) == (1, 0, -1)
    assert rotate_3d((1, 0, -1), (1, 0, 0)) == (1, 1, 0)


def test_rotate_3d_ccw_x():
    assert rotate_3d((1, 1, 0), (-1, 0, 0)) == (1, 0, -1)
    assert rotate_3d((1, 0, -1), (-1, 0, 0)) == (1, -1, 0)
    assert rotate_3d((1, -1, 0), (-1, 0, 0)) == (1, 0, 1)
    assert rotate_3d((1, 0, 1), (-1, 0, 0)) == (1, 1, 0)


def test_rotate_3d_cw_y():
    assert rotate_3d((1, 1, 0), (0, 1, 0)) == (0, 1, 1)
    assert rotate_3d((0, 1, 1), (0, 1, 0)) == (-1, 1, 0)
    assert rotate_3d((-1, 1, 0), (0, 1, 0)) == (0, 1, -1)
    assert rotate_3d((0, 1, -1), (0, 1, 0)) == (1, 1, 0)


def test_rotate_3d_ccw_y():
    assert rotate_3d((1, 1, 0), (0, -1, 0)) == (0, 1, -1)
    assert rotate_3d((0, 1, -1), (0, -1, 0)) == (-1, 1, 0)
    assert rotate_3d((-1, 1, 0), (0, -1, 0)) == (0, 1, 1)
    assert rotate_3d((0, 1, 1), (0, -1, 0)) == (1, 1, 0)


def test_rotate_3d_cw_z():
    assert rotate_3d((1, 0, 1), (0, 0, 1)) == (0, 1, 1)
    assert rotate_3d((0, 1, 1), (0, 0, 1)) == (-1, 0, 1)
    assert rotate_3d((-1, 0, 1), (0, 0, 1)) == (0, -1, 1)
    assert rotate_3d((0, -1, 1), (0, 0, 1)) == (1, 0, 1)


def test_rotate_3d_ccw_z():
    assert rotate_3d((1, 0, 1), (0, 0, -1)) == (0, -1, 1)
    assert rotate_3d((0, -1, 1), (0, 0, -1)) == (-1, 0, 1)
    assert rotate_3d((-1, 0, 1), (0, 0, -1)) == (0, 1, 1)
    assert rotate_3d((0, 1, 1), (0, 0, -1)) == (1, 0, 1)
