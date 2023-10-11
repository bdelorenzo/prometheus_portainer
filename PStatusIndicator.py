import subprocess
import ast
import json
import argparse
from prometheus_client import start_http_server, Gauge
import time
import os

#Creating the Gauge.
container_state = Gauge("container_state", "State of the container", ["container_name"])

#Create parser.
parser = argparse.ArgumentParser(description = "Portainer Prometheus Script.")
#Define argumetns.
parser.add_argument("-apik", "--apikey", type=str, help="Indicates which Portainer API Key (mandatory)")
parser.add_argument("-url", type=str, help="Indicates which Portainer URL (mandatory)")
parser.add_argument("-debug", "--debugging", action='store_true', help="Shows containers (optional)")
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

        #Count the number of containers.
        count = 0 #Indicates the number of containers.
        while True:
            try:
                container = info[count]
                count+=1
            except:
                break
            
        #Find the data in JSON: Gets Names and State of each container.
        containerNumber = 0
        while containerNumber < count:
            #Adding information to a list.
            container_info.append((info[containerNumber]["Names"][0][1:],
            info[containerNumber]["State"]))

            if(args.debugging):
                #Debugging
                print("\n\tContainer: " + info[containerNumber]["Names"][0][1:] +
                "\n\tState: " + info[containerNumber]["State"] + "\n")

            containerNumber+=1
        
        return container_info #Returns container list.

    except:
        #Print error message.
        print("\n! Error while retreiving data, possible errors:" +
        "\n - No internet connection." +
        "\n - Invalid API key or URL." +
        "\nPlease make sure to use the parameters, run this script followed by \"--help\" for more information.\n")
        return container_info #Returns empty container list.

#Update the gauge with the provided values.
def update_metrics(container_name, state):
    container_state.labels(container_name=container_name).set(1 if state == 'running' else 0)

#Starts HTTP server.
if __name__ == "__main__":
    start_http_server(8000)
    seconds = 1

    try:
        while True:
            #Gets list of containers.
            containers = getAndFindData(args.apikey, args.url)

            #Validate if the list came empty.
            if not containers:
                exit(0)
            else: #Proceeds if list is not empty.
                for information in containers:
                    update_metrics(*information)                 

            print("The server is running. (" + str(seconds) + "s)")
            time.sleep(1)
            seconds+=1
    except:
        print("\nThe server stopped. Total seconds (" + str(seconds) + ")\n")
        exit(0)