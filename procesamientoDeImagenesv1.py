import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import imutils
import cv2
import os
import serial.tools.list_ports

# Variables globales a utilizar para la captura
captura1 = None
captura2 = None
arduino = None

# Funcion para obtener los puertos disponibles de arduino
def obtener_puertos_disponibles():
    puertos_disponibles = [
        port.device for port in serial.tools.list_ports.comports()
    ]
    return puertos_disponibles

# Funcion para conectar a arduino
def conectar_arduino(numero_puerto, label_estado):
    try:
        arduino = serial.Serial(port=numero_puerto, baudrate=9600, timeout=1)
        label_estado.config(
            text=f"Conectado a Arduino en el puerto {numero_puerto}")
        return arduino
    except Exception as e:
        arduino = None
        label_estado.config(
            text=f"No se pudo conectar a Arduino en el puerto {numero_puerto}")
        return None

# Funcion para desconectar arduino
def desconectar_arduino(arduino, label_estado):
    if arduino is not None:
        arduino.close()
        label_estado.config(text="Arduino desconectado")


def conectar_desconectar_arduino():
    puerto_seleccionado = combobox_arduino.get()
    global arduino
    if not puerto_seleccionado or puerto_seleccionado == "Selecciona un puerto":
        label_estado.config(text="Selecciona un puerto")
        return
    if arduino is None:
        arduino = conectar_arduino(puerto_seleccionado, label_estado)
        if arduino:
            boton_conectar_desconectar.config(text="Desconectar")
    else:
        desconectar_arduino(arduino, label_estado)
        arduino = None
        boton_conectar_desconectar.config(text="Conectar")

def enviar_datos_arduino(velocidad, posicion, letra, arduino, label_estado):
    try:
        datos = f"{velocidad},{posicion},{letra}"
        arduino.write(datos.encode())
        label_estado.config(text=f"Datos enviados: {datos}")
    except Exception as e:
        label_estado.config(text=f"Error al enviar datos: {e}")

def enviar_datos_arduino_desde_ui():
    velocidad = int(entrada_velocidad.get())
    posicion = int(entrada_posicion.get())
    letra = int(entrada_letra.get())

    enviar_datos_arduino(velocidad, posicion, letra, arduino, label_estado)

# Función para obtener la lista de cámaras conectadas
def obtener_camaras_disponibles():
    camaras_disponibles = []
    for i in range(5):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            camaras_disponibles.append(f"Camara {i}")
            cap.release()
    return camaras_disponibles

# Función para iniciar la cámara
def iniciar_captura(captura, label_imagen):
    if captura is not None:
        ret, frame = captura.read()
        if ret:
            frame = imutils.resize(frame, width=311)
            frame = imutils.resize(frame, height=241)
            imagen_camara = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(imagen_camara)
            img_tk = ImageTk.PhotoImage(image=img)
            label_imagen.configure(image=img_tk)
            label_imagen.image = img_tk
            label_imagen.after(10, lambda: iniciar_captura(captura, label_imagen))
        else:
            label_imagen.image = ""
            captura.release()

