from pathlib import Path
import json

import tkinter as tk
from tkinter import messagebox


# =================
# Clases
# =================

class Producto:
    def __init__(self, id, nombre, marca, stock, precio, estado):
        self.id = id
        self.nombre = nombre
        self.marca = marca
        self.stock = stock
        self.precio = precio
        self.estado = estado

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Nombre: {self.nombre}\n"
            f"Marca: {self.marca}\n"
            f"Stock: {self.stock}\n"
            f"Precio: {self.precio}\n"
            f"Estado: {self.estado}"
        )


class PlacaDeVideo(Producto):
    def __init__(self, id, nombre, marca, stock, precio, estado, vram, chipset, consumo_wats):
        super().__init__(id, nombre, marca, stock, precio, estado)  # El super llama a la clase contructuro Producto
        self.vram = vram
        self.chipset = chipset
        self.consumo_wats = consumo_wats

    def __str__(self):
        return (
            super().__str__()
            + f"\nVRAM: {self.vram} GB"
            + f"\nChipset: {self.chipset}"
            + f"\nConsumo: {self.consumo_wats} W"
        )


class Procesador(Producto):
    def __init__(self, id, nombre, marca, stock, precio, estado, hilos, frecuencia, socket):
        super().__init__(id, nombre, marca, stock, precio, estado)
        self.hilos = hilos
        self.frecuencia = frecuencia
        self.socket = socket

    def __str__(self):
        return (
            super().__str__()
            + f"\nHilos: {self.hilos}"
            + f"\nFrecuencia: {self.frecuencia}"
            + f"\nSocket: {self.socket}"
        )


class Ram(Producto):
    def __init__(self, id, nombre, marca, stock, precio, estado, capacidad_gb, velocidad_mhz, tipo):
        super().__init__(id, nombre, marca, stock, precio, estado)
        self.capacidad_gb = capacidad_gb
        self.velocidad_mhz = velocidad_mhz
        self.tipo = tipo

    def __str__(self):  # con esto se mostrarán tanto los datos heredados de Producto como los específicos de cada componente.
        return (
            super().__str__()
            + f"\nCapacidad: {self.capacidad_gb} GB"
            + f"\nVelocidad: {self.velocidad_mhz} MHZ"
            + f"\nTipo: {self.tipo}"
        )


class Disco(Producto):
    def __init__(self, id, nombre, marca, stock, precio, estado, capacidad_gb, tipo, velocidad):
        super().__init__(id, nombre, marca, stock, precio, estado)
        self.capacidad_gb = capacidad_gb
        self.tipo = tipo
        self.velocidad = velocidad

    def __str__(self):
        return (
            super().__str__()
            + f"\nCapacidad: {self.capacidad_gb} GB"
            + f"\nTipo: {self.tipo}"
            + f"\nVelocidad: {self.velocidad}"
        )


class Pendrive(Producto):
    def __init__(self, id, nombre, marca, stock, precio, estado, capacidad, tipo_usb):
        super().__init__(id, nombre, marca, stock, precio, estado)
        self.capacidad = capacidad
        self.tipo_usb = tipo_usb

    def __str__(self):
        return (
            super().__str__()
            + f"\nCapacidad: {self.capacidad} GB"
            + f"\nTipo de USB: {self.tipo_usb}"
        )


# =================
# Inventario
# =================

# -----------------
# Write_json
# -----------------

path = Path("./Paradigma de Programacion/Python/Trabajo Practico N°2/data.json")

# Pregunta si el archivo existe y si no existe lo crea

path.parent.mkdir(parents=True, exist_ok=True)
'''
parent → obtiene la carpeta donde va a estar data.json.
mkdir() → crea la carpeta.
parents=True → crea también las carpetas superiores que falten.
exist_ok=True → no da error si ya existen.
'''


if path.exists():
    with open(path, "r", encoding="utf-8") as archivo:
        data = json.load(archivo)
