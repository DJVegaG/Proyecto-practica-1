import tkinter as tk
from tkinter import ttk, filedialog, StringVar
from PIL import Image, ImageTk
import imutils
import cv2
import os
import serial.tools.list_ports

# Variables globales a utilizar para la captura
captura1 = None
captura2 = None

# Funcion para obtener la lista de cámaras conectadas
def obtener_camaras_disponibles():
    camaras_disponibles = []
    for i in range(5):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            camaras_disponibles.append(f"Camara {i}")
            cap.release()
    return camaras_disponibles

# Funcion para iniciar la captura de la camara 1
def iniciar_captura1(captura1, label_imagen):
    if captura1 is not None:
        ret, frame = captura1.read()
        if ret:
            frame = imutils.resize(frame, width=311)
            frame = imutils.resize(frame, height=241)
            imagen_camara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(imagen_camara)
            img_tk = ImageTk.PhotoImage(image=img)
            label_imagen.configure(image=img_tk)
            label_imagen.image = img_tk
            label_imagen.after(10, lambda: iniciar_captura1(captura1, label_imagen))
        else:
            label_imagen.image = ""
            captura1.release()

# Funcion para inciar la captura de la camara 2
def iniciar_captura2(captura2, label_imagen):
    if captura2 is not None:
        ret, frame = captura2.read()
        if ret:
            frame = imutils.resize(frame, width=311)
            frame = imutils.resize(frame, height=241)
            imagen_camara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(imagen_camara)
            img_tk = ImageTk.PhotoImage(image=img)
            label_imagen.configure(image=img_tk)
            label_imagen.image = img_tk
            label_imagen.after(10, lambda: iniciar_captura2(captura2, label_imagen))
        else:
            label_imagen.image = ""
            captura2.release()

