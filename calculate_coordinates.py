import scipy.integrate as sp
from numpy import cos, sin, radians, sqrt, linspace, round, cbrt, pi, append
from data.read_constants import transfer

DATA = transfer()


def calculate_without_air_resistance(speed=0, angle=0, planet='Марс', height=0, calc_step=0.1):
    x = [0]
    y = [height]
    g = DATA['planet'][planet]
    angle = radians(angle)
    v_x = cos(angle) * speed
    v_y = sin(angle) * speed
    tmax = (v_y + sqrt(v_y ** 2 + 2 * g * height)) / g
    points_amount = int(tmax // calc_step)
    t = linspace(0, points_amount * calc_step, points_amount)
    append(t, tmax)
    for i in t:
        x.append(v_x * i)
        y.append(height + v_y * i + (-g * i ** 2 / 2))
    # for i in range(len(t)):
    #     t[i] = round(t[i], decimals=6)
    #     x[i] = round(x[i], decimals=6)
    #     y[i] = round(y[i], decimals=6)
    return x, y, t


def calculate_with_air_resistance(speed=0, angle=0, planet='Марс', height=0, air_env='Воздух', substance='Земля',
                                  mass=0, calc_step=0.1):
    c_f = 0.47
    r = cbrt((3 * mass) / (4 * pi * material_density))
    k = (3 / 8) * (c_f * air_density) / (r * material_density)

    def dydt(u, t):
        return (u[1], -k * u[1] ** 2 - g)

    def dxdt(u, t):
        return (u[1], -k * u[1] ** 2)

    angle = radians(angle)
    v_y = speed * sin(angle)
    v_x = speed * cos(angle)
    startdy_dt = (height, v_y)
    startdx_dt = (0, v_x)
    t = 0
    t_m = []
    x_m = []
    y_m = []
    y = 1
    while y >= 0:
        x = sp.odeint(dxdt, startdx_dt, [0, t])[1][0]
        y = sp.odeint(dydt, startdy_dt, [0, t])[1][0]
        t_m.append(t)
        x_m.append(x)
        y_m.append(y)
        t += calc_step
    return x_m, y_m, t_m
