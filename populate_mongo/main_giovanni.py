# main.py
from ibm_watsonx_ai.foundation_models import ModelInference
from populate_json import JSONPopulator
from populate_mongo import MongoPopulator
import os
from ibm_watsonx_ai import Credentials
import json 

ENDPOINT_URL="https://us-south.ml.cloud.ibm.com"
API_KEY="edsLkpMKNcg95Ts1Lfuvv3w2_K4kL5owh97pTjpAdOuJ"
PROJECT_ID="4f651d94-e286-4726-b84b-0df69a71dfd3"


credentials = Credentials(
    url=ENDPOINT_URL,
    api_key=API_KEY
)
def init_model():
    return ModelInference(
        model_id="meta-llama/llama-3-405b-instruct",
        credentials=credentials,
        project_id=PROJECT_ID,
        params={"max_tokens": 20000}
    )

def main():
    try:
        # Inizializza il modello
        model = init_model()
        print("Modello inizializzato con successo")

        # Inizializza i populator
        json_populator = JSONPopulator(model)
        mongo_populator = MongoPopulator()

        # Connetti a MongoDB
        if not mongo_populator.connect():
            print("Errore nella connessione a MongoDB")
            return

        # Processa i documenti
        menu_folder = "Hackapizza Dataset/Menu/"
        for index, doc in enumerate(os.listdir(menu_folder)[5:7]):
            print(f"Processando documento: {doc}")
            
            doc_path = f"{menu_folder}{doc}"
            text = json_populator.pdf_to_text(doc_path, index)
            if not text:
                continue
                
            result = json_populator.process_document(text)
            if not result:
                continue
                
            json_data = json_populator.clean_and_parse_json(result)
            if not json_data:
                continue
                
            mongo_populator.insert_document(json_data)

    except Exception as e:
        print(f"Errore nell'esecuzione: {str(e)}")

if __name__ == "__main__":
    main()