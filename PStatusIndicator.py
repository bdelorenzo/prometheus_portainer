import subprocess
import ast
import json

try:
    #Define the command to get the container configuration and writing to a JSON file "containerAPI.json".
    getJSON = """ 
    API_KEY='ptr_ZZjjmWCiS5YOJcpCd3xIcpLImTwO2LxWNMsWByGJ0jw='
    curl -X GET --header 'Content-Type: application/json' --header "x-api-key: $API_KEY" --url 'https://portainer.delorenzo.mobi/api/endpoints/2/docker/containers/974a77279b0e44d3ceda9975081e7fd2d1ac24c92755b1c5dfb74163e15c2cb5/json' | jq > containerAPI.json
    """

    #Excecuting the command.
    subprocess.run(getJSON, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #Reading the JSON file and loading in a python dictionary "info".
    with open("containerAPI.json") as openJSON:
        info = json.load(openJSON)
        openJSON.close()

    #Printing the output. 
    print(info["State"]["Status"])

except:
    print("! Error while retreiving data, please check your internet connection.")