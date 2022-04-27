def get_speed_in_metersps(val):
    val = val.split(',')
    val, typ = float(val[0]), val[1]
    if typ == 'м/с':
        speed = val
    elif typ == 'км/ч':
        speed = val * 1000 / 3600
    elif typ == 'мил/ч':
        speed = val * 0.44704
    else:
        speed = val * 0.9144
    return speed


def get_mass_in_kilograms(val):
    val = val.split(',')
    val, typ = float(val[0]), val[1]
    if typ == 'кг':
        mass = val
    elif typ == 'г':
        mass = val / 1000
    elif typ == 'фунт':
        mass = val * 0.45
    else:
        mass = val * 1000
    return mass


def get_angle_in_degrees(val):
    val = val.split(',')
    val, typ = float(val[0]), val[1]
    if typ == 'град':
        angle = val
    elif typ == 'рад':
        angle = val * 57.3
    elif typ == 'мин':
        angle = val / 60
    else:
        angle = val / 3600
    return angle