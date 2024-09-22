import tkinter as tk 
import pandas as pd
import calendar

archivo_csv = 'tarea.csv'

# df para almacenar las tareas
columnas = ["Fecha límite", "Tarea", "Completado", "Prioridad"]

# leer el archivo
try:
    df = pd.read_csv(archivo_csv)
except FileNotFoundError:
    df = pd.DataFrame(columns=columnas)

fecha_seleccionada = None

# guardar el df en el CSV
def guardar_tareas_csv():
    global df
    try:
        df.to_csv(archivo_csv, index=False)
        print(df)
        print("Tareas guardadas en 'tarea.csv'")
    except Exception:
        print(f"Error al guardar el archivo CSV: {Exception}")

def abrir_ventana_tarea():
    ventana_tarea = tk.Toplevel()
    ventana_tarea.title("Agregar Tarea")
    ventana_tarea.geometry("300x350")
    ventana_tarea.configure(background='AntiqueWhite3')


    tarea_var = tk.StringVar()
    completado_var = tk.IntVar()  # completado (1 o 0)
    prioridad_var = tk.IntVar()  # prioridad (1, 2 o 3)

    
    tk.Label(ventana_tarea, text="Tarea:", bg='AntiqueWhite3').pack(padx=10, pady=5)
    tk.Entry(ventana_tarea, textvariable=tarea_var).pack(padx=10, pady=5)

    # asigno el valor que se elija a la variable 
    tk.Label(ventana_tarea, text="¿Está completada?", bg='AntiqueWhite3').pack(padx=10,pady=5)
    tk.Radiobutton(ventana_tarea, text="Sí", variable=completado_var, value=1, bg='AntiqueWhite3').pack(padx=10,pady=5)
    tk.Radiobutton(ventana_tarea, text="No", variable=completado_var, value=0, bg='AntiqueWhite3').pack(padx=10, pady=5)

    
    tk.Label(ventana_tarea, text="Prioridad:", bg='AntiqueWhite3').pack(padx=10, pady=5)
    tk.Radiobutton(ventana_tarea, text="Alto", variable=prioridad_var, value=1, bg='AntiqueWhite3').pack(padx=10, pady=5)
    tk.Radiobutton(ventana_tarea, text="Medio",variable=prioridad_var, value=2, bg='AntiqueWhite3').pack(padx=10,pady=5)
    tk.Radiobutton(ventana_tarea, text="Bajo", variable=prioridad_var, value=3, bg='AntiqueWhite3').pack(padx=10, pady=5)


    # agregar la tarea al df
    def agregar_tarea():
        
        global df, fecha_seleccionada
        
        tarea = tarea_var.get()
        completado = bool(completado_var.get())
        prioridad = prioridad_var.get()

        # nueva fila con los datos de la tarea
        nueva_fila = pd.DataFrame({ "Fecha límite": [fecha_seleccionada],"Tarea": [tarea],"Completado": [completado], "Prioridad": [prioridad] })
        

        # poner la nueva fila en un df
        df = pd.concat([df, nueva_fila], ignore_index=True)
        print(f"\nTarea guardada en la fecha {fecha_seleccionada}:")
        print(df)


        guardar_tareas_csv()
        ventana_tarea.destroy()

    tk.Button(ventana_tarea, text="Guardar Tarea", command=agregar_tarea, bg='NavajoWhite4').pack(padx=10, pady=10)

def abrir_dia(dia):
    #Una f-string permite insertar el valor de variables directamente dentro de una cadena de texto 
    global fecha_seleccionada
    fecha_seleccionada = f"{año_var.get()}-{mes_var.get()}-{dia:02d}"  # Asegúrate de que el día tenga dos dígitos

    dia_ventana = tk.Toplevel()
    dia_ventana.title(f"Fecha seleccionada: {fecha_seleccionada}")
    dia_ventana.geometry("300x400")
    dia_ventana.configure(background='AntiqueWhite3')

    tk.Label(dia_ventana, text=f"Fecha seleccionada: {fecha_seleccionada}", bg="seashell2").pack(padx=10, pady=10)

    tareas_dia = df[df["Fecha límite"] == fecha_seleccionada]
    if not tareas_dia.empty:
        tk.Label(dia_ventana, text="Tareas:", bg='seashell2').pack(pady=5)
        for index, tarea in tareas_dia.iterrows():
            tarea_texto = f"{tarea['Tarea']} - {'Completada' if tarea['Completado'] else 'Pendiente'} - Prioridad {tarea['Prioridad']}"
            tk.Label(dia_ventana, text=tarea_texto, bg='seashell2').pack(pady=5)

    tk.Button(dia_ventana, text="Agregar Tarea", command=abrir_ventana_tarea, bg='NavajoWhite4').pack(pady=10)


