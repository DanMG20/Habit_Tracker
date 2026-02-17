import re
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import infrastructure.config.defaults as df

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class MonthlyGraph(ctk.CTkFrame):

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

    def refresh(self, view_state):
        monthly_data = view_state["graphs"]["monthly"]

        month_range = monthly_data["month_range"]
        rendimiento_datos = monthly_data["daily_performance"]

        self._render(month_range, rendimiento_datos)
        
    def refresh_metrics(self):
        self.rango_dias_mes = self.get_month_range()
        self.rendimiento_datos = self.get_daily_performance_per_month()


    def create_graph(self):
        logger.warning("Remove later")
        """
        Crea una gráfica de barras en un frame de CustomTkinter.
        Estirada al máximo con márgenes ajustados.
        Los ejes se dibujan como flechas con ticks.
        """
        self.refresh_metrics()
        # Limpiar frame sin destruirlo
        for widget in self.winfo_children():
            widget.destroy()

        # Si existe canvas previo, eliminarlo
        if hasattr(self, "canvas_grafica") and self.canvas_grafica:
            self.canvas_grafica.get_tk_widget().destroy()
            plt.close(self.canvas_grafica.figure)
            self.canvas_grafica = None
        # Crear figura y ejes
        plt.rcParams["font.family"] = self.font
        fig, ax = plt.subplots(dpi=100)
        if "#" in self.theme_colors["frame"][1]:
            fig.patch.set_facecolor(self.theme_colors["frame"][1])
            ax.set_facecolor(self.theme_colors["frame"][1])
        else:
            color_convertido = self.gray_to_hex(self.theme_colors["frame"][1])
            fig.patch.set_facecolor(color_convertido)
            ax.set_facecolor(color_convertido)

        # Datos
        x = list(range(1, self.rango_dias_mes + 1))
        y = [self.rendimiento_datos.get(d, 0) for d in x]

        ax.bar(x, y, color=self.theme_colors["button"], width=0.6)

        # Configuración del título
        ax.set_title(
            "Rendimiento diario en el mes (%)", fontsize=25, color="white", pad=15
        )

        # Configuración de ticks (tamaño original)
        ax.tick_params(left=False, bottom=False)
        ax.set_xticks(x)
        ax.set_xticklabels(x, color="white", fontsize=18)
        ax.set_yticks(range(0, 101, 10))
        ax.set_yticklabels(
            [f"{i}%" for i in range(0, 101, 10)], color="white", fontsize=18
        )
        ax.yaxis.set_tick_params(pad=17)

        # Quitar spines y ticks automáticos
        for spine in ["top", "right", "bottom", "left"]:
            ax.spines[spine].set_visible(False)

        # Límites para que siempre se vea la flecha completa
        x_max = max(x) + 0.8
        y_max = 110
        ax.set_xlim(-0.5, x_max)
        ax.set_ylim(-5, y_max)

        # Dibujar flechas de ejes
        ax.annotate(
            "",
            xy=(x_max, 0),
            xytext=(-1, 0),
            arrowprops=dict(arrowstyle="->", linewidth=3.5, color="white"),
        )

        ax.annotate(
            "",
            xy=(0, y_max),
            xytext=(0, -5),
            arrowprops=dict(arrowstyle="->", linewidth=3.5, color="white"),
        )
        # Etiquetas de los ejes
        ax.text(x_max, -7, "Días", ha="left", va="top", color="white", fontsize=18)
        ax.text(-1, y_max, "(%)", ha="right", va="bottom", color="white", fontsize=18)

        # Cuadrícula opcional
        ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)

        # Ajustar márgenes
        fig.subplots_adjust(left=0.06, right=0.96, top=0.90, bottom=0.12)

        # Crear nuevo canvas y guardarlo en self
        self.canvas_grafica = FigureCanvasTkAgg(fig, master=self)
        self.canvas_grafica.draw()
        self.canvas_grafica.get_tk_widget().pack(
            fill="both", expand=True, padx=df.PADX, pady=df.PADY
        )




    def _render(self, rango_dias_mes, rendimiento_datos):

        self.ax.clear()

        # Fondo
        bg_color = self.theme_colors["frame"][1]
        if "#" not in bg_color:
            bg_color = self.gray_to_hex(bg_color)

        self.fig.patch.set_facecolor(bg_color)
        self.ax.set_facecolor(bg_color)

        # Datos
        x = list(range(1, rango_dias_mes + 1))
        y = [rendimiento_datos.get(d, 0) for d in x]

        self.ax.bar(x, y, color=self.theme_colors["button"], width=0.6)

        # Título
        self.ax.set_title(
            "Rendimiento diario en el mes (%)",
            fontsize=25,
            color="white",
            pad=15,
        )

        # Configuración visual
        self.ax.tick_params(left=False, bottom=False)
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(x, color="white", fontsize=18)
        self.ax.set_yticks(range(0, 101, 10))
        self.ax.set_yticklabels(
            [f"{i}%" for i in range(0, 101, 10)],
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




















 