# Función para capturar y guardar la imagen
def capturar_guardar_mostrar(captura, carpeta_destino, nombre_archivo, label_captura):
    if captura is not None:
        ret, frame = captura.read()
        if ret:
            frame = imutils.resize(frame, width=311)
            frame = imutils.resize(frame, height=241)
            imagen_captura = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(imagen_captura)
            img_tk = ImageTk.PhotoImage(image=img)
            label_captura.configure(image=img_tk)
            label_captura.image = img_tk
            ruta_completa = os.path.join(carpeta_destino, f"{nombre_archivo}.png")
            cv2.imwrite(ruta_completa, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            print(f"Captura guardada en: {ruta_completa}")
        else:
            print("No se pudo realizar la captura")

# Funciones para conectar la cámara seleccionada
def conectar_camara_1(numero_camara, label_imagen):
    try:
        global captura1
        captura1 = cv2.VideoCapture(numero_camara, cv2.CAP_DSHOW)
        if captura1.isOpened():
            print(f"Conectado a la cámara {numero_camara}")
            iniciar_captura(captura1, label_imagen)
            boton_conectar1.config(state=tk.DISABLED)
            boton_desconectar1.config(state=tk.NORMAL)
        else:
            print(f"No se pudo conectar a la cámara {numero_camara}")
    except Exception as e:
        print(f"Error al conectar a la cámara {numero_camara}: {e}")

def desconectar_camara_1():
    global captura1
    if captura1 is not None:
        captura1.release()
        print("Cámara desconectada")
        boton_conectar1.config(state=tk.NORMAL)
        boton_desconectar1.config(state=tk.DISABLED)

def conectar_camara_2(numero_camara, label_imagen):
    try:
        global captura2
        captura2 = cv2.VideoCapture(numero_camara, cv2.CAP_DSHOW)
        if captura2.isOpened():
            print(f"Conectado a la cámara {numero_camara}")
            iniciar_captura(captura2, label_imagen)
            boton_conectar2.config(state=tk.DISABLED)
            boton_desconectar2.config(state=tk.NORMAL)
        else:
            print(f"No se pudo conectar a la cámara {numero_camara}")
    except Exception as e:
        print(f"Error al conectar a la cámara {numero_camara}: {e}")

def desconectar_camara_2():
    global captura2
    if captura2 is not None:
        captura2.release()
        print("Cámara desconectada")
        boton_conectar2.config(state=tk.NORMAL)
        boton_desconectar2.config(state=tk.DISABLED)

# Función para seleccionar la carpeta de destino y el nombre del archivo
def seleccionar_destino():
    carpeta_destino = filedialog.askdirectory()
    entrada_nombre.delete(0, tk.END)  # Limpiar la entrada
    entrada_nombre.insert(0, "nombre_archivo")  # Establecer un nombre predeterminado
    etiqueta_ruta.config(text=carpeta_destino)

def cerrar_ventana():
    if captura1 is not None:
        captura1.release()
    if captura2 is not None:
        captura2.release()
    ventana.destroy()

# Configuración de la ventana
ventana = tk.Tk()
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
ventana.geometry(f"{int(ancho_pantalla * 0.8)}x{int(alto_pantalla * 0.8)}")
ventana.title("Proyecto procesamiento de imagen con webcam")
ventana.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# Lista de cámaras disponibles
lista_camaras = obtener_camaras_disponibles()

# Combobox y botón para la primera cámara
combobox_camara1 = ttk.Combobox(ventana, values=lista_camaras)
combobox_camara1.set("Selecciona una cámara")
combobox_camara1.place(x=75, y=330, width=200, height=23)

# Combobox y botón para la segunda cámara
combobox_camara2 = ttk.Combobox(ventana, values=lista_camaras)
combobox_camara2.set("Selecciona una cámara")
combobox_camara2.place(x=415, y=330, width=200, height=23)

# Botones para conectar cámaras y capturar imágenes
boton_conectar1 = tk.Button(ventana, text="Conectar", command=lambda: conectar_camara_1(combobox_camara1.current(), label_imagen1))
boton_conectar1.place(x=50, y=370, width=120, height=30)

boton_desconectar1 = tk.Button(ventana, text="Desconectar", command=desconectar_camara_1, state=tk.DISABLED)
boton_desconectar1.place(x=180, y=370, width=120, height=30)

boton_conectar2 = tk.Button(ventana, text="Conectar", command=lambda: conectar_camara_2(combobox_camara2.current(), label_imagen2))
boton_conectar2.place(x=390, y=370, width=120, height=30)

boton_desconectar2 = tk.Button(ventana, text="Desconectar", command=desconectar_camara_2, state=tk.DISABLED)
boton_desconectar2.place(x=520, y=370, width=120, height=30)

boton_capturar = tk.Button(ventana, text="Capturar", command=lambda: capturar_guardar_mostrar(captura2, etiqueta_ruta.cget("text").split(": ")[1], entrada_nombre.get(), label_captura))
boton_capturar.place(x=820, y=370, width=120, height=30)

# Etiqueta y botón para seleccionar la carpeta de destino
etiqueta_ruta = tk.Label(ventana, text="Carpeta de destino:", wraplength=300, justify="left")
etiqueta_ruta.place(x=200, y=460, width=300, height=40)

boton_seleccionar = tk.Button(ventana, text="Seleccionar carpeta", command=seleccionar_destino)
boton_seleccionar.place(x=50, y=460, width=150, height=30)

# Entrada para el nombre del archivo
etiqueta_nombre = tk.Label(ventana, text="Nombre del archivo:")
etiqueta_nombre.place(x=50, y=500, width=150, height=20)

entrada_nombre = tk.Entry(ventana)
entrada_nombre.place(x=190, y=500, width=150, height=30)
entrada_nombre.insert(0, "nombre_archivo")

# Cuadros de Imagen grises
label_imagen1 = tk.Label(ventana, background="gray")
label_imagen1.place(x=50, y=50, width=300, height=250)

label_imagen2 = tk.Label(ventana, background="gray")
label_imagen2.place(x=390, y=50, width=300, height=250)

# Cuadros de Imagen capturada
label_captura = tk.Label(ventana, background="gray")
label_captura.place(x=730, y=50, width=300, height=250)

# Obtener puertos de Arduino disponibles
puertos_arduino = obtener_puertos_disponibles()

# Combobox y botón para conectar a Arduino
combobox_arduino = ttk.Combobox(ventana, values=puertos_arduino)
combobox_arduino.set("Selecciona un puerto")
combobox_arduino.place(x=50, y=550, width=200, height=23)

# Boton para conectar y desconectar Arduino
boton_conectar_desconectar = tk.Button(ventana,text="Conectar")
boton_conectar_desconectar.place(x=50, y=600, width=120, height=30)
boton_conectar_desconectar.bind("<Button-1>", lambda event: conectar_desconectar_arduino())

# Etiqueta para mostrar el estado de la conexión
label_estado = tk.Label(ventana, text="", wraplength=200, justify="left")
label_estado.place(x=190, y=600, width=200, height=30)

label_velocidad = tk.Label(ventana, text="Velocidad:")
label_velocidad.place(x=50, y=630, width=150, height=20)

entrada_velocidad = tk.Entry(ventana)
entrada_velocidad.place(x=50, y=650, width=150, height=30)

label_posicion = tk.Label(ventana, text="Posición:")
label_posicion.place(x=210, y=630, width=150, height=20)

entrada_posicion = tk.Entry(ventana)
entrada_posicion.place(x=210, y=650, width=150, height=30)

label_letra = tk.Label(ventana, text="Letra:")
label_letra.place(x=370, y=630, width=150, height=20)

entrada_letra = tk.Entry(ventana)
entrada_letra.place(x=370, y=650, width=150, height=30)

boton_enviar = tk.Button(ventana,
                         text="Enviar",
                         command=enviar_datos_arduino_desde_ui)
boton_enviar.place(x=530, y=650, width=120, height=30)

# Iniciar la ventana
ventana.mainloop()
