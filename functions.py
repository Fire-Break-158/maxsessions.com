import docker
import paramiko

from datetime import (
    datetime, 
    timezone,
    timedelta
)
from time import sleep



### Docker Status Page ##############################################################################################################################################################################################

def getContainers():
    # setting up the required connection for the docker python library to get container info and send commands
    client = docker.from_env()
    #below method is only for the machine this is running on
    ##client = docker.from_env()
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



def restartContainer(Short_Id):
    client = docker.from_env()
    #below method is only for the machine this is running on for things like testing
    ##client = docker.from_env()
    container = client.containers.get(Short_Id)
    container.restart()

def stopContainer(Short_Id):
    client = docker.from_env()
    #below method is only for the machine this is running on for things like testing
    ##client = docker.from_env()
    container = client.containers.get(Short_Id)
    container.stop()

def startContainer(Short_Id):
    client = docker.from_env()
    #below method is only for the machine this is running on for things like testing
    ##client = docker.from_env()
    container = client.containers.get(Short_Id)
    container.start()

def pauseContainer(Short_Id):
    client = docker.from_env()
    #below method is only for the machine this is running on for things like testing
    ##client = docker.from_env()
    container = client.containers.get(Short_Id)
    container.pause()

def unpauseContainer(Short_Id):
    client = docker.from_env()
    #below method is only for the machine this is running on for things like testing
    ##client = docker.from_env()
    container = client.containers.get(Short_Id)
    container.unpause()

def removeContainer(Short_Id):
    client = docker.from_env()
    #below method is only for the machine this is running on for things like testing
    ##client = docker.from_env()
    container = client.containers.get(Short_Id)
    container.remove()





### Create Container Page ###################################################################################################################################################################################################

#def dockerRun