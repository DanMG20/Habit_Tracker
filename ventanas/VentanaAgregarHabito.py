import customtkinter as ctk 
import infrastructure.config.defaults as df
from domain.style_service import StyleService
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

class VentanaAgregarHabito:
    def __init__(self, controller,master,frames_ventana_principal):
        self.master = master
        self.controller = controller
        self.db_objeto = self.controller.db
        logger.warning("Using temporary bridge self.db_object")
        self.load_style_settings()
        self.default_text_entry  = "Levantarse Temprano, Regar las plantas, etc..."
        self.default_textbox = "Levantarse Temprano (A las 7 AM)..."
        self.frames_vent_principal = frames_ventana_principal
        #--------------------------------------------VARIABLES-------------------------------------------
        self.ALTURA_FRAME_RELLENO = 200
        self.var_seleccionar_todos = ctk.BooleanVar(value=False)
        self.inicializar_frames_agregar_habito()
        #------------------------------------------LISTA FRAMES -------------------------------------------
        self.frames_agregar_habito = [self.frame_derecho,
                                      self.frame_izq_agregar_hab,
                                      self.frame_nombre_ventana_1_0,
                                      ]
        
    def load_style_settings(self):
        style_service = StyleService()
        self.theme_colors=style_service._load_theme_colors()
        self.fonts = style_service.build_fonts()

    def inicializar_frames_agregar_habito(self):
            self.nombre_ventana_frame_1_0()
            self.crear_frame_izquierdo()
            self.crear_frame_derecho()
            self.crear_frame_botones_navegacion()

    def crear_frame_derecho(self): 
        self.frame_derecho = ctk.CTkFrame(self.master, corner_radius=df.CORNER_RADIUS)
        self.frame_derecho.grid(row = 3,
                                column=1,
                                columnspan =2,
                                rowspan = 3,
                                sticky="nsew",
                                padx= df.PADX,
                                pady = df.PADY)
        self.frame_derecho.columnconfigure(0, weight=1)
        self.frame_derecho.rowconfigure(0, weight=1)
        self.crear_frame_semana()
        self.crear_frame_botones_navegacion()
        self.crear_frame_relleno_der()
          
    def crear_frame_relleno_der(self):
        self.frame_relleno_der = ctk.CTkFrame(
            self.frame_derecho,
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"],
            height = self.ALTURA_FRAME_RELLENO)
        self.frame_relleno_der.grid(row = 2,
                                column=0,
                                sticky="nsew",
                                padx= df.PADX,
                                pady = df.PADY)

    def nombre_ventana_frame_1_0(self):
        self.frame_nombre_ventana_1_0 = ctk.CTkFrame(
            self.master, 
            corner_radius=df.CORNER_RADIUS)
        self.frame_nombre_ventana_1_0.grid(row=2,
                                           column=0,
                                           columnspan=3,
                                           sticky="nsew",
                                           padx=df.PADX,
                                           pady=df.PADY)
        label_nombre_ventana = ctk.CTkLabel(
            self.frame_nombre_ventana_1_0, 
            text="AGREGAR HÁBITO",
            font=self.fonts["SUBTITLE"],
            anchor="center")
        label_nombre_ventana.pack(
            fill="both",
            expand=True,
            padx=df.PADX, 
            pady=df.PADY)

    def crear_frame_izquierdo(self):
        self.frame_izq_agregar_hab = ctk.CTkFrame(self.master)
        self.frame_izq_agregar_hab.grid(
            column=0, 
            row=3, 
            rowspan=3,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY)
        self.nombre_habito()
        self.color_habito()
        self.configurar_frame_izquierdo()
        frame_relleno_izq = ctk.CTkFrame(
            self.frame_izq_agregar_hab,
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"],
            height = self.ALTURA_FRAME_RELLENO)
        frame_relleno_izq.grid(row = 4,
                                column=0,
                                sticky="nsew",
                                padx= df.PADX,
                                pady = df.PADY)

    def configurar_frame_izquierdo(self): 
        self.frame_izq_agregar_hab.columnconfigure(0, weight=1)
        for fila in range(4):
            self.frame_izq_agregar_hab.rowconfigure(fila, weight=1)

    def configurar_frame_semana(self):
        self.frame_selec_semana.columnconfigure(0, weight=1)
        self.frame_selec_semana.columnconfigure(1, weight=1)
        for fila in range(5):
            self.frame_selec_semana.rowconfigure(fila, weight=1)

    def nombre_habito(self): 
        label_nombre = ctk.CTkLabel(self.frame_izq_agregar_hab, 
                                    text="INGRESA EL NOMBRE DE TU NUEVO HÁBITO",
                                    font=self.fonts["SMALL"],
                                    )
        label_nombre.grid(column=0, row=0, sticky="nsew", padx=df.PADX, pady=df.PADY)
        self.entry_nombre = ctk.CTkEntry(self.frame_izq_agregar_hab,
                                    font=self.fonts["SMALL"],
                                    )
        self.entry_nombre.grid(column=0, row=1, sticky="nsew", padx=df.PADX, pady=df.PADY)
        self.entry_nombre.insert(0, self.default_text_entry)
        self.entry_nombre.configure(text_color='gray')
        self.entry_nombre.bind("<FocusIn>",self.on_entry_click) 
        self.entry_nombre.bind("<FocusOut>", self.on_focusout_entry)

    def color_habito(self): 
        label_nombre = ctk.CTkLabel(
            self.frame_izq_agregar_hab, 
            text="ELIGE EL COLOR DE TU NUEVO HÁBITO",
            font=self.fonts["SMALL"],
        )
        label_nombre.grid(column=0, row=2, sticky="nsew", padx=df.PADX, pady=df.PADY)

        frame_colores = ctk.CTkFrame(self.frame_izq_agregar_hab)
        frame_colores.grid(column=0, row=3, sticky="nsew", padx=df.PADX, pady=df.PADY)

        self.btn_colores_estado = {}   # {color: boton}
        self.color_seleccionado = None

        for color in df.COLORES:
            boton_color = ctk.CTkButton(
                frame_colores,
                fg_color=color,
                width=60,
                height=60,
                text=""
            )
            boton_color.pack(side="left", expand=True, padx=5)

            # Guardar botón en el diccionario
            self.btn_colores_estado[color] = boton_color

            # Comando con lambda que captura color
            boton_color.configure(command=lambda c=color: self.evento_btn_color(c))

        # Seleccionar por defecto el gris si existe en estilos.COLORES
        if df.COLORES[0] in self.btn_colores_estado:
            self.evento_btn_color(df.COLORES[0])

    def crear_frame_semana(self): 
        self.frame_selec_semana = ctk.CTkFrame(self.frame_derecho)
        self.frame_selec_semana.grid(column=0, row=0, sticky="nsew",
                                    padx=df.PADX, pady=df.PADY)
        self.dias_repeticion()
        self.agregar_descripcion()
        self.configurar_frame_semana()

    def dias_repeticion(self):
        label_semana = ctk.CTkLabel(self.frame_selec_semana, 
                                    text="DIAS DE LA SEMANA",
                                    font=self.fonts["SMALL"],
                                    )
        label_semana.grid(column=0,columnspan =2, row=0, sticky="nsew", padx=df.PADX, pady=df.PADY)
        boton_seleccionar_todos = ctk.CTkCheckBox(self.frame_selec_semana, 
                                                  text="SELECCIONAR TODOS",
                                                  variable=self.var_seleccionar_todos,
                                                  command=self.evento_btn_selec_todos,
                                                  font=self.fonts["SMALL"])
        boton_seleccionar_todos.grid(column=1, row=2, sticky="e", padx=40, pady=df.PADY)

        self.frame_dias_semana = ctk.CTkFrame(self.frame_selec_semana)
        self.frame_dias_semana.grid(column=0,columnspan=2 ,row=1, sticky="nsew", padx=df.PADX, pady=df.PADY)
        self.crear_botones_semana()

    def agregar_descripcion(self):
        label_descripcion = ctk.CTkLabel(self.frame_selec_semana, 
                                    text="AGREGA UNA BREVE DESCRIPCION DE TU HÁBITO",
                                    font=self.fonts["SMALL"],
                                    )
        label_descripcion.grid(column=0,columnspan =2, row=3, sticky="nsew", padx=df.PADX, pady=df.PADY)
        self.cuadro_texto_descripcion = ctk.CTkTextbox(self.frame_selec_semana, 
                                    height=100,
                                    font=self.fonts["SMALL"],
                                    border_width=2,
                                    )
        self.cuadro_texto_descripcion.insert("0.0", self.default_textbox)
        self.cuadro_texto_descripcion.configure(text_color='gray')
        self.cuadro_texto_descripcion.bind("<FocusIn>",self.on_textbox_click) 
        self.cuadro_texto_descripcion.bind("<FocusOut>", self.on_focusout_textbox)
        self.cuadro_texto_descripcion.grid(column=0,columnspan =2, row=4, sticky="nsew", padx=df.PADX, pady=df.PADY)

    def crear_botones_semana(self):
        # claves únicas: (clave, etiqueta)
        dias = [("D","D"), ("L","L"), ("Ma","M"), ("Mi","M"), ("J","J"), ("V","V"), ("S","S")]

        self.botones_semana = {}           # {clave: boton}
        self.estado_botones_semana = {}    # {clave: bool}

        for clave, texto in dias:
            boton = ctk.CTkButton(
                self.frame_dias_semana,
                #fg_color=estilos.COLORES[0],
                font=self.fonts["SMALL"],
                width=60,
                height=60,
                text=texto
            )
            boton.pack(side="left", padx=13, expand=True)

            # estado inicial
            boton.selected = False
            self.botones_semana[clave] = boton
            self.estado_botones_semana[clave] = False
        
            # comando seguro que captura boton y clave en el momento de creación
            boton.configure(command=lambda b=boton, k=clave: self.evento_btn_semana(b, k))
     
    def crear_frame_botones_navegacion(self): 
        self.frame_botones_navegacion = ctk.CTkFrame(
            self.frame_derecho,
            #fg_color=estilos.tema_frame_color
            )
        self.frame_botones_navegacion.grid(column=0, row=1, sticky="nsew",
                                     padx=df.PADX, pady=df.PADY)
        
        for columna in range(2):
            self.frame_botones_navegacion.columnconfigure(columna, weight=1)
        boton_cancelar = ctk.CTkButton(self.frame_botones_navegacion,
                                       text="CANCELAR",
                                       command=self.evento_btn_cancelar,
                                       #fg_color=estilos.COLOR_CONTRASTE,
                                       font=self.fonts["SUBTITLE"])
        boton_cancelar.grid(column=0, row=0, sticky="nsew", padx=df.PADX, pady=df.PADY)
        boton_agregar_habito = ctk.CTkButton(self.frame_botones_navegacion,
                                            text="AGREGAR HABITO",
                                            #fg_color=estilos.COLOR_CONTRASTE,
                                            command=self.evento_btn_crear_habito,
                                            font=self.fonts["SUBTITLE"])
        boton_agregar_habito.grid(column=1, row=0, sticky="nsew", padx=df.PADX, pady=df.PADY)
        
