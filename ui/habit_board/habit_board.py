import customtkinter as ctk
from infrastructure.config import defaults as df
from ui.habit_board.habit_board_header import HabitBoardHeader
from ui.habit_board.habit_board_table import HabitBoardTable

from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)


events = {"habit_changed", "week_changed", "day_changed"}

class HabitBoard(ctk.CTkFrame): 
    def __init__(self, 
                 master, 
                 style_settings,
                 show_yesterday_check_panel,
                 show_today_panel
                 ):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)
        self.style_settings = style_settings
        self.fonts = style_settings["fonts"]
        self.theme_colors = style_settings["colors"]
        self.show_yesterday_panel = show_yesterday_check_panel
        self.show_today_panel = show_today_panel

        self.build()

    
    def build(self):
        self.draw_header()
        self.draw_scroll_frame()
        self.draw_board()

    def refresh(self, view_state):

        habit_board_state = view_state.get("habit_board")

        if not habit_board_state:
            return

        self.header.refresh(habit_board_state)
        self.board.refresh(habit_board_state)

    def draw_header(self):
        self.header = HabitBoardHeader(
            master=self,
            style_settings = self.style_settings,
            show_yesterday_panel=self.show_yesterday_panel,
            show_today_panel = self.show_today_panel,
        )
        self.header.grid(row=0, column=0, sticky="nsew", padx =(0,22))       
    
    def draw_scroll_frame(self):
        
        self_habit_table = ctk.CTkScrollableFrame(
            self,
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"],
        )
        self_habit_table.grid(
            row=1, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY
        )
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

    def draw_board(self): 
        self.board = HabitBoardTable(
            master= self,
            style_settings= self.style_settings
        )
        self.board.grid(row=1, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY)


