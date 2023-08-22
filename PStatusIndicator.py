import subprocess
import ast
import json

try:
    def getAndFindData():
        #Define the command to get the container configuration and writing to a JSON file "containerAPI.json".

        apiKey = "ptr_ZZjjmWCiS5YOJcpCd3xIcpLImTwO2LxWNMsWByGJ0jw="
        url = "https://portainer.delorenzo.mobi/api/endpoints/2/docker/containers/json?all=true"

        getJSON = ("API_KEY=" + apiKey + 
        "\ncurl -X GET --header 'Content-Type: application/json' --header \"x-api-key: $API_KEY\" --url '" + 
        url + "' | jq > containerAPI.json")

        # getJSON = """ 
        # API_KEY='ptr_ZZjjmWCiS5YOJcpCd3xIcpLImTwO2LxWNMsWByGJ0jw='
        # curl -X GET --header 'Content-Type: application/json' --header "x-api-key: $API_KEY" --url 'https://portainer.delorenzo.mobi/api/endpoints/2/docker/containers/json?all=true' | jq > containerAPI.json
        # """

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
                #print("Break!")
                break
        
        print("Number of Containers: " + str(count) + "\n") #Display number of containers.
    
        #Find the data in JSON.
        containerNumber = 0
        #Prints Name, State and Status of each container.
        while containerNumber < count:
            print("\tContainer: " + info[containerNumber]["Names"][0][1:] +
            "\n\tState: " + info[containerNumber]["State"] +
            "\n\tStatus: " + info[containerNumber]["Status"] + "\n")
            containerNumber+=1

    getAndFindData()

except:
    print("! Error while retreiving data, please check your internet connection.")
