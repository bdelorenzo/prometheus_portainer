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
        count = 0
        while True:
            try:
                container = info[count]
                count+=1
            except:
                break
        
        #Display number of containers.
        print("\nNumber of Containers: " + str(count) + "\n")
            
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
