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


dockertools = Blueprint('dockertools', __name__, template_folder='templates', static_folder='static')


@dockertools.route('/')
def index():
    return render_template('docker_index.html')





@dockertools.route('/docker-container-manager', methods = ['GET', 'POST'])
def dockerStatus():


    # set up clients for getting containers and sending commands
    def getContainers():
        # setting up the required connection for the docker python library to get container info and send commands
        client = docker.from_env()
        containers = client.containers.list(all=True)

        containerList = []
        # iterating through each container we pulled and get some basic issue and keep the 'clientMethod' so we can use it
        # later for getting more info once a container is selected and for sending commands to a specific container
        for container in containers:
            containerInfo = {}
            containerInfo["Name"] = container.name
            containerInfo["Image"] = container.image
            containerInfo["Status"] = container.status
            containerInfo["Short_Id"] = container.short_id
            # add everything into the list of dicts
            containerList.append(containerInfo)
        return(containerList)

    containers = getContainers()


    def getContainerInfo(Short_Id):
        client = docker.from_env()
        # below method is only for the machine this is running on
        ##client = docker.from_env()
        # we now look up the specific container info based on the 'Short_Id' we passed earlier via POST
        container = client.containers.get(Short_Id)

        containerList = []
        containerInfo = {}
        containerInfo["Name"] = container.name
        containerInfo["Status"] = container.status
        containerInfo["Short_Id"] = container.short_id
        containerInfo["PreImage"] = container.image
        # container.image gives ugly text/info so we convert it to a str and clean it up for display
        PreImage = str(containerInfo['PreImage'])
        containerInfo["Image"] = PreImage.split("'")[1]
        # if we just printed container.logs it just prints the file name so we use this to print the contents of the file
        # and we ensure its the correct container log by specifying the Short_Id
        logs = client.containers.get(containerInfo["Short_Id"]).logs().decode('utf-8')
        containerInfo['Logs'] = logs
        # add everything into the list of dicts so
        containerList.append(containerInfo)
        return(containerList)


    # most of our methods are post as we typically need to pass more than 1 variable and doing so over post is easier
    if request.method == 'GET':

        return render_template('docker_containers.html', containers=containers)
    elif request.method == 'POST':
        # all of the info hidden in the button is put into a dictionary for us to use 
        data = request.form.to_dict()
        # we check what the value for the button was set to which changes based on the page and button and reac accordingly
        if data['submit'] == 'Container Selected':
            # we put 2 values we need as variables so we can use them in the 'getContainerInfo' function as the needed inputs
            Short_Id = data['Short_Id']
            containerInfo = getContainerInfo(Short_Id)
            return render_template('container_info.html', container=containerInfo)
        elif data['submit'] == 'Restart':
            Short_Id = data['Short_Id']
            client = docker.from_env()
            container = client.containers.get(Short_Id)
            container.restart()        
            # we fetch the container into again after running the command to ensure we refresh its status   
            containerInfo = getContainerInfo(Short_Id)
            return render_template('container_info.html', container=containerInfo)
        elif data['submit'] == 'Stop':
            Short_Id = data['Short_Id']
            client = docker.from_env()
            container = client.containers.get(Short_Id)
            container.stop()
            # we fetch the container into again after running the command to ensure we refresh its status
            containerInfo = getContainerInfo(Short_Id)            
            return render_template('container_info.html', container=containerInfo)
        elif data['submit'] == 'Start':
            Short_Id = data['Short_Id']
            client = docker.from_env()
            container = client.containers.get(Short_Id)
            container.start()
            # we fetch the container into again after running the command to ensure we refresh its status
            containerInfo = getContainerInfo(Short_Id)
            return render_template('container_info.html', container=containerInfo)
        elif data['submit'] == 'Pause':
            Short_Id = data['Short_Id']
            client = docker.from_env()
            container = client.containers.get(Short_Id)
            container.pause()
            # we fetch the container into again after running the command to ensure we refresh its status
            containerInfo = getContainerInfo(Short_Id)
            return render_template('container_info.html', container=containerInfo)
        elif data['submit'] == 'Unpause':
            Short_Id = data['Short_Id']
            client = docker.from_env()
            container = client.containers.get(Short_Id)
            container.unpause()
            containerInfo = getContainerInfo(Short_Id)
            return render_template('container_info.html', container=containerInfo)
        elif data['submit'] == 'Remove':
            Short_Id = data['Short_Id']
            client = docker.from_env()
            container = client.containers.get(Short_Id)
            container.stop()
            container.remove()
            containers = getContainers()
            return render_template('docker_containers.html', containers=containers)
        else:
            containers = getContainers()
            return render_template('docker_containers.html', containers=containers)





