
import customtkinter as ctk
from infrastructure.config import defaults as df
from domain.style_service import StyleService
from infrastructure.logging.logger import get_logger


logger = get_logger(__name__)


class QuoteWindow(ctk.CTkToplevel):
    def __init__(self, master, on_add_quote,quotes,on_delete_quote,on_update_quote):
        super().__init__(master)
        self.master = master
        self.on_add_quote = on_add_quote
        self.quotes = quotes
        self.on_delete_quote = on_delete_quote
        self.on_update_quote = on_update_quote

        self.selected_quote = None

        self.load_style_settings()
        self.build()


    def build(self):
        
        self.draw_quote_window()
        self.config_panels()
        self.draw_edit_panel()
        self.config_edit_panel()
        self.draw_entrys()
        self.draw_quote_table()
        self.draw_button_panel()
        self.draw_add_button()
        self.draw_update_button()
        self.draw_delete_button()


    def load_style_settings(self):
        style_service = StyleService()
        self.theme_colors = style_service._load_theme_colors()
        self.fonts = style_service.build_fonts()
    

    def draw_quote_table(self): 
        self.quote_frame = ctk.CTkScrollableFrame(
            master=self,
            corner_radius=df.CORNER_RADIUS
        )
        self.quote_frame.grid(row = 0, column = 0 ,padx = 10 ,pady= 5, sticky="nsew")

        ctk.CTkLabel(self.quote_frame,
                    font=self.fonts["SMALL"], 
                    text="Frases guardadas").grid(row = 0,
                                                   column = 0 ,
                                                     columnspan = 2 ,
                                                     pady=10, sticky ="nsew")
        self. draw_table_headers()
        self.draw_quotes()
        self.config_table()

    def config_panels(self): 
      
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)

    def draw_table_headers(self): 
        headers = ["Frase", "Autor"]

        for index,header in enumerate(headers):
            ctk.CTkLabel(
                        self.quote_frame,
                        text=header,
                        font=self.fonts["SMALL"],
                        fg_color=self.theme_colors["top_frame"],
                        
                    ).grid( column = index , 
                           row = 1, sticky = "nsew" ,pady = 2
                           )


    def config_table(self):
        self.quote_frame.grid_columnconfigure(0, weight=3)
        self.quote_frame.grid_columnconfigure(1, weight=1)

    def config_edit_panel(self): 
        self.edit_panel.grid_rowconfigure(0, weight=1)

    def draw_quotes(self):
        for index,quote in enumerate(self.quotes):
                for n in range(2):
                    if n >0: 
                        but_state ="disabled"
                    else:
                        but_state ="normal "
                    btn=ctk.CTkButton(
                        self.quote_frame,
                        corner_radius= 0,
                        text=self.shorten_text(quote[n+1]),
                        font=self.fonts["SMALL"],
                        state = but_state,
                        fg_color=self.theme_colors["top_frame"],
                       
                        )

                    btn.configure( command= lambda q=quote, b=btn: self.on_quote_selected(q,b))
                    btn.grid( column = n , row = index+2, sticky = "nsew" ,pady = 2)
                    
                index  = 0 


    def shorten_text(self,text):
        max_chars = 35
        if len(text) <= max_chars:
            return text
        return text[:max_chars - 3] + "..."

                

    def draw_quote_window(self):
        self.grab_set()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        self.width = 900
        self.heigth = 350

        x = (pantalla_ancho // 2) - (self.width // 2) + 143
        y = (pantalla_alto // 2) - (self.heigth // 2)
        self.geometry(f"{self.width}x{self.heigth}+{x}+{y}")
        self.title("Frases")

        
 

        self.update_idletasks()

    def draw_entrys(self): 

        ctk.CTkLabel(self.edit_panel, font=self.fonts["SMALL"], text="Frase:").pack(pady=(10, 0))
        self.entry_quote = ctk.CTkEntry(self.edit_panel,
                                        font=self.fonts["SMALL"], 
                                        width=350
                                        )
        self.entry_quote.pack(pady=5, padx = df.PADX)

        ctk.CTkLabel(self.edit_panel, font=self.fonts["SMALL"], text="Autor:").pack(pady=(10, 0))
        self.entry_author = ctk.CTkEntry(self.edit_panel,
                                          width=350,
                                          font= self.fonts["SMALL"]
                                          )
        self.entry_author.pack(pady=5, padx = df.PADX)



    def draw_edit_panel(self):

        self.edit_panel = ctk.CTkFrame(
            master = self, 
            corner_radius= df.CORNER_RADIUS
        )
        self.edit_panel.grid( row = 0 , column = 1, sticky ="nsew", pady= df.PADY, padx =df.PADX)

    def draw_button_panel(self): 

        self.button_panel = ctk.CTkFrame(
            master = self.edit_panel,
            corner_radius= df.CORNER_RADIUS
        )
        self.button_panel.pack( fill= "both", pady= df.PADY , padx = df.PADX, expand =True)

    def draw_update_button(self):
        ctk.CTkButton(
            self.button_panel,
            text="Editar frase",
            font=self.fonts["SMALL"],
            command=self.update_button_event,
        ).pack(fill="both", pady=10, padx= df.PADX,expand =True)
        

    def draw_add_button(self):

        ctk.CTkButton(
            self.button_panel,
            text="Agregar frase",
            font=self.fonts["SMALL"],
            command=self.add_quote,
        ).pack( fill="both", pady=10, padx= df.PADX,expand =True)
        

    def draw_delete_button(self): 

        ctk.CTkButton(
            self.button_panel,
            text="Eliminar frase",
            font=self.fonts["SMALL"],
            command=self.delete_quote,
        ).pack( fill="both", pady=10, padx= df.PADX,expand =True)
        
    def update_button_event(self):

        quote_str= self.entry_quote.get().strip()
        author_str = self.entry_author.get().strip()

        self.safety_check(quote_str,author_str)
        self.on_update_quote(
            self.selected_quote[0],
            quote_str,
            author_str
        )
        
    def on_quote_selected(self,quote, button): 
        self.selected_quote = quote
        self.write_quote()

        for child in self.quote_frame.winfo_children():
            child.configure(fg_color = self.theme_colors["top_frame"])

        button.configure(
        fg_color=self.theme_colors["progressbar"]
    )

    def write_quote(self):
        self.entry_quote.delete(0, "end")
        self.entry_quote.insert(0, self.selected_quote[1])

        self.entry_author.delete(0, "end")
        self.entry_author.insert(0, self.selected_quote[2])



    def delete_quote(self):
        self.on_delete_quote(self.selected_quote[0])

    def add_quote(self):
        quote_str = self.entry_quote.get().strip()
        author_str = self.entry_author.get().strip()

        self.safety_check(quote_str,author_str)
        self.on_add_quote([(quote_str,author_str)])
        #self.draw_quotes() --->  solucionar bugg

        
    def safety_check(self,quote_str,author_str):

        if not quote_str or not author_str:
            self.label_error.configure(text="Ambos campos son obligatorios")
            return
        