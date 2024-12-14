from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from pathlib import Path
import logging

#####

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()         # Shows logs
    ]
)

#####

class Database:

    def __init__(self, path: Path, type: str):
        self.path = Path(path)
        self.type = str(type)
        self.suffix = self.path.suffix
        self.suffix_list = [".db", ".sqlite"]
        #self.llm = Assistant("llama3.1", 0.5)
        self.file_exist = self._check_file()
        self.loaded_db = self._load_db()
        self.table_columns = self.loaded_db.get_usable_table_names()

    def _check_file(self) -> bool:
        """
        Takes a string path, turns it into Path object for better control and checks existence and correct suffix.

        Args:
            self : the Database object
                self.path (str): The path attribute.
        
        Returns:
            bool True: The file is fine.
            bool False: There's an error with the file
        """
        if self.path.exists():
            if self.suffix in self.suffix_list:
                return True
            else:
                raise ValueError(f"Database file suffix is not supported...\nExpected suffixes: {self.suffix_list}.\nGiven suffix: {self.suffix}")
        else:
            raise FileNotFoundError(f"File at {self.path} not found...")
        
    def _load_db(self) -> SQLDatabase:
        """Loads SQL database into a Langchain object."""
        if self.file_exist:
            if self.type == "sqlite":
                logging.info(f"Database Langchain object successfuly created: {self.path}")
                return SQLDatabase.from_uri(f"sqlite:///{self.path}")
            else:
                raise ValueError(f"Given Database type attribute of {self.path.name} doesn't match database type, could be incorrect...\nGiven Database object type: {self.type}")
        else:
            return None