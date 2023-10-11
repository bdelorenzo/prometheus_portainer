import subprocess
import ast
import json
import argparse
from prometheus_client import start_http_server, Gauge
import time
import os

def printOldJSON():
    #Reading the JSON file and loading in a python dictionary "info".
    with open("oldJSON.json") as openJSON:
        info = json.load(openJSON)
        openJSON.close()

    #print("Info:" + str(info))

    #Info is the JSON, First number in [] is the container, Section between [], the 0 in [] for the value inside the list, [1:] custs the \
    print(info[1]["Names"][0][1:])

def printNewJSON():
    #Opens and read the JSON file.
    with open("Newendpoints.json") as openJSON:
        info = json.load(openJSON)
        openJSON.close()

    #Declaring variables
    EndpointID = ""
    EndpointName = ""
    Container = ""
    ContainerState = ""

    #Declaring list of results.
    results = []

    #Iterates trhough each endpoint and container and adds to the results list.
    endpointNumber = 0
    containerNumber = 0
    while True:
        #Temporary list for container data.
        containerTemp = []
        try:
            #Gets endpoint name.
            EndpointName = info[endpointNumber]["Name"]

            while True:
                try:
                    #Gets each container Name and State and add them to the temporary list.
                    Container = info[endpointNumber]["Snapshots"][0]["DockerSnapshotRaw"]["Containers"][containerNumber]["Names"][0][1:]
                    ContainerState = info[endpointNumber]["Snapshots"][0]["DockerSnapshotRaw"]["Containers"][containerNumber]["State"]
                    containerTemp.append((Container, ContainerState))
                    containerNumber+=1
                except:
                    break
            
            #Adds data to the results list.
            results.append({EndpointName: containerTemp})

            #Update variables for the loop.
            endpointNumber+=1
            containerNumber = 0

        except:
            break

    print(results)
    #print(results[1]["Docker 02"])

printNewJSON()






























#########################################################################################################

# container_info = []
# #Count the number of containers.
# count = 0 #Indicates the number of containers.
# while True:
#     try:
#         container = info[count]
#         count+=1
#     except:
#         break

# containerNumber = 0
# while containerNumber < count:
#     #Adding information to a list.
#     container_info.append((info[containerNumber]["Names"][0][1:],
#     info[containerNumber]["State"]))

#     print("\n\tContainer: " + info[containerNumber]["Names"][0][1:] +
#     "\n\tState: " + info[containerNumber]["State"] + "\n")