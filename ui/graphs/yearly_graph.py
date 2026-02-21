import re
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import infrastructure.config.defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class YearlyGraph(ctk.CTkFrame):

    state_key  ="graphs.yearly"

    MONTH_NAMES = ["enero","febrero","marzo", "abril","mayo", "junio", "julio","agosto", "sep", "oct", "nov", "dic"]
    events = {"habit_changed", "graph_changed", "day_changed"}

    def __init__(self, master, style_settings):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)

        self.theme_colors = style_settings["colors"]
        self.fonts = style_settings["fonts"]
        self.font = style_settings["current_font"]

        self.canvas_grafica = None
        self.fig = None
        self.ax = None

        self._build_base()


    def _build_base(self):
        plt.rcParams["font.family"] = self.font
        self.fig, self.ax = plt.subplots(dpi=100)

        self.canvas_grafica = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_grafica.get_tk_widget().pack(
            fill="both", expand=True, padx=df.PADX, pady=df.PADY
        )


    def refresh(self, yearly_data):
        monthly_performance = yearly_data["monthly_performance"]

        self._render(monthly_performance)


    def gray_to_hex(self, color_str):
        """
        Convierte 'grayNN' o 'greyNN' a '#RRGGBB'.
        Si ya es un hex válido, lo devuelve igual.
        """
        color_str = color_str.strip().lower()
        # Detecta gray o grey seguido de un número
        match = re.match(r"(gray|grey)(\d{1,3})", color_str)
        if match:
            porcentaje = int(match.group(2))
            porcentaje = max(0, min(100, porcentaje))  # limitar 0-100
            valor = round(porcentaje * 255 / 100)
            return "#{0:02x}{0:02x}{0:02x}".format(valor)
        # Si ya es hexadecimal
        if color_str.startswith("#"):
            return color_str
        raise ValueError(f"Color desconocido: {color_str}")



    def _render(self, month_performance):

        self.ax.clear()

        # Fondo
        bg_color = self.theme_colors["frame"][1]
        if "#" not in bg_color:
            bg_color = self.gray_to_hex(bg_color)

        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)

        # Datos
        x = self.MONTH_NAMES
        y = month_performance

        self.ax.bar(x, y, color=self.theme_colors["button"], width=0.6)

        # Título
        self.ax.set_title(
            "Rendimiento mensual/año",
            fontsize=25,
            color="white",
            pad=15,
        )

        self.ax.tick_params(left=False, bottom=False)
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(x, color="white", fontsize=18)
        self.ax.set_yticks(range(10, 101, 10))
        self.ax.set_yticklabels(
            [f"{i}%" for i in range(10, 101, 10)],
            color="white",
            fontsize=18,
        )

        for spine in ["top", "right", "bottom", "left"]:
            self.ax.spines[spine].set_visible(False)

        x_max = len(x) - 0.3
        y_max = 110
        self.ax.set_xlim(-0.5, x_max)
        self.ax.set_ylim(-5, y_max)

        self.ax.annotate(
            "",
            xy=(x_max, 0),
            xytext=(-0.85, 0),
            arrowprops=dict(arrowstyle="->", linewidth=3.5, color="white"),
        )

        self.ax.annotate(
            "",
            xy=(-0.5, y_max),
            xytext=(-0.5, -5),
            arrowprops=dict(arrowstyle="->", linewidth=3.5, color="white"),
        )

        self.ax.text(x_max, -7, "Mes", ha="left", va="top", color="white", fontsize=18)
        self.ax.text(-0.8, y_max, "(%)", ha="right", va="bottom", color="white", fontsize=18)

        self.ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)

        self.fig.subplots_adjust(left=0.07, right=0.96, top=0.90, bottom=0.12)

        self.canvas_grafica.draw()
