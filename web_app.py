import re
import sqlite3
from bottle import route, run, debug, template, request, static_file, error
from bike_geometry import FrameGeometry

# Helper class extracting the first element of each FormDict item into a new Dict
def extractFormDict(form_dict):
    new_dict = dict()
    for key in form_dict.keys():
        new_dict[key] = form_dict.get(key)
    return new_dict


def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


@route('/add_bike')
def add_bike():
    frame_geo = FrameGeometry()
    return template('generate_form', fields=frame_geo.as_dict().keys(),
                    geometry_type=frame_geo.TYPE)


@route('/add_bike', method='POST')
def save_bike():
    print("Form dict:")
    print(request.forms.items())
    print(request.forms.dict)

    geometry_type = request.forms.dict.pop('type', None)[0]
    output_str = '<p>{}:</p>'.format(' '.join(camel_case_split(geometry_type)))
    for key in request.forms.keys():
        output_str += '<p>    {} = {}</p>'.format(key.replace('_',' ').capitalize(), request.forms.get(key))
    print(output_str)
    return output_str


debug(True)
run()
