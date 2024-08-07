import subprocess
import ast
import json
import argparse
from prometheus_client import start_http_server, Gauge
import time
import os
import sys

def printOldJSON():
    #Reading the JSON file and loading in a python dictionary "info".
    with open("oldJSON.json") as openJSON:
        info = json.load(openJSON)
        openJSON.close()

    #print("Info:" + str(info))

    #Info is the JSON, First number in [] is the container, Section between [], the 0 in [] for the value inside the list, [1:] custs the \
    print(info[1]["Names"][0][1:])

def printNewJSON():
    # #Opens and read the JSON file.
    # with open("Newendpoints.json") as openJSON:
    #     info = json.load(openJSON)
    #     openJSON.close()

    #Define the command to get the container configuration.
    getJSON = """ 
    API_KEY=your_API_KEY'
    curl -X GET --header 'Content-Type: application/json' --header "x-api-key: $API_KEY" --url 'https://portainer.delorenzo.mobi/api/endpoints' | jq
    """

    #Excecuting the command.
    JSONinfo = subprocess.run(getJSON, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    #Decoding the output from bytes to string.
    output = JSONinfo.stdout.decode("utf-8")
    
    #Loading the string into a dictionary (JSON Format).
    info = json.loads(output)

    #Declaring variables
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

    debugging = False

    def debug():
        #Debug view:
        #Prints the number of Endpoints.
        print("Number of Endpoints: " + str(len(results)) + "\n")

        #Gets and prints each Endpoint and Container.
        counter = 0
        while counter < len(results): #len(results) is the length of the results list.

            #Gets the names of each Endpoint with next(iter().
            EndptName = next(iter(results[counter]))

            #Prints Endpoint + number of containers.
            print("\tEndpoint " + str(counter + 1) + ": " + str(EndptName) + "\n")
            print("\tNumber of containers: " + str(len(results[counter][EndptName])))

            #Counts and prints each container Name and its State:
            countApps = 0
            while countApps < len(results[counter][EndptName]): #len(results[counter][EndptName]) is the number of containers.

                #Generates string.
                debudResult = (
                "\t\tName: " + str(results[counter][EndptName][countApps][0]) + "\n" + #Name.
                "\t\tState: " + str(results[counter][EndptName][countApps][1]) + "\n" #State.
                )

                print(debudResult)
                countApps+=1

            counter+=1

    endpoints = []
    endpoints = results

    #Gets and prints each Endpoint and Container.
    counter = 0
    while counter < len(endpoints): #len(results) is the length of the results list.

        #Gets the names of each Endpoint with next(iter().
        EndptName = next(iter(endpoints[counter]))

        #Counts and prints each container Name and its State:
        countApps = 0
        while countApps < len(endpoints[counter][EndptName]): #len(results[counter][EndptName]) is the number of containers.

            #Generates string.
            debudResult = (
            "\t\tName: " + str(endpoints[counter][EndptName][countApps][0]) + "\n" + #Name.
            "\t\tState: " + str(endpoints[counter][EndptName][countApps][1]) + "\n" #State.
            )

            ENDPOINTNAME = next(iter(endpoints[counter]))
            NAME = endpoints[counter][EndptName][countApps][0]
            STATE = endpoints[counter][EndptName][countApps][1]

            print(ENDPOINTNAME)
            print(NAME)
            print(STATE)

            

            #print(debudResult)
            countApps+=1

        counter+=1

    if debugging:
        debug()

printNewJSON()

number = 0
while True:
    print('\r' + str(number), end='')
    sys.stdout.flush()
    time.sleep(1)
    number+=1