def abrir_manual():
    manual = tk.Toplevel()
    manual.title("Manual de Uso")
    manual.geometry("400x300")
    manual.configure(background='AntiqueWhite3')

    
    texto_manual = """
    Manual de uso del calendario y gestión de tareas:
    - Selecciona un mes y un año.
    - Haz clic en un día del calendario 
    - En la ventana del día, puedes agregar o ver las tareas.
    - Las tareas tienen una fecha límite, estado (completada o no) y prioridad.
    """
    
    etiqueta_manual = tk.Label(manual, text=texto_manual, bg="seashell2", fg="black", justify="left")
    etiqueta_manual.pack(padx=10, pady=10)
    boton_cerrar = tk.Button(manual, text="Cerrar", command=manual.destroy, bg='NavajoWhite4')
    boton_cerrar.pack(pady=10)

def mostrar_calendario():
    mes = int(mes_var.get())
    año = int(año_var.get())

    ventana_calendario = tk.Toplevel()
    ventana_calendario.title(f"Calendario {mes}/{año}")
    ventana_calendario.geometry("500x500")
    ventana_calendario.configure(background='AntiqueWhite3')
    primer_dia_mes, num_dias_mes = calendar.monthrange(año, mes)

    # l,m,x,j,v,s,d
    for col, dia in enumerate(dias_semana):
        etiqueta = tk.Label(ventana_calendario, text=dia, borderwidth=4, relief="groove", width=6, height=2)
        etiqueta.grid(row=2, column=col, sticky="nsew")

    # días del mes
    dia_actual = 1
    for fila in range(3, 9):
        for columna in range(7):
            if fila == 3 and columna < primer_dia_mes:
                cuadro = tk.Label(ventana_calendario, text="", borderwidth=2, relief="groove", width=6, height=2)
                cuadro.grid(row=fila, column=columna, sticky="nsew")
            elif dia_actual <= num_dias_mes:
                cuadro = tk.Button(ventana_calendario, text=str(dia_actual), borderwidth=2, relief="groove", width=6, height=2,
                                   command=lambda dia=dia_actual: abrir_dia(dia))
                cuadro.grid(row=fila, column=columna, sticky="nsew")
                dia_actual += 1
    for i in range(7):
        ventana_calendario.grid_columnconfigure(i, weight=1)
    for i in range(8):
        ventana_calendario.grid_rowconfigure(i, weight=1)
        
#orden por prioridad y por fecha de todas las tareas       
def mostrar_ventana_ordenada(orden):
    ventana_ordenada= tk.Toplevel()
    ventana_ordenada.title(f"Tareas Ordenadas por {orden}")
    ventana_ordenada.geometry("400x400")
    ventana_ordenada.configure(background='AntiqueWhite3')

    if orden == "Día":
        df_ordenado = df.copy()
        df_ordenado['Día'] = pd.to_datetime(df_ordenado['Fecha límite']).dt.day
        df_ordenado.sort_values(by='Día', inplace=True)
    elif orden == "Prioridad":
        df_ordenado = df.sort_values(by='Prioridad')

    if df_ordenado.empty:
        tk.Label(ventana_ordenada, text="No hay tareas para mostrar", bg='seashell2').pack(pady=10)
    else:
        for i, (index, tarea) in enumerate(df_ordenado.iterrows()):
            tarea_texto= f"{tarea['Fecha límite']} - {tarea['Tarea']} - {'Completada' if tarea['Completado'] else 'Pendiente'} - Prioridad {tarea['Prioridad']}"
            tk.Label(ventana_ordenada, text=tarea_texto, bg='seashell2').pack(pady=5)


# ventana principal
ventana = tk.Tk()
ventana.title("Calendario y Tareas")
ventana.geometry("500x500")
ventana.configure(background='AntiqueWhite3')


mes_var = tk.StringVar()
año_var = tk.StringVar()
dias_semana = ['L', 'M', 'X', 'J', 'V', 'S', 'D']
tk.Label(ventana, text="Mes:", bg='AntiqueWhite3').grid(row=0, column=0, sticky="nsew")
tk.OptionMenu(ventana, mes_var, *list(range(1, 13))).grid(row=0, column=1, sticky="nsew", pady=4)
tk.Label(ventana, text="Año:", bg='AntiqueWhite3').grid(row=0, column=2, sticky="nsew")
tk.OptionMenu(ventana, año_var, *list(range(2024, 2050))).grid(row=0, column=3, sticky="nsew", pady=4)

tk.Button(ventana, text="Mostrar Calendario", bg='NavajoWhite4', command=mostrar_calendario).grid(row=1, column=0, columnspan=4, sticky="nsew")
tk.Button(ventana, text="Abrir Manual de Uso", bg='NavajoWhite4', command=abrir_manual).grid(row=2, column=0, columnspan=4, sticky="nsew")
tk.Button(ventana, text="Ordenar por Día", bg='NavajoWhite4', command=lambda: mostrar_ventana_ordenada("Día")).grid(row=3, column=0, columnspan=2, sticky="nsew")
tk.Button(ventana, text="Ordenar por Prioridad", bg='NavajoWhite4', command=lambda: mostrar_ventana_ordenada("Prioridad")).grid(row=3, column=2, columnspan=2, sticky="nsew")


ventana.mainloop()
