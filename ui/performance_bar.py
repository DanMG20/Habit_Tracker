import customtkinter as ctk 
import infrastructure.config.defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class PerformanceBar(ctk.CTkFrame):

    def __init__(self, master, style_settings):
        super().__init__(master=master, corner_radius=df.CORNER_RADIUS)

        self.fonts = style_settings["fonts"]
        self.theme_colors = style_settings["colors"]

        self.performance_bar = None
        self.performance_label = None

        self._build()

    def _build(self):
        self._draw_performance_bar()
        self._draw_performance_label()


    def refresh(self, view_state):

        performance = view_state.get("active_performance")

        if performance is None:
            self.performance_bar.set(0)
            self.performance_label.configure(text="0%")
            return
        logger.info(performance)
        self.performance_bar.set(performance / 100)
        self.performance_label.configure(text=f"{performance}%")




    def _render(self, performance):

        if performance is None:
            self.performance_bar.set(0)
            self.performance_label.configure(text="0%")
            return

        self.performance_bar.set(performance / 100)
        self.performance_label.configure(text=f"{performance}%")

    def _draw_performance_bar(self):
        self.performance_bar = ctk.CTkProgressBar(
            self,
            corner_radius=df.CORNER_RADIUS * 2,
        )

        self.performance_bar.pack(
            side="left",
            fill="both",
            expand=True,
            padx=df.PADX * 1.5,
            pady=df.PADY * 1.5,
        )


    def _draw_performance_label(self):
        self.performance_label = ctk.CTkLabel(
            self,
            font=self.fonts["SMALL"],
        )

        self.performance_label.pack(
            side="right",
            fill="both",
            padx=df.PADX * 2,
            pady=df.PADY,
        )


