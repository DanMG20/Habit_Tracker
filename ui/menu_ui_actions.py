from dataclasses import dataclass
from typing import Callable

@dataclass
class MenuUIActions:
    open_font: Callable
    reset_files: Callable
    open_add_quote: Callable
    open_add_goal: Callable
    open_about: Callable
    change_appearance: Callable
    change_theme: Callable
