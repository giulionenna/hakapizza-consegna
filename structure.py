class JSONStructureManager:
    @staticmethod
    def get_default_structure():
        return {
            "restaurant": {
                "name": "String",
                "description": "String",
                "chef": {
                    "name": "String",
                    "description": "String",
                    "abilities": "String[]"
                },
                # ... resto della struttura ...
            }
        }

    @staticmethod
    def create_prompt(json_structure):
        return f"""Sei un esperto analizzatore di documenti in ambito ristorazione galattica e fantasy.
        Il tuo compito è analizzare documenti di menù e estrarre informazioni strutturate secondo uno schema JSON predefinito.
        
        REGOLE IMPORTANTI:
        - Devi mantenere la stessa struttura JSON fornita
        - Compila TUTTI i campi, non lasciare valori nulli
        - Se un'informazione non è presente nel testo, usa valori plausibili basati sul contesto
        - Mantieni la coerenza tra le varie parti del documento
        
        CONTESTO SPECIFICO:
        - I documenti provengono da ristoranti in un universo fantasy/sci-fi
        - Ogni chef ha abilità speciali e licenze specifiche
        - Le tecniche di cucina possono includere elementi magici o tecnologici
        - Gli ingredienti possono provenire da diverse dimensioni o pianeti
        
        REGOLA DA SEGUIRE: RISPONDI SOLO CON IL JSON, NON AGGIUNGGERE COMMENTI O INTESTAZIONI
        
        STRUTTURA DA POPOLARE:
        {json_structure}
        
        DOCUMENTO DA ANALIZZARE:
        """