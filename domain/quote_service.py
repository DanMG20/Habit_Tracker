import json 
from typing import Optional, Tuple, List 
from utils.paths import resource_path
from infrastructure.logging.logger import get_logger 
logger = get_logger(__name__)

class QuoteService:
    def __init__(self, quote_repository):
        self._repo = quote_repository

    def initialize_quotes(self):
        """
        Ensures initial quotes on database. 
        """
    
        if self._repo.count() > 0:
            return

        default_quotes = self._load_default_quotes() 
        self.add_quotes(default_quotes)

    def get_quote(self):
        return self._repo.get_random()

    def get_all_quotes(self):
        return self._repo.get_all()

    def delete_selected_quote(self, quote_id):
        self._repo.delete_by_id(quote_id)
  

    def add_quotes(self,quotes: List[Tuple[str,str]]) -> None:
        self._repo.insert_many(quotes)

    def update_quote(self,quote_id, new_quote, new_author): 
        self._repo.update(quote_id,
                          new_quote,
                          new_author)    

    def _load_default_quotes(self): 
        path = resource_path("resources\\json\\default_quotes.json")

        try:
            with open(path, "r", encoding="utf-8") as file:
                default_quotes = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error al leer el archivo de frases: {e}")
            default_quotes = []

        return [(item["quote"], item.get("author", "")) for item in default_quotes] 

