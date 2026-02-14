import customtkinter as ctk
import infrastructure.config.defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class HabitFormView:

    DEFAULT_TEXT_NAME_ENTRY = "Levantarse Temprano, Regar las plantas, etc..."
    DEFAULT_TEXT_CATEGORY_ENTRY = "Tareas, Estudio,  Aseo personal, Proyectos, etc..."
    DEFAULT_TEXTBOX = "Levantarse Temprano (A las 7 AM), Caminar (15 min) , etc..."


    VIEW_MODES = {"add_habit":"AGREGAR HÁBITO",
                 "update_habit":"EDITAR HÁBITO" }
    

    
    ALTURA_FRAME_RELLENO = 200


    def __init__(self,
                 master,
                 style_settings,
                 go_to_main_view, 
                 add_new_habit_event,
                 update_habit,
                 get_habit_categories, 
                ):
        
        self.master = master
        self.fonts = style_settings["fonts"]
        self.theme_colors = style_settings["colors"]
        self.view_mode = "add_habit"
        self.go_to_main_view = go_to_main_view
        self.add_new_habit_event = add_new_habit_event
        self.update_habit_event =update_habit
        self.get_habit_categories = get_habit_categories
        self.command_modes = {"add_habit":self.evento_btn_crear_habito,
                 "update_habit":self.evento_btn_editar_habito}
        self.habit_id_loaded = None
        self.var_select_days_checkbox = ctk.BooleanVar(value=False)
        self.create_frames()




    def _get_frames(self):
        return [
            self.right_frame_container,
            self.left_frame_container,
            self.name_window_frame,
        ]

    def set_view_mode(self,new_mode): 
        if self.view_mode == new_mode:
            return
        self.view_mode = new_mode
        self._change_mode(new_mode)


    def _change_mode(self,mode): 
        self.label_view_name.configure(text = self.VIEW_MODES[mode])
        self.save_habit_button.configure(
            text = self.VIEW_MODES[mode], 
            command = self.command_modes[mode]
            )

    def load_habit(self,habit):
  
        self.habit_id_loaded = habit["id"]
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, habit["habit_name"])
        
    
        self.category_combobox.set(habit["category"])

        self.description_entry.delete("1.0", "end")
        self.description_entry.insert("1.0", habit["description"])

        self.select_color(habit["habit_color"])


        for (clave, boton), estado in zip(self.botones_semana.items(), habit["execution_days"]):

            boton.selected = estado
            self.estado_botones_semana[clave] = estado

            if estado:
                boton.configure(border_width=4, border_color=df.COLOR_BORDE)
            else:
                boton.configure(border_width=0)
        
    def create_frames(self):
        self.create_name_view_frame()
        self.create_left_frame_container()
        self.create_right_frame()
        self.crear_frame_botones_navegacion()

    def create_right_frame(self):
        self.right_frame_container = ctk.CTkFrame(self.master, corner_radius=df.CORNER_RADIUS)

        self.right_frame_container.columnconfigure(0, weight=1)
        self.right_frame_container.rowconfigure(0, weight=1)
        
        self.crear_frame_semana()
        self.crear_frame_botones_navegacion()
        self.crear_frame_relleno_der()

    def crear_frame_relleno_der(self):
        self.frame_relleno_der = ctk.CTkFrame(
            self.right_frame_container,
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"],
            height=self.ALTURA_FRAME_RELLENO,
        )
        self.frame_relleno_der.grid(
            row=2, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY
        )

    def create_name_view_frame(self):
        self.name_window_frame = ctk.CTkFrame(
            self.master, corner_radius=df.CORNER_RADIUS
        )
        self.create_label_view_name()

    def create_label_view_name(self): 
                    
        self.label_view_name = ctk.CTkLabel(
            self.name_window_frame,
            text="AGREGAR HÁBITO",
            font=self.fonts["SUBTITLE"],
            anchor="center",
        )
        self.label_view_name.pack(fill="both", expand=True, padx=df.PADX, pady=df.PADY)

    def create_left_frame_container(self):
        self.left_frame_container = ctk.CTkFrame(self.master)

        self.draw_name_entry_block()
        self.draw_category_block()
        self.color_habito()
        self.configurar_frame_izquierdo()
        frame_relleno_izq = ctk.CTkFrame(
            self.left_frame_container,
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"],
            height=self.ALTURA_FRAME_RELLENO,
        )
        frame_relleno_izq.grid(
            row=6, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY
        )

    def configurar_frame_izquierdo(self):
        self.left_frame_container.columnconfigure(0, weight=1)
        for fila in range(6):
            self.left_frame_container.rowconfigure(fila, weight=1)

    def configurar_frame_semana(self):
        self.frame_selec_semana.columnconfigure(0, weight=1)
        self.frame_selec_semana.columnconfigure(1, weight=1)
        for fila in range(5):
            self.frame_selec_semana.rowconfigure(fila, weight=1)

    def draw_name_entry_block(self):
        ctk.CTkLabel(
            self.left_frame_container,
            text="INGRESA EL NOMBRE DE TU NUEVO HÁBITO",
            font=self.fonts["SMALL"],
        ).grid(column=0, row=0, sticky="nsew", padx=df.PADX, pady=df.PADY)
        self.name_entry = ctk.CTkEntry(
            self.left_frame_container,
            font=self.fonts["SMALL"],
        )
        self.name_entry.grid(
            column=0, row=1, sticky="nsew", padx=df.PADX, pady=df.PADY
        )
        self.name_entry.insert(0, self.DEFAULT_TEXT_NAME_ENTRY)
        self.name_entry.configure(text_color="gray")
        self.name_entry.bind("<FocusIn>", self.on_entry_click)
        self.name_entry.bind("<FocusOut>", self.on_focusout_entry)

    def draw_category_block(self):
        categories = self.get_habit_categories()

        if categories == []: 
            categories = ["Crea una nueva categoria"]

        category_label = ctk.CTkLabel(
            self.left_frame_container,
            text="ELIGE UNA CATEGORIA O CREA UNA NUEVA",
            font=self.fonts["SMALL"],
        )
        category_label.grid(column=0, row=2, sticky="nsew", padx=df.PADX, pady=df.PADY)
        self.category_combobox = ctk.CTkComboBox(
            self.left_frame_container,
            font=self.fonts["SMALL"],
            values= categories
        )
        self.category_combobox.grid(
            column=0, row=3, sticky ="ew", padx=df.PADX, pady=df.PADY
        )
        self.category_combobox.configure(text_color="gray")

    def color_habito(self):
        label_color = ctk.CTkLabel(
            self.left_frame_container,
            text="ELIGE EL COLOR DE TU NUEVO HÁBITO",
            font=self.fonts["SMALL"],
        )
        label_color.grid(column=0, row=4, sticky="nsew", padx=df.PADX, pady=df.PADY)

        frame_colores = ctk.CTkFrame(self.left_frame_container)
        frame_colores.grid(column=0, row=5, sticky="nsew", padx=df.PADX, pady=df.PADY)

        self.btn_colores_estado = {}  # {color: boton}
        self.color_seleccionado = None

        for color in df.COLORES:
            boton_color = ctk.CTkButton(
                frame_colores, fg_color=color, width=60, height=60, text=""
            )
            boton_color.pack(side="left", expand=True, padx=5)

            # Guardar botón en el diccionario
            self.btn_colores_estado[color] = boton_color

            # Comando con lambda que captura color
            boton_color.configure(command=lambda c=color: self.select_color(c))



    def crear_frame_semana(self):
        self.frame_selec_semana = ctk.CTkFrame(self.right_frame_container)
        self.frame_selec_semana.grid(
            column=0, row=0, sticky="nsew", padx=df.PADX, pady=df.PADY
        )
        self.dias_repeticion()
        self.agregar_descripcion()
        self.configurar_frame_semana()

    def dias_repeticion(self):
        label_semana = ctk.CTkLabel(
            self.frame_selec_semana,
            text="DIAS DE LA SEMANA",
            font=self.fonts["SMALL"],
        )
        label_semana.grid(
            column=0, columnspan=2, row=0, sticky="nsew", padx=df.PADX, pady=df.PADY
        )
        boton_seleccionar_todos = ctk.CTkCheckBox(
            self.frame_selec_semana,
            text="SELECCIONAR TODOS",
            variable=self.var_select_days_checkbox,
            command=self.evento_btn_selec_todos,
            font=self.fonts["SMALL"],
        )
        boton_seleccionar_todos.grid(column=1, row=2, sticky="e", padx=40, pady=df.PADY)

        self.frame_dias_semana = ctk.CTkFrame(self.frame_selec_semana)
        self.frame_dias_semana.grid(
            column=0, columnspan=2, row=1, sticky="nsew", padx=df.PADX, pady=df.PADY
        )
        self.crear_botones_semana()

    def agregar_descripcion(self):
        label_descripcion = ctk.CTkLabel(
            self.frame_selec_semana,
            text="AGREGA UNA BREVE DESCRIPCION DE TU HÁBITO",
            font=self.fonts["SMALL"],
        )
        label_descripcion.grid(
            column=0, columnspan=2, row=3, sticky="nsew", padx=df.PADX, pady=df.PADY
        )
        self.description_entry = ctk.CTkTextbox(
            self.frame_selec_semana,
            height=100,
            font=self.fonts["SMALL"],
            border_width=2,
        )
        self.description_entry.insert("0.0", self.DEFAULT_TEXTBOX)
        self.description_entry.configure(text_color="gray")
        self.description_entry.bind("<FocusIn>", self.on_textbox_click)
        self.description_entry.bind("<FocusOut>", self.on_focusout_textbox)
        self.description_entry.grid(
            column=0, columnspan=2, row=4, sticky="nsew", padx=df.PADX, pady=df.PADY
        )

    def crear_botones_semana(self):
        # claves únicas: (clave, etiqueta)
        dias = [
            ("D", "D"),
            ("L", "L"),
            ("Ma", "M"),
            ("Mi", "M"),
            ("J", "J"),
            ("V", "V"),
            ("S", "S"),
        ]

        self.botones_semana = {}  # {clave: boton}
        self.estado_botones_semana = {}  # {clave: bool}

        for clave, texto in dias:
            boton = ctk.CTkButton(
                self.frame_dias_semana,
                font=self.fonts["SMALL"],
                width=60,
                height=60,
                text=texto,
            )
            boton.pack(side="left", padx=13, expand=True)

            # estado inicial
            boton.selected = False
            self.botones_semana[clave] = boton
            self.estado_botones_semana[clave] = False

            # comando seguro que captura boton y clave en el momento de creación
            boton.configure(
                command=lambda b=boton, k=clave: self.evento_btn_semana(b, k)
            )

    def crear_frame_botones_navegacion(self):
        self.frame_botones_navegacion = ctk.CTkFrame(
            self.right_frame_container,

        )
        self.frame_botones_navegacion.grid(
            column=0, row=1, sticky="nsew", padx=df.PADX, pady=df.PADY
        )

        for columna in range(2):
            self.frame_botones_navegacion.columnconfigure(columna, weight=1)
        boton_cancelar = ctk.CTkButton(
            self.frame_botones_navegacion,
            text="CANCELAR",
            command=self.go_to_main_view,

            font=self.fonts["SUBTITLE"],
        )
        boton_cancelar.grid(column=0, row=0, sticky="nsew", padx=df.PADX, pady=df.PADY)
        self.save_habit_button = ctk.CTkButton(
            self.frame_botones_navegacion,
            text="AGREGAR HABITO",
            command=self.evento_btn_crear_habito,
            font=self.fonts["SUBTITLE"],
        )
        self.save_habit_button.grid(
            column=1, row=0, sticky="nsew", padx=df.PADX, pady=df.PADY
        )

    # ----------------------------------------------------EVENTOS-------------------------------------------------------------------------
    def cambiar_foco(self):
        self.master.focus_set()

    def hide(self):
        for frame in self._get_frames():
            frame.grid_remove()
        self.cambiar_foco()

    def show(self):
        for frame in self._get_frames():
            frame.grid()

    def evento_btn_semana(self, boton, clave):
        # alternar estado
        boton.selected = not boton.selected
        self.estado_botones_semana[clave] = boton.selected

        if boton.selected:
            boton.configure(border_width=4, border_color=df.COLOR_BORDE)
        else:
            boton.configure(border_width=0)  # 0 para quitar borde

    def evento_btn_selec_todos(self):
        seleccionar = self.var_select_days_checkbox.get()  # True/False
    
        for clave, boton in self.botones_semana.items():
            boton.selected = seleccionar
            self.estado_botones_semana[clave] = seleccionar
            if seleccionar:
                boton.configure(border_width=4, border_color=df.COLOR_BORDE)
            else:
                boton.configure(border_width=0)

    def select_color(self, color):
        # Desmarcar todos
        for c, boton in self.btn_colores_estado.items():
            boton.configure(border_width=0)

        # Marcar solo el seleccionado
        boton_seleccionado = self.btn_colores_estado[color]
        boton_seleccionado.configure(border_width=4, border_color=df.COLOR_BORDE)

        # Guardar en la variable actual
        self.color_seleccionado = color

    def evento_habito_sin_ejecuciones(self):
        label_error = ctk.CTkLabel(
            self.frame_selec_semana,
            text="Debes elegir al menos un día para ejecutar el hábito*",
            text_color="red",
            font=self.fonts["SMALL"],
        )
        label_error.grid(column=0, row=2, sticky="w", padx=40, pady=df.PADY)

    def evento_btn_crear_habito(self):
        valores = list(self.estado_botones_semana.values())

        if not True in valores:
            self.evento_habito_sin_ejecuciones()
        else:
            # obtener descripcion
            descripcion = self.description_entry.get("0.0", "end-1c")
            self.add_new_habit_event(
                {'name': self.name_entry.get(),
                  'execution_days' : valores,
                  'color': self.color_seleccionado,
                  'category': self.category_combobox.get(),
                  'descripcion' :descripcion
                }
            )
            self.name_entry.delete(0, "end")
            self.go_to_main_view()



    def evento_btn_editar_habito(self):
        valores = list(self.estado_botones_semana.values())

        if not True in valores:
            self.evento_habito_sin_ejecuciones()
        else:
            # obtener descripcion
            descripcion = self.description_entry.get("0.0", "end-1c")
            self.update_habit_event(
                {'name': self.name_entry.get(),
                  'execution_days' : valores,
                  'color': self.color_seleccionado,
                  'category': self.category_combobox.get(),
                  'descripcion' :descripcion,
                  'id': self.habit_id_loaded
                }
            )
            self.name_entry.delete(0, "end")


    def on_entry_click(self, event):
        if self.name_entry.get() == self.DEFAULT_TEXT_NAME_ENTRY:
            self.name_entry.delete(0, "end")
            self.name_entry.configure(text_color="white")

    def on_focusout_entry(self, event):
        if self.name_entry.get() == "":
            self.name_entry.insert(0, self.DEFAULT_TEXT_NAME_ENTRY)
            self.name_entry.configure(text_color="gray")

    def on_textbox_click(self, event):
        # Quitar el salto de línea extra con strip()
        if (
            self.description_entry.get("0.0", "end").strip()
            == self.DEFAULT_TEXTBOX
        ):
            self.description_entry.delete("0.0", "end")
            self.description_entry.configure(text_color="white")

    def on_focusout_textbox(self, event):
        # Revisar si está vacío (después de quitar espacios y saltos)
        if self.description_entry.get("0.0", "end").strip() == "":
            self.description_entry.insert("0.0", self.DEFAULT_TEXTBOX)
            self.description_entry.configure(text_color="gray")
