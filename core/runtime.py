"""
Module handling runtime execution context and process lifecycle management.
"""

import os
import sys
from typing import NoReturn


def restart_application() -> NoReturn:
    """
    Restarts the application by completely replacing the current process.

    This function uses the OS-level execution replacement mechanism. 
    Any code placed after the invocation of this function will never be executed.
    """
    os.execl(sys.executable, sys.executable, *sys.argv)