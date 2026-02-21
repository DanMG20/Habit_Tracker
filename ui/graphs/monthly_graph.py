import re
import numpy as np
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import infrastructure.config.defaults as df

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class MonthlyGraph(ctk.CTkFrame):
    state_key  ="graphs.monthly"

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

    def _build_base(self):
        plt.rcParams["font.family"] = self.font
        self.fig, self.ax = plt.subplots(dpi=100)

        self.canvas_grafica = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_grafica.get_tk_widget().pack(
            fill="both", expand=True, padx=df.PADX, pady=df.PADY
        )

    def refresh(self, monthly_data):
        month_range = monthly_data["month_range"]
        rendimiento_datos = monthly_data["daily_performance"]
        year = monthly_data["year"]

        self._render(month_range, rendimiento_datos, year)
        
    def refresh_metrics(self):
        self.rango_dias_mes = self.get_month_range()
        self.rendimiento_datos = self.get_daily_performance_per_month()


    def _render(self, rango_dias_mes, rendimiento_datos, year):
        self.ax.clear()
        # Fondo
        bg_color = self.theme_colors["frame"][1]
        line_color =self.theme_colors["button"][1]
        if "#" not in bg_color:
            bg_color = self.gray_to_hex(bg_color)

        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)

        # Datos

        x = list(range(1, rango_dias_mes + 1))
        y_raw = [rendimiento_datos.get(d) for d in x]

        y = [np.nan if v is None else v for v in y_raw]
        
        self.ax.plot(
            x,
            y,
            color=line_color,
            linewidth=3,

        )
        self.ax.fill_between(
            x,
            y,
            0,
            where=~np.isnan(y),
            color=line_color,
            alpha=0.25,
        )
        # Título
        self.ax.set_title(
            f"Rendimiento diario/mes — ({year}) ",
            fontsize=25,
            color="white",
            pad=15,
        )

        # Configuración visual
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

        x_max = max(x) + 0.8
        y_max = 110
        self.ax.set_xlim(-0.5, x_max)
        self.ax.set_ylim(-5, y_max)

        self.ax.annotate(
            "",
            xy=(x_max, 0),
            xytext=(-1, 0),
            arrowprops=dict(arrowstyle="->", linewidth=3.5, color="white"),
        )

        self.ax.annotate(
            "",
            xy=(0, y_max),
            xytext=(0, -5),
            arrowprops=dict(arrowstyle="->", linewidth=3.5, color="white"),
        )

        self.ax.text(x_max, -7, "Días", ha="left", va="top", color="white", fontsize=18)
        self.ax.text(-1, y_max, "(%)", ha="right", va="bottom", color="white", fontsize=18)

        self.ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)

        self.fig.subplots_adjust(left=0.06, right=0.96, top=0.90, bottom=0.12)

        self.canvas_grafica.draw()




















 
