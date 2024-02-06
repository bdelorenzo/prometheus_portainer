import subprocess
import ast
import json
import argparse
from prometheus_client import start_http_server, Gauge
import time
import os

#Creating the Gauge.
container_state = Gauge("container_state", "State of the container", ["container_name", "endpoint_name"])

#Create parser.
parser = argparse.ArgumentParser(description = "Portainer Prometheus Script.")
#Define argumetns.
parser.add_argument("-apik", "--apikey", type=str, help="Indicates which Portainer API Key (mandatory)")
parser.add_argument("-url", type=str, help="Indicates which Portainer URL (mandatory)")
parser.add_argument("-debug", "--debugging", action='store_true', help="Shows containers. Note: This option consumes memory over time and could make the application crash after some time. Better for testing only. (optional)")
#Parse the rguments.
args = parser.parse_args()

#Requests containers from Portainer.
def getAndFindData(APIK, URL):
    apiKey = APIK
    url = URL

    container_info = []

    try:
        #Define the command to get the container configuration.
        getJSON = ("API_KEY=" + apiKey + 
        "\ncurl -X GET --header 'Content-Type: application/json' --header \"x-api-key: $API_KEY\" --url '" + 
        url + "' | jq")

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

        if(args.debugging):
            #Debug view:
            #Prints the number of Endpoints.
            print("Number of Endpoints: " + str(len(results)) + "\n")

            #Gets and prints each Endpoint and Container.
            counter = 0
            while counter < len(results): #len(results) is the length of the results list.

                #Gets the names of each Endpoint with next(iter()).
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
        
        return results #Returns endpoints list.

    except:
        #Print error message.
        print("\n! Error while retreiving data, possible errors:" +
        "\n - No internet connection." +
        "\n - Invalid API key or URL." +
        "\nPlease make sure to use the parameters, run this script followed by \"--help\" for more information.\n")
        return results #Returns empty endpoints list.

#Update the gauge with the provided values.
def update_metrics(endpoint_name, container_name, state):
    #print("FROM UPDATE METRICS METHOD: " + endpoint_name + " " + container_name + " " + state)
    container_state.labels(container_name=container_name, endpoint_name=endpoint_name).set(1 if state == 'running' else 0)

#Starts HTTP server.
if __name__ == "__main__":
    start_http_server(8000)
    seconds = 1

    try:
        while True:
            #Gets list of endpoints.
            endpoints = getAndFindData(args.apikey, args.url)

            #Validate if the list came empty.
            if not endpoints:
                exit(0)
            else: #Proceeds if list is not empty.

                #Gets each Endpoint and Container.
                counter = 0
                while counter < len(endpoints): #len(endpoints) is the length of the endpoints list.

                    #Gets the names of each Endpoint with next(iter().
                    EndptName = next(iter(endpoints[counter]))

                    #Counts each container Name and its State:
                    countApps = 0
                    while countApps < len(endpoints[counter][EndptName]): #len(endpoints[counter][EndptName]) is the number of containers.
                        ENDPOINTNAME = next(iter(endpoints[counter]))
                        NAME = endpoints[counter][EndptName][countApps][0]
                        STATE = endpoints[counter][EndptName][countApps][1]

                        # print(ENDPOINTNAME)
                        # print(NAME)
                        # print(STATE)

                        update_metrics(ENDPOINTNAME, NAME, STATE)

                        countApps+=1

                    counter+=1

            if args.debugging:
                print("\nThe server is running. (" + str(seconds) + "s)\n")

            time.sleep(1)
            seconds+=1

    except:
        print("\nThe server stopped. Total seconds (" + str(seconds) + ")\n")
        exit(0)
