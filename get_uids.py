from ibm_watson_machine_learning import APIClient
from dotenv import load_dotenv, find_dotenv
import os

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    api_key = os.environ.get("APIKEY")
    location = os.environ.get("REGION")

    wml_credentials = {
        "apikey": api_key,
        "url": 'https://' + location + '.ml.cloud.ibm.com'
    }

    client = APIClient(wml_credentials)
    print("Printing spaces:")
    client.spaces.list()
    client.set.default_space(os.environ.get("SPACE_UID"))
    print("Printing deployments:")
    client.deployments.list()