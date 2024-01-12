import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import imutils
import cv2
import os
import serial.tools.list_ports
import time
import threading

# Variables globales a utilizar
captura1 = None
captura2 = None
arduino = None
velocidades_predefinidas = [60]
rotacion_completa = 5868
angulos_predefinidos = [10, 15, 20, 30, 40, 45, 60, 90, 120, 180, 360]
captura_en_proceso = True

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
def capturar_guardar_mostrar(captura, nombre_archivo, label_captura, camara_numero):
    global captura_en_proceso
    angulo_seleccionado = int(combobox_angulos.get())

    if angulo_seleccionado not in [10, 15, 20, 30, 40, 45, 60, 90, 120, 180, 360]:
        print("Ángulo no válido")
        return

    cantidad_capturas = 360 / angulo_seleccionado
    tiempo_captura = 26 / cantidad_capturas

    for i in range(int(cantidad_capturas)):
        if not captura_en_proceso:
            break

        ret, frame = captura.read()
        if ret:
            frame = imutils.resize(frame, width=311)
            frame = imutils.resize(frame, height=241)
            imagen_captura = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            img = Image.fromarray(imagen_captura)
            img_tk = ImageTk.PhotoImage(image=img)
            label_captura.configure(image=img_tk)
            label_captura.image = img_tk
            ruta_completa = os.path.join(etiqueta_ruta.cget("text"), f"{nombre_archivo}_camara{camara_numero}_{i + 1}.png")
            cv2.imwrite(ruta_completa, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
            print(f"Captura de camara {camara_numero}, imagen {i + 1} guardada en: {ruta_completa}")
            seleccion = combobox_velocidades.get()
            if seleccion:
                velocidad_seleccionada = int(seleccion)
                enviar_datos_arduino(velocidad_seleccionada, rotacion_completa, arduino, label_estado)

            ventana.update()
            time.sleep(tiempo_captura)
        else:
            print(f"No se pudo realizar la captura de camara {camara_numero}")
            break
    captura_en_proceso = False

def reiniciar_captura():
    global captura_en_proceso
    captura_en_proceso = True

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

# Función para obtener los puertos disponibles de Arduino
def obtener_puertos_disponibles():
    puertos_disponibles = [port.device for port in serial.tools.list_ports.comports()]
    return puertos_disponibles

# Función para conectar a Arduino
def conectar_arduino(numero_puerto, label_estado):
    try:
        arduino = serial.Serial(port=numero_puerto, baudrate=9600, timeout=1)
        label_estado.config(text=f"Conectado a Arduino en el puerto {numero_puerto}")
        return arduino
    except Exception as e:
        arduino = None
        label_estado.config(text=f"No se pudo conectar a Arduino en el puerto {numero_puerto}")
        return None

# Función para desconectar Arduino
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

# Funcion para enviar los datos al arduino de la mesa giratoria
def enviar_datos_arduino(velocidad, posicion, arduino, label_estado):
    try:
        datos = f"{velocidad},{posicion}"
        arduino.write(datos.encode())
        label_estado.config(text=f"Datos enviados: {datos}")
    except Exception as e:
        label_estado.config(text=f"Error al enviar datos: {e}")

# Funcion para obtener los datos que se van a enviar
def enviar_datos_arduino_desde_ui():
    seleccion = combobox_velocidades.get()
    if seleccion:
        velocidad_seleccionada = int(seleccion)
        enviar_datos_arduino(velocidad_seleccionada, rotacion_completa, arduino, label_estado)

# Funcion para detener el giro
def dato_detencion_giratoria():
    try:
        dato_detencion = 0
        global arduino
        if arduino is not None:
            datos = f"{dato_detencion}"
            arduino.write(datos.encode())
            label_estado.config(text=f"Dato de detencion enviado")
        else:
            label_estado.config(text="Arduino no esta conectado")
    except Exception as e:
        label_estado.config(text=f"Error al enviar dato de detencion")

# Funcion para dejar la mesa en el punto 0
def dato_calibracion_mesa():
    try:
        dato_calibracion = 2
        global arduino
        if arduino is not None:
            datos = f"{dato_calibracion}"
            arduino.write(datos.encode())
            label_estado.config(text="Calibrando la mesa")
        else:
            label_estado.config(text="Arduino no conectado")
    except Exception as e:
        label_estado.config(text=f"Error al enviar los datos de calibracion")

# Obtener puertos de Arduino disponibles
puertos_arduino = obtener_puertos_disponibles()

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
boton_capturar1 = tk.Button(ventana, text="Capturar", command=lambda: threading.Thread(target=lambda: capturar_guardar_mostrar(captura1, entrada_nombre.get(),label_captura1,1)).start())
boton_capturar1.place(x=130, y=720, width=120, height=30)
# Conexion camara 2
boton_conectar2 = tk.Button(ventana, text="Conectar", command=lambda: conectar_camara_2(combobox_camara2.current(), label_imagen2))
boton_conectar2.place(x=390, y=370, width=120, height=30)
# Desconexion camara 2
boton_desconectar2 = tk.Button(ventana, text="Desconectar", command=desconectar_camara_2, state=tk.DISABLED)
boton_desconectar2.place(x=520, y=370, width=120, height=30)
# Captura camara 2
boton_capturar2 = tk.Button(ventana, text="Capturar", command=lambda: threading.Thread(target=lambda: capturar_guardar_mostrar(captura2, entrada_nombre.get(),label_captura2,2)).start())
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

# Elementos de conexion con Arduino
# Combobox y boton para conectar a Arduino
label_conexion_arduino = tk.Label(ventana, text="Conexión con Arduino:")
label_conexion_arduino.place(x=700, y=30, width=200, height=20)
combobox_arduino = ttk.Combobox(ventana, values=puertos_arduino, state="readonly")
combobox_arduino.set("Selecciona un puerto")
combobox_arduino.place(x=700, y=50, width=200, height=23)

# Boton para conectar y desconectar Arduino
boton_conectar_desconectar = tk.Button(ventana,text="Conectar")
boton_conectar_desconectar.place(x=910, y=50, width=120, height=30)
boton_conectar_desconectar.bind("<Button-1>", lambda event: conectar_desconectar_arduino())

# Etiqueta para mostrar el estado de la conexión
label_estado = tk.Label(ventana, text="Conecte el arduino", wraplength=200, justify="left")
label_estado.place(x=700, y=80, width=200, height=30)

# Elementos para enviar datos a Arduino
# Boton para enviar datos a Arduino
boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_datos_arduino_desde_ui)
boton_enviar.place(x=740, y=220, width=120, height=30)
# Boton para pausar la rotacion
boton_enviar_detencion = tk.Button(ventana, text="Detener", command=dato_detencion_giratoria)
boton_enviar_detencion.place(x=740, y=250, width=120, height=30)
# Boton para calibrar la mesa
boton_calibracion = tk.Button(ventana, text="Calibrar", command=dato_calibracion_mesa)
boton_calibracion.place(x=740, y=280, width=120, height=30)

