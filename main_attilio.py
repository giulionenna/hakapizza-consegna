import json_schema_extractor
from json_schema_extractor import JSONSchemaExtractorAgent
import os
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

ENDPOINT_URL="https://us-south.ml.cloud.ibm.com"
API_KEY="edsLkpMKNcg95Ts1Lfuvv3w2_K4kL5owh97pTjpAdOuJ"
PROJECT_ID="4f651d94-e286-4726-b84b-0df69a71dfd3"

credentials = Credentials(
    url=ENDPOINT_URL,
    api_key=API_KEY
)

def main():
    model = ModelInference(
    model_id="meta-llama/llama-3-405b-instruct", 
    credentials=credentials,
    project_id=PROJECT_ID,
   )
    json_schema_extractor = JSONSchemaExtractorAgent("test_path",model,n_files=2)
    #json_schema_extractor.set_main_prompt("Stai analizzando un insieme di documenti su dei ristoranti fantastici ambientati in una galassia immaginaria.")
    json_schema_extractor.set_main_prompt("Stai analizzando un insieme di documenti su dei ristoranti fantastici ambientati in una galassia immaginaria. Il tuo obiettivo è estrarre uno schema JSON che rappresenti i dati principali di questi documenti.Non popolare i campi del json rispondi solo con lo schema")

    collectionDescription=json_schema_extractor.extract_json_schema()
    print(collectionDescription)  

main()