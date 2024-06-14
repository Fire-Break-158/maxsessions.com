from flask import (
    Blueprint, 
    render_template, 
    send_from_directory
)
from datetime import datetime


familyphotos = Blueprint('familyphotos', __name__, template_folder='templates', static_folder='static')


@familyphotos.route('/Home')
def Home():
    return render_template('family_index.html')


@familyphotos.route('/January06')
def January06():
    return render_template('January06.html')


@familyphotos.route('/March06')
def March06():
    return render_template('March06.html')


@familyphotos.route('/AprilMay06')
def AprilMay06():
    return render_template('AprilMay06.html')


@familyphotos.route('/JuneJuly06')
def JuneJuly06():
    return render_template('JuneJuly06.html')


@familyphotos.route('/August06')
def August06():
    return render_template('August06.html')


@familyphotos.route('/December05')
def December05():
    return render_template('December05.html')


@familyphotos.route('/October02')
def October02():
    return render_template('October02.html')