# Titulo indicativo de envio de datos
label_datos = tk.Label(ventana, text="Envio de datos para giro")
label_datos.place(x=700, y=130, width=200, height=20)

# Titulo para saber donde esta el combobox de texto de velocidad
label_velocidad = tk.Label(ventana, text="Velocidad:")
label_velocidad.place(x=700, y=160, width=150, height=20)
# Combo box para seleccionar la velocidad
combobox_velocidades = ttk.Combobox(ventana, values=velocidades_predefinidas, state="readonly")
combobox_velocidades.set("Selecciona una velocidad")
combobox_velocidades.place(x=820, y=160, width=160, height=20)

# Titulo para saber donde esta el combobox de angulo
label_angulo = tk.Label(ventana, text="Angulo:")
label_angulo.place(x=700, y=190, width=150, height=20)
# Combo box para seleccionar el angulo
combobox_angulos = ttk.Combobox(ventana, values=angulos_predefinidos, state="readonly")
combobox_angulos.set("Selecciona un angulo")
combobox_angulos.place(x=820, y=190, width=160, height=20)

# Boton para reiniciar el bool
boton_reiniciar_captura = tk.Button(ventana, text="Reiniciar",command=reiniciar_captura)
boton_reiniciar_captura.place(x=280, y=720, width=150, height=30)

# Iniciar la ventana
ventana.mainloop()
