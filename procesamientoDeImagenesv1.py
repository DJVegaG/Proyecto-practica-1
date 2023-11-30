import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import imutils
import cv2
import os

# Variables globales a utilizar para la captura
captura1 = None
captura2 = None

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
def capturar_guardar(captura, carpeta_destino, nombre_archivo):
    if captura is not None:
        ret, frame = captura.read()
        if ret:
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
ventana.geometry("750x800")
ventana.resizable(0, 0)
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

boton_capturar2 = tk.Button(ventana, text="Capturar", command=lambda: capturar_guardar(captura2, etiqueta_ruta.cget("text").split(": ")[1], entrada_nombre.get()))
boton_capturar2.place(x=450, y=410, width=120, height=30)

# Etiqueta y botón para seleccionar la carpeta de destino
etiqueta_ruta = tk.Label(ventana, text="Carpeta de destino:")
etiqueta_ruta.place(x=50, y=500, width=600, height=20)

boton_seleccionar = tk.Button(ventana, text="Seleccionar carpeta", command=seleccionar_destino)
boton_seleccionar.place(x=50, y=460, width=150, height=30)

# Entrada para el nombre del archivo
etiqueta_nombre = tk.Label(ventana, text="Nombre del archivo:")
etiqueta_nombre.place(x=50, y=650, width=150, height=20)

entrada_nombre = tk.Entry(ventana)
entrada_nombre.place(x=210, y=645, width=150, height=30)
entrada_nombre.insert(0, "nombre_archivo")

# Cuadros de Imagen grises
label_imagen1 = tk.Label(ventana, background="gray")
label_imagen1.place(x=50, y=50, width=300, height=250)

label_imagen2 = tk.Label(ventana, background="gray")
label_imagen2.place(x=390, y=50, width=300, height=250)

# Iniciar la ventana
ventana.mainloop()
