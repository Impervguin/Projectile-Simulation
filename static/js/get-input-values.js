function get_input_values() {
    var speed = document.getElementById("speed-form");
    var speed_units = document.getElementById("speed-units-form");
    var mass = document.getElementById("mass-form");
    var mass_units = document.getElementById("mass-units-form");
    var substance = document.getElementById("substance-form");
    var angle = document.getElementById("angle-form");
    var angle_units = document.getElementById("angle-units-form");
    var height = document.getElementById("height-form");
    var planet = document.getElementById("planet-form");
    var air_env = document.getElementById("air-form");
    var calc_step = document.getElementById("calc-step-form");
    var air_resistance = document.getElementById("air-resistance-on");
    var values = [speed, mass, angle, height, calc_step];
    for (const value of values){
        if (value.value == "") {
            alert("Заполните все поля");
            return 0;
        };
    };
    const data = {
        "speed": [speed.value, speed_units.value],
        "mass": [mass.value, mass_units.value],
        "angle": [angle.value, angle_units.value],
        "substance": substance.value,
        "height": height.value,
        "planet": planet.value,
        "air_env": air_env.value,
        "calc_step": calc_step.value,
        "resistance": air_resistance.checked,
    };
    return data;
}