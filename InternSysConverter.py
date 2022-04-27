def get_speed_in_metersps(typ, val):
    if typ == 'm/s':
        speed = val
    elif typ == 'km/h':
        speed = val * 1000 / 3600
    elif typ == 'ml/h':
        speed = val * 0.44704
    else:
        speed = val * 0.9144
    return speed


def get_mass_in_kilograms(typ, val):
    if typ == 'kg':
        mass = val
    elif typ == 'g':
        mass = val / 1000
    elif typ == 'pd':
        mass = val * 0.45
    else:
        mass = val * 1000
    return mass


def get_angle_in_degrees(typ, val):
    if typ == 'deg':
        angle = val
    elif typ == 'rad':
        angle = val * 57.3
    elif typ == 'min':
        angle = val / 60
    else:
        angle = val / 3600
    return angle