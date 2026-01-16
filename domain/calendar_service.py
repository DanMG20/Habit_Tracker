from datetime import datetime
from datetime import timedelta
import calendar
from dateutil.relativedelta import relativedelta
from utils.paths import resource_path
import locale
# Establecer el locale a español (puede variar según el sistema operativo)
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
class CalendarService():
    def __init__(self, db_objeto):
        self.db_objeto = db_objeto
        self.refrescar_variables()


    
    def refrescar_variables(self):
        self.DIA_HOY = datetime.now()
        self.dia_hoy_variable = datetime.now()
        self.dia_hoy_variable_2 = datetime.now()
        self.dia_hoy_variable_3 = datetime.now()
        self.DIA_AYER = datetime.now() - timedelta(days=1)

    
    def date_vars(self):
            #CONSTANTES
            FECHA_MANANA = datetime.now() + timedelta(days=1)
            DIA_MANANA =FECHA_MANANA.day
            SEMANA_CORRIENTE =FECHA_MANANA.isocalendar().week
            MES_CORRIENTE = datetime.now().strftime("%B")
            ANIO_CORRIENTE = datetime.now().year
            # Aqui cambiamos el inicio de la semana a domingo
            dia_semana_domingo = (datetime.now().weekday() + 1) % 7
            if dia_semana_domingo == 0:
                dia = " Domingo "
                dia_ayer = " Lunes "
            elif dia_semana_domingo == 1:
                dia = " Lunes "
                dia_ayer = " Domingo "
            elif dia_semana_domingo == 2:
                dia = " Martes "
                dia_ayer = " Lunes "
            elif dia_semana_domingo == 3:
                dia = " Miércoles "
                dia_ayer = " Martes "
            elif dia_semana_domingo == 4:
                dia = " Jueves "
                dia_ayer = " Miércoles "
            elif dia_semana_domingo == 5:
                dia = " Viernes "
                dia_ayer = " Jueves "
            elif dia_semana_domingo == 6:
                dia = " Sábado "
                dia_ayer = " Viernes "
            mes_encabezado = MES_CORRIENTE
            texto_semana_encabezado = "Semana " + str((self.dia_hoy_variable+timedelta(days=1)).isocalendar().week)
            texto_dia_encabezado = "HOY," + dia + str(self.DIA_HOY.day)
            texto_dia_encabezado_ayer = "AYER," + dia_ayer + str(self.DIA_AYER.day)
            return (texto_dia_encabezado,
                    texto_semana_encabezado,
                    mes_encabezado,
                    ANIO_CORRIENTE,
                    texto_dia_encabezado_ayer)

    def inicio_semana(self):
        # Ajustar el inicio de la semana al domingo
            inicio_semana = self.dia_hoy_variable - timedelta(days=(self.dia_hoy_variable.weekday() + 1) % 7)
            return inicio_semana
    
    def dias_actuales(self): 
        dias_actuales = []
        for dia_indic in range(7):  # Del domingo (0) al sábado (6)
                dia_semana = self.inicio_semana() + timedelta(days=dia_indic)
                dias_actuales.append(dia_semana)
        
        return dias_actuales
    #----------------------------------------------CALCULO RENDIMIENTO--------------------------------------
    def calcular_rendimiento_semanal(self):
        ejecuciones = self.db_objeto.cargar_ejecuciones()
        inicio_semana = self.inicio_semana()  # Domingo
        fin_semana = inicio_semana + timedelta(days=6)

        habitos_totales = 0
        habitos_cumplidos = 0

        for habit in self.db_objeto.habitos:
            fecha_creacion = datetime.strptime(habit["Fecha_creacion"], "%Y-%m-%d").date()
            dias_ejecucion = habit["dias_ejecucion"]  # lista de 7 elementos [0|1]

            for i in range(7):
                dia_semana = inicio_semana + timedelta(days=i)
                if dia_semana.date() < fecha_creacion:
                    continue  # Ignorar días antes de la creación

                # Obtener índice correcto según weekday: domingo=0, lunes=1, ...
                # Si tu lista empieza en lunes, ajusta: weekday=dia_semana.weekday()
                if dias_ejecucion[i] == 1:  # Día programado
                    habitos_totales += 1
                    # Buscar si se cumplió
                    ejecucion = next(
                        (e for e in ejecuciones if e["nombre_habito"] == habit["nombre_habito"]
                        and e["fecha_ejecucion"] == dia_semana.strftime("%Y-%m-%d")),
                        None
                    )
                    if ejecucion and ejecucion.get("completado", False):
                        habitos_cumplidos += 1

        rendimiento = (habitos_cumplidos / habitos_totales * 100) if habitos_totales > 0 else 0
        rendimiento_redondeado = round(rendimiento)
        return rendimiento_redondeado

    


    def semana_siguiente(self):
         if self.dia_hoy_variable > (self.DIA_HOY +timedelta(weeks=1)):
                print("Ya no se puede avanzar mas")
         else:
             self.dia_hoy_variable = self.dia_hoy_variable + timedelta(weeks=1)

    def semana_anterior(self): 
        if self.db_objeto.habitos:
            # Convertir las fechas a objetos date y tomar la más antigua
            fechas = [
                datetime.strptime(h["Fecha_creacion"], "%Y-%m-%d").date()
                for h in self.db_objeto.habitos
            ]
            fecha_inicial = min(fechas)
        else:
            fecha_inicial = self.DIA_HOY.date()

        if self.dia_hoy_variable.date() <= fecha_inicial:
            print("ya no se puede avanzar más")
        else:
            self.dia_hoy_variable -= timedelta(weeks=1)
         
    def obtener_dias_mes(self):
        año =self.dia_hoy_variable_2.year
        mes=self.dia_hoy_variable_2.month
        rango = calendar.monthrange(año,mes)[1]
        return rango

    def calcular_rendimiento_diario(self, fecha):
        """
        Calcula el rendimiento diario en % de hábitos cumplidos.
        La semana comienza en domingo (domingo=0 ... sábado=6).
        
        fecha: datetime (día a evaluar)
        """
        fecha_dia = fecha.date()
        dia_semana = (fecha_dia.weekday() + 1) % 7  # domingo=0 ... sábado=6

        ejecuciones = self.db_objeto.cargar_ejecuciones()
        habitos = self.db_objeto.habitos

        habitos_totales = 0
        habitos_cumplidos = 0

        for habito in habitos:
            fecha_creacion = datetime.strptime(habito["Fecha_creacion"], "%Y-%m-%d").date()

            # Solo contar si el hábito existía en ese día
            if fecha_creacion <= fecha_dia:
                # Verificar si ese hábito se debe ejecutar en ese día de la semana
                if habito["dias_ejecucion"][dia_semana]:
                    habitos_totales += 1

                    # Verificar si fue cumplido en ejecuciones
                    for ejec in ejecuciones:
                        ejec_fecha = datetime.strptime(ejec["fecha_ejecucion"], "%Y-%m-%d").date()
                        if (
                            ejec["nombre_habito"] == habito["nombre_habito"]
                            and ejec_fecha == fecha_dia
                            and ejec["completado"]
                        ):
                            habitos_cumplidos += 1
                            break  # evitar duplicados

        if habitos_totales == 0:
            return 0
        return (habitos_cumplidos / habitos_totales) * 100

    def calcular_rendimiento_mes(self):
        """
        Devuelve un diccionario con el rendimiento (%) por cada día del mes.
        Usa la función calcular_rendimiento_diario.
        """
        year = self.dia_hoy_variable_2.year
        month = self.dia_hoy_variable_2.month
        # número de días en el mes
        num_days = calendar.monthrange(year, month)[1]
        resultados = {}

        for day in range(1, num_days + 1):
            fecha = datetime(year, month, day)
            rendimiento = self.calcular_rendimiento_diario(fecha)
            resultados[day] = rendimiento

        return resultados
    
    def calcular_rend_mes(self):
        rend_diario_mes = self.calcular_rendimiento_mes()
        rend_diario_mes_lista = []
        
        for valor in rend_diario_mes.values():
            rend_diario_mes_lista.append(valor)
        rango = self.obtener_dias_mes()
        total=0

        for dia in rend_diario_mes_lista: 
            total += dia

        promedio_mes = total/rango

        return round(promedio_mes)

    def encabezado_mes(self): 
        return self.dia_hoy_variable_2.strftime("%B")
    
    def encabezado_anio(self):
        return self.dia_hoy_variable_3.year

    def mes_siguiente(self):
        if self.dia_hoy_variable_2 > (self.DIA_HOY +relativedelta(months=1)):
            print("Ya no se puede avanzar mas")
        else:
            self.dia_hoy_variable_2 +=  relativedelta(months=1)

    def mes_anterior(self): 
        if self.db_objeto.habitos:
            # Convertir las fechas a objetos date y tomar la más antigua
            fechas = [
                datetime.strptime(h["Fecha_creacion"], "%Y-%m-%d").date()
                for h in self.db_objeto.habitos
            ]
            fecha_inicial = min(fechas)
        else:
            fecha_inicial = self.DIA_HOY.date()

        if self.dia_hoy_variable_2.date() <= fecha_inicial:
            print("ya no se puede avanzar más")
        else:
            self.dia_hoy_variable_2 -= relativedelta(months=1)
    

    def rendimiento_meses_anio(self):
        rendimiento_meses = []
        anio = self.dia_hoy_variable_3.year
        # número de días en el mes
        meses = [month for month in range(1, 13)]
        for mes in meses:
            rango = calendar.monthrange(anio,mes)[1]
            total=0
            for day in range(1, rango + 1):
                fecha = datetime(anio, mes, day)
                rendimiento = self.calcular_rendimiento_diario(fecha)
                total += rendimiento
                rendimiento_mes = total/rango
            rendimiento_meses.append(round(rendimiento_mes))
        tot=0
        for rend in rendimiento_meses:
            tot +=rend
        rendimiento_anual = round(tot/12,2)
        return rendimiento_meses,rendimiento_anual
    
    def nombres_meses(self):
        return [calendar.month_name[month] for month in range(1, 13)]
    

    def anio_siguiente(self):
        if self.dia_hoy_variable_3 > (self.DIA_HOY +relativedelta(years=1)):
            print("Ya no se puede avanzar mas")
        else:
            self.dia_hoy_variable_3 +=  relativedelta(years=1)

    def anio_anterior(self): 
        if self.db_objeto.habitos:
            # Convertir las fechas a objetos date y tomar la más antigua
            fechas = [
                datetime.strptime(h["Fecha_creacion"], "%Y-%m-%d").date()
                for h in self.db_objeto.habitos
            ]
            fecha_inicial = min(fechas)
        else:
            fecha_inicial = self.DIA_HOY.date()

        if self.dia_hoy_variable_3.date() <= fecha_inicial:
            print("ya no se puede avanzar más")
        else:
            self.dia_hoy_variable_3 -= relativedelta(years=1)