# Imports
import json
import subprocess
import datetime
import docker
import traceback
import sys

from flask import (
    Flask, 
    g, 
    render_template, 
    request, 
    url_for, 
    redirect, 
    render_template_string, 
    send_file, 
    make_response, 
    jsonify, 
    session,
    Response
)
from time import sleep
from werkzeug.exceptions import NotFound

# internal libraries below
from functions import *





##
## Setup and Housekeeping
##
app = Flask(__name__, template_folder='templates')





@app.template_filter('json_pretty')
def json_pretty_filter(value):
    if isinstance(value, str):
        value = json.loads(value)    
    return json.dumps(value, indent=4)





@app.template_filter('asint')
def asint(value):
    return int(value)





@app.errorhandler(Exception)
def handle_error(e):
    # Check if the error is a 404 and retrieve the original URL
    original_url = None
    if isinstance(e, NotFound):
        original_url = request.url

    # This error handler will handle exceptions not caught by a try/except block
    rootUrl=request.url_root
    previousUrl = request.referrer if request.referrer else request.url_root

    # Modify the message to include the original_url for 404 errors
    if original_url:
        message = f"Could not find the requested page: {original_url}. Please try again by going <a href='{previousUrl}'>back</a> to the previous page or return to the <a href='{rootUrl}'>Backoffice Home</a>"
    else:
        message = f"Please try again by going <a href='{previousUrl}'>back</a> to the previous page or return to the <a href='{rootUrl}'>Backoffice Home</a>"

    trace = traceback.format_exc()
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_details = traceback.format_exception(exc_type, exc_value, exc_traceback)
    formatted_traceback = ''.join(traceback_details)
    debugInfo = f'''
    <b>Debugging Information Below:</b><br>
    <pre>
    {formatted_traceback}
    </pre>
    '''
    print(str(e) + "\n" + str(message) + "\n" + str(debugInfo))
    return render_template('response.html', responseType='Error', data=str(e), data2=message, data3=debugInfo, sideMenu=False)





##
## Setup complete, Routes below
##
@app.route('/')
def htmlroot():
    return render_template('index.html')





@app.route('/dockerstatus', methods = ['GET', 'POST'])
def dockerStatus():


    # set up clients for getting containers and sending commands
    containers = getContainers()


    # most of our methods are post as we typically need to pass more than 1 variable and doing so over post is easier
    if request.method == 'GET':

        return render_template('technology/docker_containers.html', containers=containers)
    elif request.method == 'POST':
        # all of the info hidden in the button is put into a dictionary for us to use 
        data = request.form.to_dict()
        # we check what the value for the button was set to which changes based on the page and button and reac accordingly
        if data['submit'] == 'Container Selected':
            # we put 2 values we need as variables so we can use them in the 'getContainerInfo' function as the needed inputs
            Short_Id = data['Short_Id']
            containerInfo = getContainerInfo(Short_Id)
            return render_template('technology/container_info.html', container=containerInfo)
        elif data['submit'] == 'Restart':
            Short_Id = data['Short_Id']
            # if one of the command buttons was pressed for a single container we use the variables just set to
            # accurately give the command to the right computer and the right container on it
            restartContainer(Short_Id)
            # we fetch the container into again after running the command to ensure we refresh its status
            containerInfo = getContainerInfo(Short_Id)           
            return render_template('technology/container_info.html', container=containerInfo)
        elif data['submit'] == 'Stop':
            Short_Id = data['Short_Id']
            stopContainer(Short_Id)
            containerInfo = getContainerInfo(Short_Id)            
            return render_template('technology/container_info.html', container=containerInfo)
        elif data['submit'] == 'Start':
            Short_Id = data['Short_Id']
            startContainer(Short_Id)
            containerInfo = getContainerInfo(Short_Id)
            return render_template('technology/container_info.html', container=containerInfo)
        elif data['submit'] == 'Pause':
            Short_Id = data['Short_Id']
            pauseContainer(Short_Id)
            containerInfo = getContainerInfo(Short_Id)
            return render_template('technology/container_info.html', container=containerInfo)
        elif data['submit'] == 'Unpause':
            Short_Id = data['Short_Id']
            unpauseContainer(Short_Id)
            containerInfo = getContainerInfo(Short_Id)
            return render_template('technology/container_info.html', container=containerInfo)
        elif data['submit'] == 'Remove':
            Short_Id = data['Short_Id']
            stopContainer(Short_Id)
            removeContainer(Short_Id)
            containers = getContainers()
            return render_template('technology/docker_containers.html', containers=containers)
    


@app.route('/containercreator', methods = ['GET', 'POST'])
def containerCreator():
    if request.method == 'GET':
        return render_template('technology/container_creator.html')
    if request.method == 'POST':
        data = request.form.to_dict()
