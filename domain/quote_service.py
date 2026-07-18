"""
Module providing quote management services, handling baseline seed data and run-time catalog mutations.
"""

import json
import sqlite3
from typing import List, Tuple, Dict, Any, Optional

from utils.paths import resource_path
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class QuoteService:
    """
    Domain service responsible for managing the application's motivational quote lifecycle.
    """

    DEFAULT_QUOTES_PATH: str = "resources/json/default_quotes.json"

    def __init__(self, quote_repository: Any) -> None:
        """
        Initializes the QuoteService injecting its persistent data access layer.

        Args:
            quote_repository (Any): Concrete infrastructure gateway managing the quotes table.
        """
        self._repo: Any = quote_repository
        self._initialize_quotes()

    def _initialize_quotes(self) -> None:
        """
        Guarantees the persistence layer contains baseline motivational seeding entries on startup.
        """
        if self._repo.count() > 0:
            return

        logger.info("Quotes catalog empty. Injecting system default baseline profiles.")
        default_quotes: List[Tuple[str, str]] = self._load_default_quotes() 
        if default_quotes:
            self.add_quotes(default_quotes)

    def get_quote(self) -> Optional[sqlite3.Row]:
        """
        Selects a random transactional quote record from the infrastructure repository.

        Returns:
            Optional[sqlite3.Row]: A database row containing text and author keys, or None if empty.
        """
        return self._repo.get_random()

    def get_all_quotes(self) -> List[sqlite3.Row]:
        return self._repo.get_all()

    def delete_selected_quote(self, quote_id: int) -> None:
        self._repo.delete_by_id(quote_id)
        logger.info(f"Successfully removed Quote ID {quote_id} from tracking structures.")
  
    def add_quotes(self, quotes: List[Tuple[str, str]]) -> None:
        self._repo.insert_many(quotes)
        logger.info(f"Bulk transaction successfully stored {len(quotes)} new entries.")

    def update_quote(self, quote_id: int, new_quote: str, new_author: str) -> None: 
        self._repo.update(quote_id, new_quote, new_author)
        logger.info(f"Quote ID {quote_id} fields successfully synchronized and updated.")

    def _load_default_quotes(self) -> List[Tuple[str, str]]: 
        """
        Deserializes the static fallback JSON resources file into valid entity payloads.

        Returns:
            List[Tuple[str, str]]: A list of translated structural data pairs matching (quote, author).
        """
        path: str = resource_path(self.DEFAULT_QUOTES_PATH)
        default_quotes: List[Dict[str, Any]] = []

        try:
            with open(path, "r", encoding="utf-8") as file:
                default_quotes = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as error:
            # Replaced print() with robust descriptive system logging
            logger.error(f"Failed to extract static quote definitions from target path '{path}': {error}")
            return []

        return [(item["quote"], item.get("author", "")) for item in default_quotes]