#----------------------------------------------------EVENTOS-------------------------------------------------------------------------
    def cambiar_foco(self):
        self.master.focus_set()

    def evento_btn_cancelar(self):
        self.frame_nombre_ventana_1_0.grid_forget()
        self.frame_derecho.grid_forget()
        self.cambiar_foco()
        for frame in self.frames_vent_principal: 
            frame.tkraise()

    def evento_btn_semana(self, boton, clave):
        # alternar estado
        boton.selected = not boton.selected
        self.estado_botones_semana[clave] = boton.selected

        if boton.selected:
            boton.configure(border_width=4, border_color=df.COLOR_BORDE)
        else:
            boton.configure(border_width=0)  # 0 para quitar borde

    def evento_btn_selec_todos(self):
        seleccionar = self.var_seleccionar_todos.get()  # True/False
        for clave, boton in self.botones_semana.items():
            boton.selected = seleccionar
            self.estado_botones_semana[clave] = seleccionar
            if seleccionar:
                boton.configure(border_width=4, border_color=df.COLOR_BORDE)
            else:
                boton.configure(border_width=0)

    def evento_btn_color(self, color):
        # Desmarcar todos
        for c, boton in self.btn_colores_estado.items():
            boton.configure(border_width=0)

        # Marcar solo el seleccionado
        boton_seleccionado = self.btn_colores_estado[color]
        boton_seleccionado.configure(border_width=4, border_color=df.COLOR_BORDE)

        # Guardar en la variable actual
        self.color_seleccionado = color

    def evento_habito_sin_ejecuciones(self):
        label_error = ctk.CTkLabel(self.frame_selec_semana, 
                                                  text="Debes elegir al menos un día para ejecutar el hábito*",
                                                  text_color="red",
                                                  font=self.fonts["SMALL"])
        label_error.grid(column=0, row=2, sticky="w", padx=40, pady=df.PADY)

    def evento_btn_crear_habito(self):
        valores = list(self.estado_botones_semana.values())
        if not True in valores:
            self.evento_habito_sin_ejecuciones()
        else:
            #obtener descripcion
            descripcion = self.cuadro_texto_descripcion.get("0.0","end-1c")
            #crear el habito en base de datos
            self.db_objeto.crear_habito(self.entry_nombre.get(), valores,self.color_seleccionado,descripcion)
            self.entry_nombre.delete(0,"end")
            self.evento_btn_cancelar()
            self.master.actualizacion_agregar_habito()
            self.master.obj_eliminar_habito.listar_habitos()
            self.master.listar_habitos_ayer()
            
    def on_entry_click(self,event):
        if self.entry_nombre.get() == self.default_text_entry :
            self.entry_nombre.delete(0, 'end')
            self.entry_nombre.configure(text_color='white')
            

    def on_focusout_entry(self,event):
        if self.entry_nombre.get() == '':
            self.entry_nombre.insert(0, self.default_text_entry )
            self.entry_nombre.configure(text_color='gray')


    def on_textbox_click(self, event):
        # Quitar el salto de línea extra con strip()
        if self.cuadro_texto_descripcion.get("0.0", 'end').strip() == self.default_textbox:
            self.cuadro_texto_descripcion.delete("0.0", 'end')
            self.cuadro_texto_descripcion.configure(text_color='white')

    def on_focusout_textbox(self, event):
        # Revisar si está vacío (después de quitar espacios y saltos)
        if self.cuadro_texto_descripcion.get("0.0", 'end').strip() == '':
            self.cuadro_texto_descripcion.insert("0.0", self.default_textbox)
            self.cuadro_texto_descripcion.configure(text_color='gray')