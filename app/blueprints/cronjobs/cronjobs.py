import docker
import datetime
import subprocess
import os

from pathlib import Path
from flask import (
    Blueprint, 
    render_template, 
    request
)
from datetime import datetime


cronjobs = Blueprint('cronjobs', __name__, template_folder='templates', static_folder='static')




@cronjobs.route('/cronjob-manager', methods = ['GET', 'POST'])
def cronjob_manager():

    cronjobs = subprocess.run(['crontab', '-l'], capture_output=True, text=True).stdout
    cronjobs = cronjobs.splitlines()
    # Store the crontab in a variable
    print(cronjobs)

    # most of our methods are post as we typically need to pass more than 1 variable and doing so over post is easier
    if request.method == 'GET':
        return render_template('cronjobs.html', cronjobs=cronjobs)
    
    if request.method == 'POST':
        data = request.form.to_dict()
        job_to_delete = data.get('cronjob')
        updated_cron_jobs = [job for job in cronjobs if job_to_delete not in job]

        # Write the updated crontab back to a temporary file
        with open('/tmp/mycron', 'w') as f:
            for job in updated_cron_jobs:
                f.write(job + '\n')

        # Install the updated crontab
        subprocess.run(['crontab', '/tmp/mycron'])

        # Clean up the temporary file
        subprocess.run(['rm', '/tmp/mycron'])

        print("Cron job deleted successfully.")
        return render_template('cronjobs.html', cronjobs=cronjobs)
