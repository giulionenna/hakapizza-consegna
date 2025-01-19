

import os
import PyPDF2

#create class to extract json schema
class JSONSchemaExtractorAgent:
    def __init__(self, files_path,llm, n_files=3,main_prompt="", initial_prompt="",end_prompt="",openai_model=""):
        self.file_path = files_path
        self.model = llm
        self.initial_prompt = initial_prompt
        self.end_prompt = end_prompt
        self.jsonSchema=""
        self.collectionDescription=""
        self.main_prompt=main_prompt
        self.openai_model=openai_model
        self.n_files = n_files


    def set_main_prompt(self, prompt):
        self.main_prompt = prompt

    def extract_json_schema(self,added_prompt=""):
        complete_text = ""
        tot_files = len(os.listdir(self.file_path))
        last_output=""
        for index, doc in enumerate(os.listdir(self.file_path)):
            try:
                if ".pdf" not in doc:
                    print(f"Skipping {doc} as it is not a pdf file")
                    continue
                with open(f"{self.file_path}/{doc}", "rb") as f:
                    text = ""
                    #read pdf file
                    pdf = PyPDF2.PdfReader(f)
                    #extract text from pdf file
                    complete_text += f"\n#################\nDocument number: {index+1}\n#######################\n"
                    for page in pdf.pages:
                        text += page.extract_text()
                    complete_text+=text

                    if (index+1) % self.n_files == 0 or (index+1) == tot_files: 
                        prompt = f"""{self.main_prompt}\n
                                    {self.initial_prompt}\n
                                    {complete_text}\n  
                        """
                        if last_output != "":
                            prompt += f"""Questo è l'ultimo json estratto:\n{last_output}\n
                            Migliora lo schema JSON precedente analizzando le informazioni dei nuovi documenti. Non popolare i campi del json rispondi solo con lo schema\n 
                            """
                        prompt += f"{self.end_prompt}\nRespond only with valid JSON. Do not write an introduction or summary."
                        print("Extracting json schema for document number: ",index+1) 

                        if self.openai_model!="":
                            print("Using OpenAI model...")
                            result=   self.model.chat.completions.create(
                                model=self.openai_model,
                               messages=[
                                            {
                                                "role": "user",
                                                "content": prompt,
                                            }
                                        ],
                            )

                            last_output=result.choices[0].message.content

                        else: 
                            result = self.model.chat(messages=[{'role': 'user', 'content': prompt}])
                            last_output = result['choices'][0]['message']['content']
                        complete_text=""
            except Exception as e:
                print(f"Error while processing file {doc}")
                print(e)
                continue

        self.jsonSchema=last_output
        return last_output    
    
    def get_json_schema(self):
        return self.jsonSchema

    def format_json_schema(self):
        pass

    def generate_collection_description(self):
        main_prompt=self.main_prompt+f"""
       Sei incaricato di analizzare una collezione di documenti relativi a ristoranti e ai menu che propongono. La tua analisi deve concentrarsi sulla struttura e sui temi generali trattati in questi documenti, senza soffermarti sui dettagli specifici di ogni ristorante.
        Devi identificare i paragrafi principali,  i temi principali trattati e ricorrenti, e le strutture generali dei documenti.
        Il tuo obiettivo è informare un utente generico sui contenuti e le strutture principali di questa collezione di documenti.
        Genera una descrizione sintetica e informativa che riassuma i temi trattati nei documenti e la loro organizzazione. Non includere dettagli identificativi o descrizioni specifiche dei ristoranti ed esempi.
        Non fornire esplicitamente le informazioni estratte dai documenti quali nomi del ristorante o dei piatti, ma descrivi in modo generale i contenuti e le strutture principali dei documenti che hai identificato.
        Utilizza massimo 300 parole per descrivere la collezione di documenti.
        NEL CASO LA DESCRIZIONE SIA TROPPO LUNGA SINTETIZZA LE INFORMAZIONI PIÙ RILEVANTI.
        """
        complete_text = ""
        tot_files = len(os.listdir(self.file_path))
        last_output=""
        for index, doc in enumerate(os.listdir(self.file_path)):
            if ".pdf" not in doc:
                print(f"Skipping {doc} as it is not a pdf file")
                continue
            with open(f"{self.file_path}/{doc}", "rb") as f:
                text = ""
                #read pdf file
                pdf = PyPDF2.PdfReader(f)
                #extract text from pdf file
                complete_text += f"\n#################\nDocument number: {index+1}\n#######################\n"
                for page in pdf.pages:
                    text += page.extract_text()
                complete_text+=text

                if (index+1) % self.n_files == 0 or (index+1) == tot_files: 
                    prompt = f"""{self.main_prompt}\n
                                {self.initial_prompt}\n
                                {complete_text}\n  
                    """
                    if last_output != "":
                        prompt += f"""Questa è l'ultima descrizione generata:\n{last_output}\n
                        Se necessario migliora lo descrizione precedente analizzando le informazioni dei nuovi documenti aggiungendo nuovi dettagli.\n 
                        """
                    prompt += f"{self.end_prompt}\n"

                    print("Generating collection description for document number: ",index+1)
                    if self.openai_model!="":
                            print("Using OpenAI model...")
                            result=   self.model.chat.completions.create(
                                model=self.openai_model,
                               messages=[
                                            {
                                                "role": "user",
                                                "content": prompt,
                                            }
                                        ],
                            )

                            last_output=result.choices[0].message.content

                    else:
                        result = self.model.chat(messages=[{'role': 'user', 'content': main_prompt+"\n"+prompt}])
                        last_output = result['choices'][0]['message']['content']
                    complete_text=""
        self.collectionDescription=last_output
        return last_output