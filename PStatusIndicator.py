import subprocess
import ast
import json
import argparse

#Create parser.
parser = argparse.ArgumentParser(description = "Portainer Prometheus Script.")
#Define argumetns.
parser.add_argument("-apik", "--apikey", type=str, help="Indicates which Portainer API Key")
parser.add_argument("-url", type=str, help="Indicates which Portainer URL")
#Parse the rguments.
args = parser.parse_args()

def getAndFindData(APIK, URL):
    apiKey = APIK
    url = URL

    try:
        #Define the command to get the container configuration and writing to a JSON file "containerAPI.json".
        getJSON = ("API_KEY=" + apiKey + 
        "\ncurl -X GET --header 'Content-Type: application/json' --header \"x-api-key: $API_KEY\" --url '" + 
        url + "' | jq > containerAPI.json")

        #Excecuting the command.
        subprocess.run(getJSON, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        #Reading the JSON file and loading in a python dictionary "info".
        with open("containerAPI.json") as openJSON:
            info = json.load(openJSON)
            openJSON.close()

        #Count the number of containers.
        count = 0
        while True:
            try:
                container = info[count]
                count+=1
            except:
                break
        
        print("\nNumber of Containers: " + str(count) + "\n") #Display number of containers.
            
        #Find the data in JSON: Prints Name, State and Status of each container.
        containerNumber = 0
        while containerNumber < count:
            print("\tContainer: " + info[containerNumber]["Names"][0][1:] +
            "\n\tState: " + info[containerNumber]["State"] +
            "\n\tStatus: " + info[containerNumber]["Status"] + "\n")
            containerNumber+=1

    except:
        #Print error message.
        print("\n! Error while retreiving data, possible errors:" +
        "\n - No internet connection." +
        "\n - Invalid API key or URL." +
        "\nPlease make sure to use the parameters, run this script followed by \"--help\" for more information.\n")

getAndFindData(args.apikey, args.url)
