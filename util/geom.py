Vec2d = tuple[int, int]
Vec3d = tuple[int, int, int]


def rotate_2d(v: Vec2d, z: int) -> Vec2d:
    x, y = v
    if z > 0:
        return (-y, x)
    elif z < 0:
        return (y, -x)
    return v


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


def absolute_3d(v: Vec3d) -> Vec3d:
    x, y, z = v
    return (abs(x), abs(y), abs(z))


def invert_3d(v: Vec3d) -> Vec3d:
    x, y, z = v
    return (-x, -y, -z)


def rotate_3d(v: Vec3d, r: Vec2d) -> Vec3d:
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
