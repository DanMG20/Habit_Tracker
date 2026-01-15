import customtkinter as ctk 
import styles as styles
import matplotlib.pyplot as plt
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class VentanaGraficaAnio():
    def __init__(self, master,frames_ventana_principal,db_objeto,fecha_objeto):
        self.master = master
        self.frames_vent_principal = frames_ventana_principal
        self.db_objeto = db_objeto
        self.fecha_objeto = fecha_objeto
    
    
    def abrir_frames(self): 
        self.calcular_variables()
        self.crear_frame_grafica()

    def calcular_variables(self):
        self.meses =self.fecha_objeto.nombres_meses()
        self.rendimiento_meses = self.fecha_objeto.rendimiento_meses_anio()[0]
        self.rendimiento_anual = self.fecha_objeto.rendimiento_meses_anio()[1]

    def gray_to_hex(self,color_str):
        """
        Convierte 'grayNN' o 'greyNN' a '#RRGGBB'.
        Si ya es un hex válido, lo devuelve igual.
        """
        color_str = color_str.strip().lower()
        # Detecta gray o grey seguido de un número
        match = re.match(r'(gray|grey)(\d{1,3})', color_str)
        if match:
            porcentaje = int(match.group(2))
            porcentaje = max(0, min(100, porcentaje))  # limitar 0-100
            valor = round(porcentaje * 255 / 100)
            return '#{0:02x}{0:02x}{0:02x}'.format(valor)
        # Si ya es hexadecimal
        if color_str.startswith('#'):
            return color_str
        raise ValueError(f"Color desconocido: {color_str}")

    def crear_frame_grafica(self): 
        self.frame_grafica_anual = ctk.CTkFrame(self.master)
        self.frame_grafica_anual.grid(
            row=3,
            column=0,
            columnspan =3,
            sticky="nsew",
            rowspan = 3, 
            padx= styles.PADX,
            pady= styles.PADY
        )
        self.crear_grafica()
        
    def crear_grafica(self):
        
        """
        Crea una gráfica de barras en un frame de CustomTkinter.
        Estirada al máximo con márgenes ajustados.
        Los ejes se dibujan como flechas con ticks.
        """
        self.calcular_variables()
        # Limpiar frame sin destruirlo
        for widget in self.frame_grafica_anual.winfo_children():
            widget.destroy()

        # Si existe canvas previo, eliminarlo
        if hasattr(self, "canvas_grafica") and self.canvas_grafica:
            self.canvas_grafica.get_tk_widget().destroy()
            self.canvas_grafica = None
            
        # Crear figura y ejes
        plt.rcParams["font.family"] = styles.FUENTE_PRINCIPAL
        fig, ax = plt.subplots(dpi=100)
        if "#" in styles.tema_frame_color[1]:
            fig.patch.set_facecolor(styles.tema_frame_color[1])
            ax.set_facecolor(styles.tema_frame_color[1])
        else: 
            color_convertido = self.gray_to_hex(styles.tema_frame_color[1])
            fig.patch.set_facecolor(color_convertido)
            ax.set_facecolor(color_convertido)

        # Datos
        x = self.meses
        y = self.rendimiento_meses

        ax.bar(x, y, color=styles.tema_botones_color, width=0.6)

        # Configuración del título
        ax.set_title("Rendimiento mensual en el año (%)", fontsize=25, color="white", pad=15)

        # Configuración de ticks (tamaño original)
        ax.tick_params(left=False, bottom=False)
        ax.set_xticks(x)
        ax.set_xticklabels(x, color="white", fontsize=18)
        ax.set_yticks(range(0, 101, 10))
        ax.set_yticklabels([f"{i}%" for i in range(0, 101, 10)], color="white", fontsize=18)
        ax.yaxis.set_tick_params(pad=35)
        # Quitar spines y ticks automáticos
        for spine in ["top", "right", "bottom", "left"]:
            ax.spines[spine].set_visible(False)

        # Límites para que siempre se vea la flecha completa
        x_max = len(x) -0.3
        y_max = 110
        ax.set_xlim(-0.5, x_max)
        ax.set_ylim(-5, y_max)

        # Dibujar flechas de ejes
        # Dibujar flechas de ejes (ajustadas para que Y no se encime en "Enero")
        ax.annotate("", xy=(x_max, 0), xytext=(-0.85, 0),
                    arrowprops=dict(arrowstyle="->", linewidth=3.5, color='white'))

        ax.annotate("", xy=(-0.5, y_max), xytext=(-0.5, -5),
                    arrowprops=dict(arrowstyle="->", linewidth=3.5, color='white'))

        # Etiquetas de los ejes
        ax.text(x_max, -7, "Mes", ha='left', va='top', color='white', fontsize=18)
        ax.text(-0.8, y_max, "(%)", ha='right', va='bottom', color='white', fontsize=18)

        # Cuadrícula opcional
        ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)

        # Ajustar márgenes
        fig.subplots_adjust(
            left=0.07,
            right=0.96,
            top=0.90,
            bottom=0.12
        )

        # Crear nuevo canvas y guardarlo en self
        self.canvas_grafica = FigureCanvasTkAgg(fig, master=self.frame_grafica_anual)
        self.canvas_grafica.draw()
        self.canvas_grafica.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=styles.PADX,
            pady=styles.PADY
        )


    
