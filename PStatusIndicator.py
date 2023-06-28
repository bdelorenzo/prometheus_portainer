import os
import subprocess
import ast

#Define the command to get JSON file configuration.
getJSON = """ 
API_KEY='ptr_ZZjjmWCiS5YOJcpCd3xIcpLImTwO2LxWNMsWByGJ0jw='
curl -X GET --header 'Content-Type: application/json' --header "x-api-key: $API_KEY" --url 'https://portainer.delorenzo.mobi/api/endpoints/2/docker/containers/974a77279b0e44d3ceda9975081e7fd2d1ac24c92755b1c5dfb74163e15c2cb5/json' | jq
"""
#Execute the command and store it in a variable.
result = subprocess.run(getJSON, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output = result.stdout.decode()

#Processes the JSON string.
output = output[-26:]
output = "{" + output[:-7] + "}"
output = ast.literal_eval(output) #Converts str to dict.
print(output["Status"]) #Output.