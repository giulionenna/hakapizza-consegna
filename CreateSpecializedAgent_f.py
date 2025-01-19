from langchain_ibm import ChatWatsonx
from langchain_openai import ChatOpenAI
from ibm_watsonx_ai.foundation_models import ModelInference
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from credentials import *
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import Literal, Annotated
import json
from pymongo import MongoClient
from typing import List, Dict

class CreateSpecializedAgent:
    def __init__(self, llm, json_schema, collection_description, mongo_uri = "mongodb://localhost:27017/", db_name = "hackapizza", collection_name = "Documents_1"):
        self.llm = llm
        self.json_schema = json_schema
        self.collection_description = collection_description
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        collection_description_prompt = """
        Sei un esperto computer engineer abile nell'interrogare database MongoDB.
        Sei un agente che deve rispondere a delle query da un insieme di documenti. Ecco una descrizione della collezione di documenti con cui lavorerai:
        {collection_description}
        devi usare gli strumenti che ti vengono dati per rispondere alle query sulla collezione di documenti.
        """

        self.query_translation_prompt = """
        You are given a query in natural language and a json schema. The json schema is the schema of the json documents in a MongoDB collection that will be queried. You will translate the natural language query into a series of mongoDB queries. The queries will be executed with an "aggregate" function. You only have to return the mongodb queries, not the python code. since queries will be executed with an aggregate function, you can use any of the aggregate operators. Most of the times the query is not a simle filter but requires also a particolar view of the result (maybe pivots using the $unwind operator).

        JSON SCHEMA:
        {json_schema}

        NATURAL LANGUAGE QUERY:
        {query}
        """

        self.query_translation_schema={
        "title": "Query_Translation",
        "description": " Traduci Una query in linguaggio naturale in una serie di query MongoDB che verranno eseguite con una funzione aggregate",
        "type": "object",
        "properties": {
            "queries": {
            "description" : "Una serie di query MongoDB che verranno eseguite con una funzione aggregate",
            "type": "array",
            "items": {
                "type": "string",
                "description": "Una query MongoDB, deve essere una chiave-valore in parentesi graffe e sia la chiave che il valore devono essere stringhe incapsulate in una coppia di apici. Esempio: {'$match': {'name': 'John'}"
            }
            }
        },
        "required": ["queries"],
        "additionalProperties": False
        }

        collection_description_prompt = """
        You are an agent that needs to answer queries from a set of documents. Here is a description of the document collection you will be working with:
        {collection_description}
        You need to use the tools that you are given to answer queries about the document collection. 
        """
        
        self.translation_llm = llm.with_structured_output(self.query_translation_schema)
        self.system_prompt = collection_description_prompt.format(collection_description=collection_description)
        
        @tool
        def query_mongodb(query : str)-> str:
            """function that takes a query in natural language and queries the mongodb"""
            prompt = self.query_translation_prompt.format(json_schema=json_schema, query=query)
            result = self.translation_llm.invoke(prompt)
            print(result)
            
            final_list = []

            for query in result["queries"]:
                try:
                    if type(query) == str:
                        final_list.append(eval(query))
                    else:
                        final_list.append(query)
                except Exception as e:
                    print(f"Error: {query}")
                    print(e)
                    continue

            result = self.collection.aggregate(final_list)

            # Itera sui risultati
            res = ""
            for doc in result:
                res += str(doc)
                print(doc)
            return res
        
    
        self.agent = create_react_agent(self.llm, [query_mongodb],
                                         state_modifier=SystemMessage(self.system_prompt),
                                           debug=False)
