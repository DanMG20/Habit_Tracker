import customtkinter as ctk
from infrastructure.config import defaults as df
from ui.habit_board.habit_board_header import HabitBoardHeader
from ui.habit_board.habit_board_table import HabitBoardTable

from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

class HabitBoard(ctk.CTkFrame): 
    def __init__(self,master,fonts,theme_colors, on_check_yesterday, get_week_state,date,get_state):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)
        self.master = master 
        self.fonts = fonts
        self.theme_colors = theme_colors
        self.on_check_yesterday = on_check_yesterday
        self.get_week_state = get_week_state
        self.date = date
        self.get_state = get_state

        self.build()
        logger.info("Succesfully built")

    
    def build(self):
        self.draw_header()
        self.draw_scroll_frame()
        self.draw_board()

    def refresh(self): 
        self.board.refresh()
        self.header.refresh()


    def draw_header(self):
        self.header = HabitBoardHeader(
            master=self,
            fonts = self.fonts,
            theme_colors= self.theme_colors,
            on_check_yesterday_event=self.on_check_yesterday,
            get_week_state=self.get_week_state,
            today = self.date,
        )
        self.header.grid(row=0, column=0, sticky="nsew")       
    
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
            self,
            self.fonts,
            self.theme_colors,
            self.get_state,
            self.date
        )
        self.board.grid(row=1, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY)


