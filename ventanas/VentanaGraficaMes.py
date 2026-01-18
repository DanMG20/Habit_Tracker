import customtkinter as ctk 
import infrastructure.config.defaults as df
from domain.style_service import StyleService
import matplotlib.pyplot as plt
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class VentanaGraficaMes():
    def __init__(self, master,
                 controller,
                 frames_ventana_principal,
                 objeto_grafica_anio
                 ):
        self.master = master
        self.controller = controller
        self.load_style_settings()
        self.frames_vent_principal = frames_ventana_principal
        self.objeto_grafica_anio = objeto_grafica_anio

    def load_style_settings(self):
        style_service = StyleService()
        self.theme_colors=style_service._load_theme_colors()
        self.fonts = style_service.build_fonts()
        self.font = style_service.get_font()
    def inicializar_frames_graf_mensual(self):
        self.crear_frame_botones_navegacion()
        self.crear_frame_grafica()


    def calcular_variables(self):
        self.rango_dias_mes =self.controller.get_month_days_range()
        self.rendimiento_datos = self.controller.get_daily_performance_in_month()


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
        self.frame_grafica_mensual = ctk.CTkFrame(self.master)
        self.frame_grafica_mensual.grid(
            row=3,
            column=0,
            columnspan =3,
            sticky="nsew",
            rowspan = 3, 
            padx= df.PADX,
            pady= df.PADY
        )
        self.crear_grafica()
        
    def crear_frame_botones_navegacion(self): 
        self.frame_botones_navegacion = ctk.CTkFrame(self.master)
        self.frame_botones_navegacion.grid(
            row= 2, 
            column = 0, 
            sticky ="nsew",
            padx= df.PADX, 
            pady =df.PADY
            )
        #configurar frame 
        self.frame_botones_navegacion.rowconfigure(0, weight=1)
        for column in range (2):
            self.frame_botones_navegacion.columnconfigure (column, weight=1)
        #Boton ventana principal 
        self.boton_ventana_principal = ctk.CTkButton(
            self.frame_botones_navegacion,
            command=self.evento_regresar_ventana_principal,
            text ="Ventana principal", 
            font=self.fonts["SUBTITLE"])
        self.boton_ventana_principal.grid(
            row=0, 
            column = 0, 
            sticky ="nsew",
            padx= df.PADX, 
            pady =df.PADY
           )
        #Boton ventana rend
        self.boton_ventana_rendimiento = ctk.CTkButton(
            self.frame_botones_navegacion,
            text = "Rendimiento Anual",
            command= self.evento_grafica_anual,
            font=self.fonts["SUBTITLE"])
        self.boton_ventana_rendimiento.grid(
            row=0, 
            column = 1, 
            sticky ="nsew",
            padx= df.PADX, 
            pady =df.PADY
            )
    def crear_grafica(self):
        #control 
        print("CREANDO GRAFICA_MENSUAL")


        """
        Crea una gráfica de barras en un frame de CustomTkinter.
        Estirada al máximo con márgenes ajustados.
        Los ejes se dibujan como flechas con ticks.
        """
        self.calcular_variables()
        # Limpiar frame sin destruirlo
        for widget in self.frame_grafica_mensual.winfo_children():
            widget.destroy()

        # Si existe canvas previo, eliminarlo
        if hasattr(self, "canvas_grafica") and self.canvas_grafica:
            self.canvas_grafica.get_tk_widget().destroy()
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
        ax.set_title("Rendimiento diario en el mes (%)", fontsize=25, color="white", pad=15)

        # Configuración de ticks (tamaño original)
        ax.tick_params(left=False, bottom=False)
        ax.set_xticks(x)
        ax.set_xticklabels(x, color="white", fontsize=18)
        ax.set_yticks(range(0, 101, 10))
        ax.set_yticklabels([f"{i}%" for i in range(0, 101, 10)], color="white", fontsize=18)
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
        ax.annotate("", xy=(x_max, 0), xytext=(-1, 0),
            arrowprops=dict(arrowstyle="->", linewidth=3.5, color='white'))

        ax.annotate("", xy=(0, y_max), xytext=(0, -5),
                    arrowprops=dict(arrowstyle="->", linewidth=3.5, color='white'))
        # Etiquetas de los ejes
        ax.text(x_max, -7, "Días", ha='left', va='top', color='white', fontsize=18)
        ax.text(-1, y_max, "(%)", ha='right', va='bottom', color='white', fontsize=18)

        # Cuadrícula opcional
        ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)

        # Ajustar márgenes
        fig.subplots_adjust(
            left=0.06,
            right=0.96,
            top=0.90,
            bottom=0.12
        )

        # Crear nuevo canvas y guardarlo en self
        self.canvas_grafica = FigureCanvasTkAgg(fig, master=self.frame_grafica_mensual)
        self.canvas_grafica.draw()
        self.canvas_grafica.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=df.PADX,
            pady=df.PADY
        )

    def evento_regresar_ventana_principal(self):
        self.master.label_f_control.configure(text=self.master.headers[1])
        
        #Configura la barra con el rendimiento mensual 
        self.master.barra_rendimiento.set(self.master.rendimiento_semanal/100)
        self.master.label_rendimiento.configure( text =f"{self.master.rendimiento_semanal}%")
        self.master.configurar_controles_semanales()

        # Limpiar frame sin destruirlo
        if hasattr(self, "frame_grafica_mensual") and self.frame_grafica_mensual:
            print("LIMPIAR FRAME MENSUAL")
            for widget in self.frame_grafica_mensual.winfo_children():
                widget.destroy()
        
            self.frame_grafica_mensual.grid_forget()


        if hasattr(self.objeto_grafica_anio, "frame_grafica_anual") and self.objeto_grafica_anio.frame_grafica_anual:
            print("LIMPIAR FRAME ANUAL")
            for widget in self.objeto_grafica_anio.frame_grafica_anual.winfo_children():
                widget.destroy()
        
            self.objeto_grafica_anio.frame_grafica_anual.grid_forget()
        
        
        # Levantar frames fecha
       
        self.frames_vent_principal[0].tkraise() 


    def evento_grafica_anual(self):
        if hasattr(self, "frame_grafica_mensual") and self.frame_grafica_mensual:
            print("EVENTO GRAFICA MENSUAL ; LIMPIANDO GRAFICA MENSUAL")
            for widget in self.frame_grafica_mensual.winfo_children():
                widget.destroy()
        
            self.frame_grafica_mensual.grid_forget()


        if hasattr(self.objeto_grafica_anio, "frame_grafica_anual") and self.objeto_grafica_anio.frame_grafica_anual:
            print("EVENTO GRAFICA ANUAL ; LIMPIANDO GRAFICA ANUAL")
            for widget in self.objeto_grafica_anio.frame_grafica_anual.winfo_children():
                widget.destroy()
        
            self.objeto_grafica_anio.frame_grafica_anual.grid_forget()
        
        self.boton_ventana_rendimiento.configure(text="Rendimiento Mensual",
                                                 command= self.master.evento_grafica_mensual)
        #Configurar botones para cambiar entre meses 
        
        self.master.configurar_controles_año()
        #Cambia el encabezado del frame control
        
        self.master.label_f_control.configure(text=self.controller.get_year_header())
        #Calcula el rendimiento que ira en la barra 
        
        rend_anual = self.controller.get_yearly_performance()
        
        #Configura la barra con el rendimiento mensual 
        
        self.master.barra_rendimiento.set(rend_anual[1]/100)
        
        self.master.label_rendimiento.configure(text =f"{rend_anual[1]}%")
        
        # configurar boton para regresar a grafica mensual
      
        # Muestra el frame de la grafica mensual
        self.master.frames_ventana_grafica_anio()
        
        #self.obj_ventana_grafica_mes.frame_botones_navegacion.tkraise()


    def evento_grafica_mensual(self):
        if hasattr(self, "frame_grafica_mensual") and self.frame_grafica_mensual:
            print("EVENTO GRAFICA MENSUAL ; LIMPIANDO GRAFICA MENSUAL")
            for widget in self.frame_grafica_mensual.winfo_children():
                widget.destroy()
        
            self.frame_grafica_mensual.grid_forget()


        if hasattr(self.objeto_grafica_anio, "frame_grafica_anual") and self.objeto_grafica_anio.frame_grafica_anual:
            for widget in self.objeto_grafica_anio.frame_grafica_anual.winfo_children():
                widget.destroy()
        
            self.objeto_grafica_anio.frame_grafica_anual.grid_forget()


            #Configurar botones para cambiar entre meses 
        self.master.configurar_controles_mes()
        #Cambia el encabezado del frame control
        self.master.label_f_control.configure(text=self.fechas_objeto.encabezado_mes())
        #Calcula el rendimiento que ira en la barra 
        self.master.promedio_mes = self.fechas_objeto.calcular_rend_mes()
        #Configura la barra con el rendimiento mensual 
        self.master.barra_rendimiento.set(self.promedio_mes/100)
        self.master.label_rendimiento.configure(text =f"{self.promedio_mes}%")
        # Muestra el frame de la grafica mensual
        self.frame_grafica_mensual.grid(
            row=3,
            column=0,
            columnspan =3,
            sticky="nsew",
            rowspan = 3, 
            padx= df.PADX,
            pady= df.PADY
       )
        self.frame_botones_navegacion.tkraise()
        
        self.boton_ventana_rendimiento.configure(text="Rendimiento Anual",
                                                 command= self.master.evento_grafica_mensual)
