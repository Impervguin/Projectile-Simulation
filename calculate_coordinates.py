import scipy.integrate as sp
from numpy import cos, sin, radians, sqrt, linspace, round, cbrt, pi


def calculate_without_air_resistance(start_speed=0, angle=0, g=0, start_height=0):
    x = [0]
    y = [start_height]
    points_amount = int(start_speed) if start_speed >= 100 else 100
    angle = radians(angle)
    v_x = cos(angle) * start_speed
    v_y = sin(angle) * start_speed
    tmax = (v_y + sqrt(v_y ** 2 + 2 * g * start_height)) / g
    t = linspace(0, tmax, points_amount)
    for i in t:
        x.append(v_x * i)
        y.append(start_height + v_y * i + (-g * i ** 2 / 2))
    for i in range(len(t)):
        t[i] = round(t[i], decimals=6)
        x[i] = round(x[i], decimals=6)
        y[i] = round(y[i], decimals=6)
    return x, y, t


def calculate_with_air_resistance(start_speed=0, angle=0, g=0, start_height=0, air_density=0, material_density=0,
                                  mass=0):
    c_f = 0.47
    r = cbrt((3 * mass) / (4 * pi * material_density))
    k = (3 / 8) * (c_f * air_density) / (r * material_density)

    def dydt(u, t):
        return (u[1], -k * u[1] ** 2 - g)

    def dxdt(u, t):
        return (u[1], -k * u[1] ** 2)

    points_amount = int(start_speed * 5) if start_speed >= 20 else 100
    angle = radians(angle)
    v_y = start_speed * sin(angle)
    v_x = start_speed * cos(angle)
    startdy_dt = (start_height, v_y)
    startdx_dt = (0, v_x)
    tmax = (v_y + sqrt(v_y ** 2 + 2 * g * start_height)) / g
    t = linspace(0, tmax, points_amount)
    y = sp.odeint(dydt, startdy_dt, t)
    x = sp.odeint(dxdt, startdx_dt, t)
    y = y[:, 0]
    x = x[:, 0]
    for t0 in range(len(y)):
        if y[t0] < 0:
            y = y[:t0 + 1]
            x = x[:t0 + 1]
            t = t[:t0 + 1]
            y[t0] = 0
            break
        else:
            y[t0] = round(y[t0], decimals=6)
            x[t0] = round(x[t0], decimals=6)
            t[t0] = round(t[t0], decimals=6)
    return x, y, t