#        if data['submit'] == 'Execute':
#            if 'command' not in request.form:
#                return "No command provided", 400
#
#
#            command = request.form['command']
#
#
#            try:
#                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
#                output = result.decode('utf-8')
#            except subprocess.CalledProcessError as e:
#                output = e.output.decode('utf-8')
#            return render_template('technology/container_creator.html', output=output)
        if data['submit'] == 'Docker Run':
            name = ''
            pull = ''
            tag = ''
            latest = ''
            v1 = ''
            v12 = ''
            v2 = ''
            v22 = ''
            v3 = ''
            v32 = ''
            v4 = ''
            v42 = ''
            d = ''
            it = ''
            rm = ''
            restart = ''
            currentTime = datetime.now()
            formattedTime = currentTime.strftime("%Y-%m-%d-%H-%M-%S")
            CMDBackup = f'CMD{formattedTime}'
            CMDcont = 'docker run '


            if 'image' in data and data['image'] and 'containerlocation' in data and data['containerlocation']:
                image = ' ' + data['image']
                pull = '--pull always'
                CMDcont += pull
                containerLocation = data['containerlocation']
                if '--name' in data and data['--name']:
                    name = ' --name "' + data['--name'] + '" '
                    CMDcont += name
                if '-v1' in data and data['-v1']:
                    v1 = ' -v ' + data['-v1']
                    CMDcont += v1
                if '-v12' in data and data['-v12']:
                    v12 = ':' + data['-v12'] + ' '
                    CMDcont += v12
                if '-v2' in data and data['-v2']:
                    v2 = '-v ' + data['-v2']
                    CMDcont += v2
                if '-v22' in data and data['-v22']:
                    v22 = ':' + data['-v22'] + ' '
                    CMDcont += v22
                if '-v3' in data and data['-v3']:
                    v3 = '-v ' + data['-v3']
                    CMDcont += v3
                if '-v32' in data and data['-v32']:
                    v32 = ':' + data['-v32'] + ' '
                    CMDcont += v32
                if '-v4' in data and data['-v4']:
                    v4 = '-v ' + data['-v4']
                    CMDcont += v4
                if '-v42' in data and data['-v42']:
                    v42 = ':' + data['-v42'] + ' '
                    CMDcont += v42
                if '-d' in data and data['-d']:
                    d = ' -d'
                    CMDcont += d
                if '-it' in data and data['-it']:
                    it = ' -it'
                    CMDcont += it
                if 'exitoption' in data and data['exitoption'] and data['exitoption'] == '--rm':
                    rm = ' --rm'
                    CMDcont += rm
                if 'exitoption' in data and data['exitoption'] and data['exitoption'] == '--restart':
                    restart = ' --restart'
                    CMDcont += restart
                CMDcont += image
                if 'tag' in data and data['tag']:
                    tag = ':' + data['tag']
                    CMDcont += tag
                if 'latest' in data and data['latest']:
                    latest = ':latest'
                    CMDcont += latest


                if 'CMDoption' in data and data['CMDoption'] and  data['CMDoption'] == 'save':
                    saveCom = f"cd {containerLocation} && echo {CMDcont} > CMD"
                    subprocess.run([saveCom], shell=True)
                    subprocess.run([CMDcont], shell=True)
                elif 'CMDoption' in data and data['CMDoption'] and  data['CMDoption'] == 'backup':
                    overwriteCom = f'cd {containerLocation} && mv CMD {CMDBackup} && echo {CMDcont} > f"CMD"'
                    subprocess.run([overwriteCom], shell=True)
                    subprocess.run([CMDcont], shell=True)

                
            else:
                responseType = 'Missing Info'
                return render_template('response.html', responseType = responseType)

            
            return render_template('technology/container_creator.html')





##
## System Tools
##
@app.route('/system')
def systemroot():
    userInfo = getOidcUserInfo(oidc)
    return render_template('system/system_index.html', userInfo=userInfo)


@app.route('/debuginfo')
def debuginfo():
    userInfo = getOidcUserInfo(oidc)
    permissions = getUserPermissions(oidc)    
    return render_template('system/debug.html', userInfo=userInfo, permissions=permissions)  


@app.route('/logout')
def logout():
    if oidc.user_loggedin:
        info = oidc.user_getinfo(['preferred_username', 'email', 'sub'])
        user_id = info.get('sub')
        if user_id in oidc.credentials_store:
            access_token = OAuth2Credentials.from_json(oidc.credentials_store[user_id]).access_token
            headers = {'Authorization': 'Bearer %s' % (access_token)}
            rawinfo = requests.post('https://keycloak.pacificbattleship.com/auth/realms/nmsn/protocol/openid-connect/revoke', headers=headers).text
            rawinfo = requests.post('https://keycloak.pacificbattleship.com/auth/realms/nmsn/protocol/openid-connect/logout', headers=headers).text
    #Performs local logout by removing the session cookie.
    oidc.logout()
    sleep(5)
    return redirect(url_for('htmlroot'))





# Main
def main():
    app.run(host='0.0.0.0', port=8000, debug=True)





if __name__ == "__main__":
    main()
