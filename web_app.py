import sqlite3
from bottle import route, run, debug, template, request, static_file, error
from bike_geometry import BikeGeometry

@route('/add_bike')
def add_bike():
    bg = BikeGeometry()
    return template('generate_form', fields=bg.as_dict().keys())

@route('/add_bike', method='POST')
def save_bike():
    print("Form dict:")
    print(request.forms.items())
    print(request.forms.decode().items())
    print("Json data:")
    print(request.json)
    bike_name = request.forms.get('bike_name')
    bike_size = request.forms.get('bike_size')
    wheel_size = request.forms.get('wheel_size')
    output_str = 'bike name = {}, bike size = {}, wheel size = {}'.format(bike_name,
                                                                          bike_size,
                                                                          wheel_size)
    print(output_str)
    return "<p>%s</p>" % output_str

debug(True)
run()