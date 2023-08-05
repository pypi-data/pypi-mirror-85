from flask import render_template, Blueprint

from raspcuterie.devices.input.am2302 import AM2302
from raspcuterie.devices import OutputDevice, InputDevice

bp = Blueprint("dashboard", __name__, template_folder="./templates")


@bp.route("/")
def dashboard():

    refrigerator = OutputDevice.registry["refrigerator"]
    heater = OutputDevice.registry["heater"]
    dehumidifier = OutputDevice.registry["dehumidifier"]
    humidifier = OutputDevice.registry["humidifier"]

    am2302: AM2302 = InputDevice.registry["temperature"]

    humidity, temperature = am2302.read_from_database()

    temperature_data = am2302.temperature_data()
    humidity_data = am2302.humidity_data()

    x = list(dict(temperature_data).values())
    if x:
        temperature_min = min(x)
        temperature_max = max(x)
    else:
        temperature_min = 0
        temperature_max = 0

    y = list(dict(humidity_data).values())
    if y:
        humidity_min = min(y)
        humidity_max = max(y)
    else:
        humidity_min = 0
        humidity_max = 0

    return render_template(
        "dashboard.html",
        refrigerator=refrigerator.value(),
        heater=heater.value(),
        dehumidifier=dehumidifier.value(),
        humidifier=humidifier.value(),
        humidifier_data=humidifier.chart(),
        dehumidifier_data=dehumidifier.chart(),
        refrigerator_data=refrigerator.chart(),
        heater_data=heater.chart(),
        humidity=humidity,
        temperature=temperature,
        temperature_min=temperature_min,
        temperature_max=temperature_max,
        temperature_data=temperature_data,
        humidity_data=humidity_data,
        humidity_min=humidity_min,
        humidity_max=humidity_max,
    )