# Funcion para capturar y guardar la imagen
def capturar_guardar_mostrar(captura, carpeta_destino, nombre_archivo, label_captura, camara_numero, tiempo_captura, cantidad_capturas, intervalo_capturas):
    if captura is not None:
        for i in range(int(cantidad_capturas)):
            ret, frame = captura.read()
            if ret:
                frame = imutils.resize(frame, width=311)
                frame = imutils.resize(frame, height=241)
                imagen_captura = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(imagen_captura)
                img_tk = ImageTk.PhotoImage(image=img)
                label_captura.configure(image=img_tk)
                label_captura.image = img_tk
                ruta_completa = os.path.join(carpeta_destino, f"{nombre_archivo}_camara{camara_numero}.png")
                cv2.imwrite(ruta_completa, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                print(f"Captura de camara {camara_numero} guardada en: {ruta_completa}")
                ventana.update()
                if i < int(cantidad_capturas) - 1:
                    ventana.after(int(intervalo_capturas), lambda: None)
                else:
                    break
            else:
                print("No se pudo realizar la captura de camara {camara_numero}")
                break

# Funcion de conexion a la camara 1
def conectar_camara_1(numero_camara, label_imagen):
    try:
        global captura1
        captura1 = cv2.VideoCapture(numero_camara, cv2.CAP_DSHOW)
        if captura1.isOpened():
            print(f"Conectado a la cámara {numero_camara}")
            iniciar_captura1(captura1, label_imagen)
            boton_conectar1.config(state=tk.DISABLED)
            boton_desconectar1.config(state=tk.NORMAL)
        else:
            print(f"No se pudo conectar a la cámara {numero_camara}")
    except Exception as e:
        print(f"Error al conectar a la cámara {numero_camara}: {e}")

# Funcion de desconexion a la camara 1
def desconectar_camara_1():
    global captura1
    if captura1 is not None:
        captura1.release()
        print("Cámara desconectada")
        boton_conectar1.config(state=tk.NORMAL)
        boton_desconectar1.config(state=tk.DISABLED)

# Funcion de conexion a la camara 2
def conectar_camara_2(numero_camara, label_imagen):
    try:
        global captura2
        captura2 = cv2.VideoCapture(numero_camara, cv2.CAP_DSHOW)
        if captura2.isOpened():
            print(f"Conectado a la cámara {numero_camara}")
            iniciar_captura2(captura2, label_imagen)
            boton_conectar2.config(state=tk.DISABLED)
            boton_desconectar2.config(state=tk.NORMAL)
        else:
            print(f"No se pudo conectar a la cámara {numero_camara}")
    except Exception as e:
        print(f"Error al conectar a la cámara {numero_camara}: {e}")

# Funcion de desconexion a la camara 2
def desconectar_camara_2():
    global captura2
    if captura2 is not None:
        captura2.release()
        print("Cámara desconectada")
        boton_conectar2.config(state=tk.NORMAL)
        boton_desconectar2.config(state=tk.DISABLED)

# Funcion para seleccionar la carpeta de destino y el nombre del archivo
def seleccionar_destino():
    carpeta_destino = filedialog.askdirectory()
    entrada_nombre.delete(0, tk.END)  # Limpiar la entrada
    entrada_nombre.insert(0, "img_prueba")  # Establecer un nombre predeterminado
    etiqueta_ruta.config(text=carpeta_destino)

# Funcion para cerrar la ventana
def cerrar_ventana():
    if captura1 is not None:
        captura1.release()
    if captura2 is not None:
        captura2.release()
    ventana.destroy()

# Configuracion de la ventana
ventana = tk.Tk()
# Obtencion del ancho y alto de la pantalla
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
# Abrir ventana con el 80% del ancho y alto de la pantalla
ventana.geometry(f"{int(ancho_pantalla * 0.8)}x{int(alto_pantalla * 0.8)}")
# Titulo de la ventana
ventana.title("Proyecto procesamiento de imagen con webcam")
# Que sucede al cerrar la ventana
ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# Lista de cámaras disponibles
lista_camaras = obtener_camaras_disponibles()

# Combobox y boton para la camara 1
combobox_camara1 = ttk.Combobox(ventana, values=lista_camaras, state="readonly")
combobox_camara1.set("Selecciona una cámara")
combobox_camara1.place(x=75, y=330, width=200, height=23)
# Nombre para la camara 1
label_camara1 = tk.Label(ventana, text="Cámara 1:")
label_camara1.place(x=75, y=305, width=60, height=23)

# Combobox y boton para la camara 2
combobox_camara2 = ttk.Combobox(ventana, values=lista_camaras, state="readonly")
combobox_camara2.set("Selecciona una cámara")
combobox_camara2.place(x=415, y=330, width=200, height=23)
# Nombre para la camara 2
label_camara2 = tk.Label(ventana, text="Cámara 2:")
label_camara2.place(x=415, y=305, width=60, height=23)

# Etiqueta y botón para seleccionar la carpeta de destino
etiqueta_ruta = tk.Label(ventana, text="Carpeta de destino:", wraplength=300, justify="left")
etiqueta_ruta.place(x=200, y=800, width=300, height=40)

boton_seleccionar = tk.Button(ventana, text="Seleccionar carpeta", command=seleccionar_destino)
boton_seleccionar.place(x=50, y=800, width=150, height=30)

# Entrada para el nombre del archivo
etiqueta_nombre = tk.Label(ventana, text="Nombre del archivo:")
etiqueta_nombre.place(x=50, y=850, width=150, height=20)

entrada_nombre = tk.Entry(ventana)
entrada_nombre.place(x=190, y=850, width=150, height=30)
entrada_nombre.insert(0, "img_prueba")

# Botones para conectar camaras y capturar imagenes
# Conexion camara 1
boton_conectar1 = tk.Button(ventana, text="Conectar", command=lambda: conectar_camara_1(combobox_camara1.current(), label_imagen1))
boton_conectar1.place(x=50, y=370, width=120, height=30)
# Desconexion camara 1
boton_desconectar1 = tk.Button(ventana, text="Desconectar", command=desconectar_camara_1, state=tk.DISABLED)
boton_desconectar1.place(x=180, y=370, width=120, height=30)
# Captura camara 1
boton_capturar1 = tk.Button(ventana, text="Capturar", command=lambda: capturar_guardar_mostrar(captura1, etiqueta_ruta.cget("text").split(": "), entrada_nombre.get(), label_captura1, 1, entrada_tiempo_captura.get(), entrada_cantidad_capturas.get(), entrada_intervalo_capturas.get()))
boton_capturar1.place(x=130, y=720, width=120, height=30)
# Conexion camara 2
boton_conectar2 = tk.Button(ventana, text="Conectar", command=lambda: conectar_camara_2(combobox_camara2.current(), label_imagen2))
boton_conectar2.place(x=390, y=370, width=120, height=30)
# Desconexion camara 2
boton_desconectar2 = tk.Button(ventana, text="Desconectar", command=desconectar_camara_2, state=tk.DISABLED)
boton_desconectar2.place(x=520, y=370, width=120, height=30)
# Captura camara 2
boton_capturar2 = tk.Button(ventana, text="Capturar", command=lambda: capturar_guardar_mostrar(captura2, etiqueta_ruta.cget("text").split(": "), entrada_nombre.get(), label_captura2, 2, entrada_tiempo_captura.get(), entrada_cantidad_capturas.get(), entrada_intervalo_capturas.get()))
boton_capturar2.place(x=470, y=720, width=120, height=30)

# Cuadros de imagen grises
# Camara 1
label_imagen1 = tk.Label(ventana, background="gray")
label_imagen1.place(x=50, y=50, width=300, height=250)
label_muestraImagen1 = tk.Label(ventana, text="Muestra de camara 1:")
label_muestraImagen1.place(x=50, y=30, width=300, height=20)
# Camara 2
label_imagen2 = tk.Label(ventana, background="gray")
label_imagen2.place(x=390, y=50, width=300, height=250)
label_muestraImagen2 = tk.Label(ventana, text="Muestra de camara 2:")
label_muestraImagen2.place(x=390, y=30, width=300, height=20)

# Cuadros de imagen capturada
# Camara 1
label_captura1 = tk.Label(ventana, background="gray")
label_captura1.place(x=50, y=450, width=300, height=250)
label_muestraCaptura1 = tk.Label(ventana, text="Muestra de captura camara 1:")
label_muestraCaptura1.place(x=50, y=430, width=300, height=20)
# Camara 2
label_captura2 = tk.Label(ventana, background="gray")
label_captura2.place(x=390, y=450, width=300, height=250)
label_muestraCaptura2 = tk.Label(ventana, text="Muestra de captura camara 2:")
label_muestraCaptura2.place(x=390, y=430, width=300, height=20)

# Elementos de captura automatica
# Titulo para saber donde esta el cuadro de texto de tiempo de captura
label_timepo_captura = tk.Label(ventana, text="Tiempo de captura (segundos):")
label_timepo_captura.place(x=50, y=770, width=200, height=20)
# Cuadro de texto para ingresar el tiempo de captura
entrada_tiempo_captura = tk.Entry(ventana)
entrada_tiempo_captura.place(x=240, y=770, width=20, height=20)
entrada_tiempo_captura.insert(0, "0")
# Titulo para saber donde esta el cuadro de texto de cantidad de capturas
label_cantidad_capturas = tk.Label(ventana, text="Cantidad de capturas:")
label_cantidad_capturas.place(x=260, y=770, width=200, height=20)
# Cuadro de texto para ingresar la cantidad de capturas
entrada_cantidad_capturas = tk.Entry(ventana)
entrada_cantidad_capturas.place(x=420, y=770, width=20, height=20)
entrada_cantidad_capturas.insert(0, "1")
# Titulo para saber donde esta el cuadro de texto de intervalo de capturas
label_intervalo_capturas = tk.Label(ventana, text="Intervalo de capturas (ms):")
label_intervalo_capturas.place(x=460, y=770, width=200, height=20)
# Cuadro de texto para ingresar el intervalo de capturas
entrada_intervalo_capturas = tk.Entry(ventana)
entrada_intervalo_capturas.place(x=650, y=770, width=30, height=20)
entrada_intervalo_capturas.insert(0, "1000")

# Iniciar la ventana
ventana.mainloop()
