from langchain_ollama import OllamaLLM
from sql_tools import Database
from prompts.llm_prompts import sql_retriever_prompt
import logging
import sqlite3
import csv

#####

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()         # Shows logs
    ]
)

#####

class Assistant:

    def __init__(self, model: str, temp: int):
        self.model = model
        self.temp = temp
        self.llm = OllamaLLM(model=self.model, temperature=self.temp)

    def get_data(self, path: str, type: str, input: str, output: str = 'csv'):
        """Retrieves data from the Database Object giving it the path, type and output"""
        logging.info(f"get_data running...")
        self.database = Database(path, type)
        self.input = input
        self.column_names = self.database.table_columns
        self.output_type = output
        self.data, self.csv_columns = self._retrieve_database(self.input, self.database, self.column_names)

        if self.output_type == 'csv':
            with open('./data/example_data', mode='w', newline='', encoding='utf-8',) as file:
                writer = csv.writer(file)
                writer.writerow(self.csv_columns)
                writer.writerows(self.data)

        return logging.info(f"CSV File created at assigned path!")

    def _generate_query(self, input: str, columns: list) -> str:
        """Generates a SQL query with a formatted prompt calling the LLM"""
        self.prompt = sql_retriever_prompt(input, columns)
        logging.info(f"Prompt generated, now running...")
        return self.llm.invoke(self.prompt)

    def _retrieve_database(self, input: str, database: Database, columns: list):
        """Retrieves data from a query with an SQL connection and turns it into a file"""
        self.query = self._generate_query(input, columns)
        logging.info(f"Query: {self.query} generated!")
        conn = sqlite3.connect(database.path)
        cursor = conn.cursor()
        execution = cursor.execute(self.query)
        data = execution.fetchall()
        columns = [ name[0] for name in execution.description ]
        logging.info(f"Data retrieved from Database {database.path}!")
        conn.close()
        return data, columns # a list of rows and the list of columns

path = "./database/olist.sqlite"
db_type = "sqlite"
input = "Give me all the information about the order reviews"
assistant = Assistant("Llama3.1", 0.5)
assist_obj = assistant.get_data(path, db_type, input)
print(assist_obj)