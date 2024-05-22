import requests
from dotenv import load_dotenv
import os

load_dotenv()
qualtrics_token = os.getenv("QUALTRICS_TOKEN")
def get_all_survey_info(qualtrics_token):
    url = "https://yourdatacenterid.qualtrics.com/API/v3/surveys"

    headers = {
        "X-API-TOKEN": qualtrics_token
    }

    all_survey_info = []

    while url:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            survey_data = response.json()["result"]["elements"]
            survey_info = [(survey["id"], survey["name"]) for survey in survey_data if "LaSER" in survey["name"]]
            #survey_info = [(survey["id"], survey["name"]) for survey in survey_data]
            all_survey_info.extend(survey_info)
            url = response.json()["result"].get("nextPage", None)
        else:
            print("Failed to retrieve survey info. Status code:", response.status_code)
            return None

    return all_survey_info


    
survey_info = get_all_survey_info(qualtrics_token)
print(survey_info)