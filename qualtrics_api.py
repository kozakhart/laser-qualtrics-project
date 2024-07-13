import http.client

import os
import base64
import json
import zipfile
import time
import requests
from dotenv import load_dotenv
load_dotenv()
qualtrics_token = os.getenv("QUALTRICS_TOKEN")
test_survey_id = os.getenv("TEST_SURVEY_ID")

def get_bearer_token():
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    #create the Base64 encoded basic authorization string

    auth = "{0}:{1}".format(CLIENT_ID, CLIENT_SECRET)

    encodedBytes=base64.b64encode(auth.encode("utf-8"))

    authStr = str(encodedBytes, "utf-8")


    #create the connection 

    conn = http.client.HTTPSConnection("sjc1.qualtrics.com")

    body = "grant_type=client_credentials&scope=read:users"

    headers = {

    'Content-Type': 'application/x-www-form-urlencoded'

    }

    headers['Authorization'] = 'Basic {0}'.format(authStr)


    #make the request

    conn.request("POST", "/oauth2/token", body, headers)

    res = conn.getresponse()

    data = res.read()
    return data.decode("utf-8")

def start_export(token, surveyId):
    conn = http.client.HTTPSConnection("sjc1.qualtrics.com")

    payload = "{\n  \"format\": \"csv\"\n}"

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'X-API-TOKEN': token
    }

    conn.request("POST", f"/API/v3/surveys/{surveyId}/export-responses", payload, headers)

    res = conn.getresponse()
    data = res.read()

    decoded = data.decode("utf-8")
    print(data.decode("utf-8"))
    progressId= json.loads(decoded)["result"]["progressId"]
    get_progress(token, surveyId, progressId)

def get_progress(token, surveyId, exportProgressId):
    time.sleep(5)
    conn = http.client.HTTPSConnection("sjc1.qualtrics.com")

    headers = {
        'Accept': "application/json",
        'X-API-TOKEN': token
    }

    while True:
        conn.request("GET", f"/API/v3/surveys/{surveyId}/export-responses/{exportProgressId}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        decoded = data.decode("utf-8")
        status = json.loads(decoded)["result"]["status"]

        if status == "complete":
            fileId = json.loads(decoded)["result"]["fileId"]
            get_export2(token, surveyId, fileId)
            break
        else:
            print("Export not complete. Current status:", status)
            time.sleep(5)
    
def get_export(token, surveyId, fileId):
    url = f"https://sjc1.qualtrics.com/API/v3/surveys/{surveyId}/export-responses/{fileId}/file"
    headers = {
        'Content-Type': 'application/octet-stream, application/json',
        'X-API-TOKEN': token
    }

    response = requests.get(url, headers=headers)
    output_zip  = "output.zip"
    if response.status_code == 200:
        with open(output_zip, 'wb') as f:
            f.write(response.content)
        print(f"Response file downloaded successfully as {output_zip}")
        with zipfile.ZipFile(output_zip, 'r') as zip_ref:
            zip_ref.extractall()
        print("Zip file contents extracted to current directory.")
    else:
        print("Failed to download response file. Status code:", response.status_code)

def get_export2(token, surveyId, fileId):
    url = f"https://sjc1.qualtrics.com/API/v3/surveys/{surveyId}/export-responses/{fileId}/file"
    headers = {
        'Content-Type': 'application/zip',
        'X-API-TOKEN': token
    }

    response = requests.get(url, headers=headers)
    output_zip = "output.zip"
    if response.status_code == 200:
        with open(output_zip, 'wb') as f:
            f.write(response.content)
        print(f"Response file downloaded successfully as {output_zip}")
        with zipfile.ZipFile(output_zip, 'r') as zip_ref:
            zip_ref.extractall(encoding='utf-8')
        print("Zip file contents extracted to current directory.")
    else:
        print("Failed to download response file. Status code:", response.status_code)



start_export(qualtrics_token, 'SV_9XE4nP54e6GMvsy')
