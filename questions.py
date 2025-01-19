import pandas as pd
from utils import ask_llm, get_domain_promp, get_info_promp
import time
import os

class Questions():
    def __init__(self):
        self.questions = pd.read_csv("Hackapizza Dataset\domande.csv")

    def get_all_questions(self):
        self.questions_list = self.questions['domanda'].tolist()
        return self.questions_list
    
    def info_requested(self):
        prompt = str(get_domain_promp()) + """ Adesso ti fornisco il file delle domande, 
        Il tuo compito è dirmi solamente come poter strutturare un json per ottenere le informazioni richieste nelle domande.
        Il tuo messaggio verrà passato ad un modello di linguaggio che creerà un json con le informazioni necessarie.
        Devi ritornare solo un json schema."""

        self.info_question = ask_llm(prompt)
        return self.info_question

questions = Questions()
questions.get_all_questions()
start_time = time.time()
result = questions.info_requested()


output_dir = "results"
base_filename = "info_question"
file_extension = ".txt"

os.makedirs(output_dir, exist_ok=True)

i = 1
while os.path.exists(os.path.join(output_dir, f"{base_filename}_{i}{file_extension}")):
    i += 1
output_filename = os.path.join(output_dir, f"{base_filename}_{i}{file_extension}")
with open(output_filename, "w") as file:
    file.write(result)

end_time = time.time()

print(f"Time taken: {end_time - start_time} seconds")