@dockertools.route('/docker-container-creator', methods = ['GET', 'POST'])
def containerCreator():
    if request.method == 'GET':
        path=os.getenv('BASEDIR')
        def list_directories(path):
            try:
                directories = [item.name for item in Path(path).iterdir() if item.is_dir()]
                return directories
            except Exception as e:
                print(f"An error occurred: {e}")
                return []
        directories = list_directories(path)
        return render_template('docker_cmd.html', directories=directories, path=path)
    if request.method == 'POST':
        data = request.form.to_dict()

        if data['submit'] == 'Directory Selected':
            if 'uniqueLocation' in data and data['uniqueLocation']:
                uniqueLocation = data['uniquelocation']
                print(uniqueLocation)
                containerLoc = uniqueLocation
            else:
                containerLoc = data['path'] + '/' + data['containerLocation']
            print(containerLoc)
            CMDLoc = containerLoc + '/CMD'
            print(CMDLoc)
            try:
                with open(CMDLoc, 'r') as file:
                    CMDCont = file.read()
                return render_template('container_creator.html', containerLoc=containerLoc, CMDCont=CMDCont)
            except FileNotFoundError:
                return render_template('container_creator.html', containerLoc=containerLoc)

        

        elif data['submit'] == 'Run Existing CMD':
            CMDCont = data['CMDCont']
            subprocess.run([CMDCont], shell=True)
            return render_template('docker_cmd.html')


        elif data['submit'] == 'Docker Run':
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
            CMDCont = 'docker run '


            if 'image' in data and data['image'] and 'containerLoc' in data and data['containerLoc']:
                image = ' ' + data['image']
                pull = '--pull always'
                CMDCont += pull
                containerLoc = data['containerLoc']
                if '--name' in data and data['--name']:
                    name = ' --name "' + data['--name'] + '"'
                    CMDCont += name
                if '-v1' in data and data['-v1']:
                    v1 = ' -v ' + data['-v1']
                    CMDCont += v1
                if '-v12' in data and data['-v12']:
                    v12 = ':' + data['-v12'] + ' '
                    CMDCont += v12
                if '-v2' in data and data['-v2']:
                    v2 = '-v ' + data['-v2']
                    CMDCont += v2
                if '-v22' in data and data['-v22']:
                    v22 = ':' + data['-v22'] + ' '
                    CMDCont += v22
                if '-v3' in data and data['-v3']:
                    v3 = '-v ' + data['-v3']
                    CMDCont += v3
                if '-v32' in data and data['-v32']:
                    v32 = ':' + data['-v32'] + ' '
                    CMDCont += v32
                if '-v4' in data and data['-v4']:
                    v4 = '-v ' + data['-v4']
                    CMDCont += v4
                if '-v42' in data and data['-v42']:
                    v42 = ':' + data['-v42'] + ' '
                    CMDCont += v42
                if '-p1' in data and data['-p1']:
                    p1 = ' -p ' + data['-p1']
                    CMDCont += p1
                if '-p12' in data and data['-p12']:
                    p12 = ':' + data['-p12'] + ' '
                    CMDCont += p12
                if '-p2' in data and data['-p2']:
                    p2 = '-p ' + data['-p2']
                    CMDCont += p2
                if '-p22' in data and data['-p22']:
                    p22 = ':' + data['-p22'] + ' '
                    CMDCont += p22
                if '-p3' in data and data['-p3']:
                    p3 = '-p ' + data['-p3']
                    CMDCont += p3
                if '-p32' in data and data['-p32']:
                    p32 = ':' + data['-p32'] + ' '
                    CMDCont += p32
                if '-p4' in data and data['-p4']:
                    p4 = '-p ' + data['-p4']
                    CMDCont += p4
                if '-p42' in data and data['-p42']:
                    p42 = ':' + data['-p42'] + ' '
                    CMDCont += p42
                if '-d' in data and data['-d']:
                    d = ' -d'
                    CMDCont += d
                if '-it' in data and data['-it']:
                    it = ' -it'
                    CMDCont += it
                if 'exitoption' in data and data['exitoption'] and data['exitoption'] == '--rm':
                    rm = ' --rm'
                    CMDCont += rm
                if 'exitoption' in data and data['exitoption'] and data['exitoption'] == '--restart':
                    restart = ' --restart'
                    CMDCont += restart
                CMDCont += image
                if 'tag' in data and data['tag']:
                    tag = ':' + data['tag']
                    CMDCont += tag
                if 'latest' in data and data['latest']:
                    latest = ':latest'
                    CMDCont += latest
                
                
                CMDCont = CMDCont.strip()


                if 'CMDoption' in data and data['CMDoption'] and  data['CMDoption'] == 'dontsave':
                    subprocess.run([CMDCont], shell=True)
                    return render_template('docker_cmd.html')
                if 'CMDoption' in data and data['CMDoption'] and  data['CMDoption'] == 'save':
                    CMDLoc = containerLoc + '/CMD'
                    with open(CMDLoc, 'w') as file:
                        file.write(CMDCont)
                    subprocess.run([CMDCont], shell=True)
                    return render_template('docker_cmd.html')
                elif 'CMDoption' in data and data['CMDoption'] and  data['CMDoption'] == 'backup':
                    renameCom = f'cd {containerLoc} && mv CMD {CMDBackup}'
                    CMDLoc = containerLoc + '/CMD'
                    with open(CMDLoc, 'w') as file:
                        file.write(CMDCont)
                    subprocess.run([renameCom], shell=True)
                    subprocess.run([CMDCont], shell=True)
                    return render_template('docker_cmd.html')

                
            else:
                responseType = 'Missing Info'
                return render_template('response.html', responseType = responseType)