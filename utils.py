import json

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

def get_credentials():
    # Load credentials from the JSON file
    with open('credentials.json', 'r') as file:
        credentials_data = json.load(file)

    # Extract the required variables
    ENDPOINT_URL = credentials_data['ENDPOINT_URL']
    API_KEY = credentials_data['API_KEY']
    PROJECT_ID = credentials_data['PROJECT_ID']

    return ENDPOINT_URL, API_KEY, PROJECT_ID

ENDPOINT_URL, API_KEY, PROJECT_ID = get_credentials()

def ask_llm(question, model="meta-llama/llama-3-3-70b-instruct", max_tokens=4000):
    credentials = Credentials(
        url=ENDPOINT_URL,
        api_key=API_KEY
    )

    model = ModelInference(
        model_id=model,
        credentials=credentials,
        project_id=PROJECT_ID,
        params={
            "max_tokens": max_tokens
        }
    )

    result = model.chat(messages=[{'role': 'user', 'content': question}])
    return result['choices'][0]['message']['content']

def get_domain_promp():
    with open("prompts/domain.txt", "r") as file:
        domain = file.read()
    return domain

def get_info_promp():
    with open("prompts/informazioni_base.txt", "r") as file:
        info = file.read()
    return info