else:
    data = {
        "PlacaDeVideo": [],
        "Procesador": [],
        "Ram": [],
        "Disco": [],
        "Pendrive": []
    }
    with open(path, "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4)


# =================
# Funciones
# =================


def agregar_procesador():

    # validacion de campos vacios
    if (
        not entry_id.get()
        or not entry_nombre.get()
        or not entry_marca.get()
        or not entry_stock.get()
        or not entry_precio.get()
        or not entry_estado.get()
        or not entry_hilos.get()
        or not entry_frecuencia.get()
        or not entry_socket.get()
    ):
        messagebox.showerror(
            "Error",
            "Todos los campos son obligatorios."
        )
        return

    try:  # esto es para q no haya errores si ingresa un numero donde no va

        procesador = {
            "id": int(entry_id.get()),
            "nombre": entry_nombre.get(),
            "marca": entry_marca.get(),
            "stock": int(entry_stock.get()),
            "precio": float(entry_precio.get()),
            "estado": entry_estado.get(),
            "hilos": int(entry_hilos.get()),
            "frecuencia": float(entry_frecuencia.get()),
            "socket": entry_socket.get()
        }

    except ValueError:

        messagebox.showerror(
            "Error",
            "ID, Stock, Precio, Hilos y Frecuencia deben ser numéricos."
        )

        return

    # guardar en la estructura de datos
    data["Procesador"].append(procesador)

    # Guardar en el json

    with open(path, "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4, ensure_ascii=False)

    messagebox.showinfo(
        "Exito",
        "Procesador agregado correctamente"
    )

    # limpiar campos
    entry_id.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_marca.delete(0, tk.END)
    entry_stock.delete(0, tk.END)
    entry_precio.delete(0, tk.END)
    entry_estado.delete(0, tk.END)
    entry_hilos.delete(0, tk.END)
    entry_frecuencia.delete(0, tk.END)
    entry_socket.delete(0, tk.END)


# mas funciones de subventanas

def abrir_agregar_procesador():

    global entry_id
    global entry_nombre
    global entry_marca
    global entry_stock
    global entry_precio
    global entry_estado
    global entry_hilos
    global entry_frecuencia
    global entry_socket

    ventana_proc = tk.Toplevel()
    ventana_proc.title("Agregar Procesador")
    ventana_proc.geometry("400x500")

    tk.Label(ventana_proc, text="ID").pack()
    entry_id = tk.Entry(ventana_proc)
    entry_id.pack()

    tk.Label(ventana_proc, text="Nombre").pack()
    entry_nombre = tk.Entry(ventana_proc)
    entry_nombre.pack()

    tk.Label(ventana_proc, text="Marca").pack()
    entry_marca = tk.Entry(ventana_proc)
    entry_marca.pack()

    tk.Label(ventana_proc, text="Stock").pack()
    entry_stock = tk.Entry(ventana_proc)
    entry_stock.pack()

    tk.Label(ventana_proc, text="Precio").pack()
    entry_precio = tk.Entry(ventana_proc)
    entry_precio.pack()

    tk.Label(ventana_proc, text="Estado").pack()  # ver si puedo poner un voton que cambie el color de las letras diciendo que estaba actividado o no 
    entry_estado = tk.Entry(ventana_proc)
    entry_estado.pack()

    tk.Label(ventana_proc, text="Hilos").pack()
    entry_hilos = tk.Entry(ventana_proc)
    entry_hilos.pack()

    tk.Label(ventana_proc, text="Frecuencia").pack()
    entry_frecuencia = tk.Entry(ventana_proc)
    entry_frecuencia.pack()

    tk.Label(ventana_proc, text="Socket").pack()
    entry_socket = tk.Entry(ventana_proc)
    entry_socket.pack()

    tk.Button(
        ventana_proc,
        text="Guardar",
        command=agregar_procesador
    ).pack(pady=10)


def abrir_agregar_ram():
    pass


def abrir_agregar_disco():
    pass


def abrir_agregar_placa():
    pass


def abrir_agregar_pendrive():
    pass


# Funciones para ventanas

def abrir_agregar():

    ventana_tipo = tk.Toplevel()
    ventana_tipo.title("Tipo de producto")

    tk.Button(
        ventana_tipo,
        text="Procesador",
        command=abrir_agregar_procesador
    ).pack(pady=5)

    tk.Button(
        ventana_tipo,
        text="RAM",
        command=abrir_agregar_ram
    ).pack(pady=5)

    tk.Button(
        ventana_tipo,
        text="Disco",
        command=abrir_agregar_disco
    ).pack(pady=5)

    tk.Button(
        ventana_tipo,
        text="Placa de Video",
        command=abrir_agregar_placa
    ).pack(pady=5)

    tk.Button(
        ventana_tipo,
        text="Pendrive",
        command=abrir_agregar_pendrive
    ).pack(pady=5)


def abrir_eliminar():
    pass


def abrir_buscar():
    pass


def abrir_guardar():
    pass


# =================
# Tkinter
# =================

ventana = tk.Tk()
ventana.title("Inventario")
ventana.geometry("300x250")

tk.Button(
    ventana,
    text="Agregar Producto",
    command=abrir_agregar
).pack(pady=10)

tk.Button(
    ventana,
    text="Eliminar Producto",
    command=abrir_eliminar
).pack(pady=10)

tk.Button(
    ventana,
    text="Buscar Producto",
    command=abrir_buscar
).pack(pady=10)

tk.Button(
    ventana,
    text="Guardar Producto",
    command=abrir_guardar
).pack(pady=10)  # sin esto el boton no aparece en venatana

ventana.mainloop()