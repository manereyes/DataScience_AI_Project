from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from pathlib import Path
from logger.logger import generate_log

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
        Validates the existence of a file via its path and suffix.
            
        Returns:
            bool:
                - 'True' if the file exists and its suffix is valid.

        Raises:
            FileNotFoundError: If the file does not exist at a specified path.
            ValueError: If the file suffix is not supported or not valid.
        
        Example:
            >>> self.path("example.db")
            >>> self.suffix(".db")
            >>> self.suffix_list = [".db", ".sqlite"]
            >>> self._check_file()
            >>> True

        # If the file does not exist:
            >>> self.path = Path("nonexistent.db")
            >>> self._check_file()
            FileNotFoundError: File at nonexistent.db not found...

        # If the suffix is unsupported:
            >>> self.path = Path("example.txt")
            >>> self._check_file()
            ValueError: Database file suffix is not supported...
                    Expected suffixes: ['.db', '.sqlite'].
                    Given suffix: .txt
        """
        if self.path.exists():
            if self.suffix in self.suffix_list:
                return True
            else:
                raise ValueError(f"Database file suffix is not supported...\nExpected suffixes: {self.suffix_list}.\nGiven suffix: {self.suffix}")
        else:
            raise FileNotFoundError(f"File at {self.path} not found...")
        
    def _load_db(self) -> SQLDatabase:
        """
        Loads SQL database into a Langchain SQLDatabase object.
        
        Returns: 
        """
        if self.file_exist:
            if self.type == "sqlite":
                generate_log(1, f"Database Langchain object successfuly created: {self.path}")
                return SQLDatabase.from_uri(f"sqlite:///{self.path}")
            else:
                raise ValueError(f"Given Database type attribute of {self.path.name} doesn't match database type, could be incorrect...\nGiven Database object type: {self.type}")
        else:
            return None