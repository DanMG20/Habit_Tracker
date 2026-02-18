import customtkinter as ctk
from infrastructure.config import defaults as df 
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class DateHeader(ctk.CTkFrame): 


    state_key = "date_header"
    events = {"view_changed", "day_changed"}

    def __init__(self,master,style_settings): 

        super().__init__(master=master, corner_radius= df.CORNER_RADIUS)
        self.fonts = style_settings["fonts"]
        self._build_static()


    def _build_static(self):
        self._draw_label()
        


    def _draw_label(self):
        self.header = ctk.CTkLabel(
            self,
            text="",
            anchor="center",
            font=self.fonts["SUBTITLE"],
        )
        self.header.pack(fill="both", expand=True, pady=df.PADY, padx=df.PADX)




    def refresh(self, header):
        if not header:
            return
        self.header.configure(text = header)