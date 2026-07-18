"""
Module providing system environment purging and baseline data factory resets.
"""

import shutil
from utils.paths import APPDATA_DIR
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class ResetService:
    """
    Domain service responsible for clearing application runtime files and persistent state caches.
    """

    def __init__(self) -> None:
        self._target_dir = APPDATA_DIR

    def reset_files(self) -> None:
        if not self._target_dir.exists():
            logger.warning(f"Target directory '{self._target_dir}' does not exist. Aborting purge.")
            return

        for child in self._target_dir.iterdir():
            try:
                if child.is_file() or child.is_symlink():
                    child.unlink()
                elif child.is_dir():
                    shutil.rmtree(child)
                logger.info(f"Successfully deleted: {child.name}")
            except OSError as error:
                logger.error(f"Failed to delete '{child.name}' during environment reset: {error}")