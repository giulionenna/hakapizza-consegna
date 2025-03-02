import os
import PyPDF2
from structure import JSONStructureManager
import json

class JSONPopulator:
    def __init__(self, model):
        self.model = model
        self.structure_manager = JSONStructureManager()
        self.json_structure = self.structure_manager.get_default_structure()
        self.main_prompt = self.structure_manager.create_prompt(self.json_structure)

    def pdf_to_text(self, doc_path, index):
        try:
            with open(doc_path, "rb") as f:
                pdf = PyPDF2.PdfReader(f)
                text = f"\nDocumento {index}:\n"
                for page in pdf.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            print(f"Errore nel processare {doc_path}: {e}")
            return None

    def process_document(self, text):
        try:
            prompt = self.main_prompt + text
            result = self.model.chat(messages=[{'role': 'user', 'content': prompt}])
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"Errore nell'elaborazione: {e}")
            return None

    def clean_and_parse_json(self, json_string):
        try:
            clean_string = json_string.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_string)
        except json.JSONDecodeError as e:
            print(f"Errore nel parsing JSON: {e}")
            return None