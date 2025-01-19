from pymongo import MongoClient

class MongoPopulator:
    def __init__(self, uri='mongodb://localhost:27017/', db_name='hackapizza', collection_name='restaurants'):
        self.uri = uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            print("Connessione a MongoDB riuscita!")
            return True
        except Exception as e:
            print(f"Errore di connessione MongoDB: {e}")
            return False

    def insert_document(self, document):
        try:
            self.collection.insert_one(document)
            print("Documento inserito con successo")
            return True
        except Exception as e:
            print(f"Errore nell'inserimento: {e}")
            return False