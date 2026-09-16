import json
from math import prod
from pathlib import Path
from datetime import date

from re import M
import tkinter as tk    
from tkinter import ttk  # Importante: ttk contiene el widget Combobox
from tkinter import messagebox

import random

# =================
# Clases
# =================
class persona:
    def __init__(self, nombre, apellido, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni

    def __str__(self):
        return (
            f"Nombre: {self.nombre}\n"
            f"Apellido: {self.apellido}\n"
            f"DNI: {self.dni}"
        )

class empleado(persona):
    def __init__(self, nombre, apellido, dni, usuario, clave):
        super().__init__(nombre, apellido, dni)
        self.usuario = usuario
        self.clave = clave

    def __str__(self):
        return (
            super().__str__()
            + f"\nUsuario: {self.usuario}"
            + f"\nClave: {self.clave}"
        )


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
        super().__init__(id, nombre, marca, stock, precio, estado)
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

    def __str__(self):
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


class cliente(persona):
    def __init__(self, nombre, apellido, dni, direccion, telefono):
        super().__init__(nombre, apellido, dni)
        self.direccion = direccion
        self.telefono = telefono

    def __str__(self):
        return (
            super().__str__()
            + f"\nDirección: {self.direccion}"
            + f"\nTeléfono: {self.telefono}"
        )

class Venta:
    def __init__(self, id_venta, producto, cantidad, empleado_nombre, fecha):
        self.id_venta = id_venta
        self.producto = producto
        self.cantidad = cantidad
        self.empleado_nombre = empleado_nombre
        self.fecha = fecha
        self.total = producto.precio * cantidad

    def registrar_venta(self):
        if self.producto.stock >= self.cantidad:
            self.producto.stock -= self.cantidad
            return True
        return False

# =================
# Inventario y JSON
# =================

path = Path(__file__).parent / "data.json"
path.parent.mkdir(parents=True, exist_ok=True)

empleado_logueado = None  

if path.exists():
    with open(path, "r", encoding="utf-8") as archivo:
        data = json.load(archivo)
else:
    data = {
        "PlacaDeVideo": [],
        "Procesador": [],
        "Ram": [],
        "Disco": [],
        "Pendrive": [],
        "usuarios": [
            {
                "dni": "12345678",
                "nombre": "Juan",
                "apellido": "Perez",
                "usuario": "juanp",
                "clave": "1234"
            }
        ],
        "Ventas": [],
    }
    with open(path, "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4)

def guardar_json():
    with open(path, "w", encoding="utf-8") as archivo:
        json.dump(data, archivo, indent=4, ensure_ascii=False)


# =================
# Estructura Principal
# =================

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventario")

        self.contenedor = tk.Frame(self)
        self.contenedor.pack(fill="both", expand=True)

        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

        self.pantallas = {}

        for PantallaClase in (MenuPrincipal, PantallaAgregarPendrive,PantallaAgregarPlacaDeVideo, PantallaAgregarProducto,PantallaAgregarDisco, PantallaAgregarRAM, PantallaAgregarProcesador, PantallaRegistrarVenta):
            pantalla = PantallaClase(parent=self.contenedor, controlador=self)
            self.pantallas[PantallaClase] = pantalla
            pantalla.grid(row=0, column=0, sticky="nsew")

        self.withdraw()
        self.abrir_login()

    def mostrar_pantalla(self, pantalla_clase):
        pantalla = self.pantallas[pantalla_clase]
        self.geometry(pantalla.dimensiones)
        pantalla.tkraise()

    def actualizar_operador(self):
        if empleado_logueado:
            self.pantallas[MenuPrincipal].lbl_usuario.config(
                text=f"Operador: {empleado_logueado.nombre} {empleado_logueado.apellido}"
            )

    def abrir_login(self):
        ventana_login = tk.Toplevel(self)
        ventana_login.title("Login")
        ventana_login.geometry("300x200")

        tk.Label(ventana_login, text="Usuario").pack(pady=2)
        entry_usuario = tk.Entry(ventana_login)
        entry_usuario.pack(pady=2)

        tk.Label(ventana_login, text="Clave").pack(pady=2)
        entry_clave = tk.Entry(ventana_login, show="*")
        entry_clave.pack(pady=2)

        def validar():
            global empleado_logueado
            u = entry_usuario.get().strip()
            c = entry_clave.get().strip()

            for usr in data.get("usuarios", []):
                if usr["usuario"] == u and usr["clave"] == c:
                    empleado_logueado = empleado(
                        nombre=usr.get("nombre", ""),
                        apellido=usr.get("apellido", ""),
                        dni=usr.get("dni", ""),
                        usuario=usr["usuario"],
                        clave=usr["clave"]
                    )

                    messagebox.showinfo("Bienvenido", f"Sesión iniciada como: {empleado_logueado.nombre} {empleado_logueado.apellido}")
                    self.actualizar_operador()
                    ventana_login.destroy()
                    self.deiconify()
                    self.mostrar_pantalla(MenuPrincipal)
                    return

            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

        tk.Button(ventana_login, text="Ingresar", command=validar).pack(pady=15)
        ventana_login.protocol("WM_DELETE_WINDOW", self.destroy)


# =================
# Vistas con Tamaños Definidos
# =================

class MenuPrincipal(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "320x350"

        self.lbl_usuario = tk.Label(self, text="Operador: No autenticado", font=("Arial", 10, "italic"))
        self.lbl_usuario.pack(pady=10)

        tk.Button(
            self,
            text="Agregar Producto",
            command=lambda: controlador.mostrar_pantalla(PantallaAgregarProducto)
        ).pack(pady=5)

        tk.Button(self, 
                 text="Eliminar Producto", command=lambda: None).pack(pady=5)
        tk.Button(self, text="Buscar Producto", command=lambda: None).pack(pady=5)
        
        tk.Button(
            self, 
            text="Registrar Venta", 
            command=lambda: controlador.mostrar_pantalla(PantallaRegistrarVenta)
        ).pack(pady=5)
        
        tk.Button(self, text="Ver Ventas Realizadas", command=self.ver_ventas).pack(pady=5)

    def ver_ventas(self):
        ventana_listado = tk.Toplevel(self)
        ventana_listado.title("Historial de Ventas")
        ventana_listado.geometry("450x300")

        txt = tk.Text(ventana_listado)
        txt.pack(fill=tk.BOTH, expand=True)

        if not data["Ventas"]:
            txt.insert(tk.END, "No hay ventas registradas todavía.")
        else:
            for v in data["Ventas"]:
                txt.insert(
                    tk.END,
                    f"Venta #{v['id_venta']} | Fecha: {v['fecha']}\n"
                    f"Producto: {v['producto']} x{v['cantidad']}\n"
                    f"Total: ${v['total']:.2f} | Atendido por: {v['vendedor']}\n"
                    f"{'-'*45}\n"
                )


class PantallaAgregarProducto(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "300x280"

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=10)

        btn_regresar = tk.Button(
            barra_superior, 
            text="← Regresar", 
            command=lambda: controlador.mostrar_pantalla(MenuPrincipal)
        )
        btn_regresar.pack(side="left")

        tk.Label(self, text="Seleccione Tipo de Producto", font=("Arial", 11, "bold")).pack(pady=10)

        tk.Button(
            self,
            text="Procesador",
            command=lambda: controlador.mostrar_pantalla(PantallaAgregarProcesador)
        ).pack(pady=4)

        tk.Button(
            self, 
            text="RAM", 
            command=lambda: controlador.mostrar_pantalla(PantallaAgregarRAM)
        ).pack(pady=4)

        tk.Button(
            self, 
            text="Disco", 
            command=lambda: controlador.mostrar_pantalla(PantallaAgregarDisco)
            ).pack(pady=4)
        
        tk.Button(
            self,
            text="Placa de Video", 
            command=lambda: controlador.mostrar_pantalla(PantallaAgregarPlacaDeVideo)
            ).pack(pady=4)
        
        tk.Button(
            self, 
            text="Pendrive", 
            command=lambda: controlador.mostrar_pantalla(PantallaAgregarPendrive)
            ).pack(pady=4)


class PantallaAgregarProcesador(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "380x500"

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=5)

        btn_regresar = tk.Button(
            barra_superior, 
            text="← Regresar", 
            command=lambda: controlador.mostrar_pantalla(PantallaAgregarProducto)
        )
        btn_regresar.pack(side="left")

        tk.Label(self, text="Agregar Procesador", font=("Arial", 11, "bold")).pack(pady=2)

        tk.Label(self, text="ID", font=("Arial", 10, "bold")).pack()

        self.entry_id = tk.Entry(self, justify="center")
        self.entry_id.pack()

        self.entry_id.insert(0, str(generar_id_unico()))
        self.entry_id.config(state="readonly")

        tk.Label(self, text="Nombre").pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        tk.Label(self, text="Marca").pack()
        self.entry_marca = tk.Entry(self)
        self.entry_marca.pack()

        tk.Label(self, text="Stock").pack()
        self.entry_stock = tk.Entry(self)
        self.entry_stock.pack()

        tk.Label(self, text="Precio").pack()
        self.entry_precio = tk.Entry(self)
        self.entry_precio.pack()

        tk.Label(self, text="Estado").pack()
        self.entry_estado = tk.Entry(self)
        self.entry_estado.pack()

        tk.Label(self, text="Hilos").pack()
        self.entry_hilos = tk.Entry(self)
        self.entry_hilos.pack()

        tk.Label(self, text="Frecuencia").pack()
        self.entry_frecuencia = tk.Entry(self)
        self.entry_frecuencia.pack()

        tk.Label(self, text="Socket").pack()
        self.entry_socket = tk.Entry(self)
        self.entry_socket.pack()

        tk.Button(self, text="Guardar", command=self.agregar_procesador).pack(pady=10)

    def agregar_procesador(self):
        if (
            not self.entry_nombre.get()
            or not self.entry_marca.get()
            or not self.entry_stock.get()
            or not self.entry_precio.get()
            or not self.entry_estado.get()
            or not self.entry_hilos.get()
            or not self.entry_frecuencia.get()
            or not self.entry_socket.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            procesador = {
                "id": generar_id_unico(),
                "nombre": self.entry_nombre.get(),
                "marca": self.entry_marca.get(),
                "stock": int(self.entry_stock.get()),
                "precio": float(self.entry_precio.get()),
                "estado": self.entry_estado.get(),
                "hilos": int(self.entry_hilos.get()),
                "frecuencia": float(self.entry_frecuencia.get()),
                "socket": self.entry_socket.get()
            }
        except ValueError:
            messagebox.showerror("Error", "ID, Stock, Precio, Hilos y Frecuencia deben ser numéricos.")
            return

        data["Procesador"].append(procesador)
        guardar_json()

        messagebox.showinfo("Éxito", "Procesador agregado correctamente")

        self.entry_nombre.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_estado.delete(0, tk.END)
        self.entry_hilos.delete(0, tk.END)
        self.entry_frecuencia.delete(0, tk.END)
        self.entry_socket.delete(0, tk.END)

class PantallaAgregarRAM(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "380x500"

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=5)

        btn_regresar = tk.Button(
            barra_superior,
            text="← Regresar",
            command=lambda: controlador.mostrar_pantalla(PantallaAgregarProducto)
        )
        btn_regresar.pack(side="left")

        tk.Label(self, text="Agregar RAM", font=("Arial", 11, "bold")).pack(pady=2)

        tk.Label(self, text="ID").pack()

        self.entry_id = tk.Entry(self, justify="center")
        self.entry_id.pack()

        self.entry_id.insert(0, str(generar_id_unico()))
        self.entry_id.config(state="readonly")

        tk.Label(self, text="Nombre").pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        tk.Label(self, text="Marca").pack()
        self.entry_marca = tk.Entry(self)
        self.entry_marca.pack()

        tk.Label(self, text="Stock").pack()
        self.entry_stock = tk.Entry(self)
        self.entry_stock.pack()

        tk.Label(self, text="Precio").pack()
        self.entry_precio = tk.Entry(self)
        self.entry_precio.pack()

        tk.Label(self, text="Estado").pack()
        self.entry_estado = tk.Entry(self)
        self.entry_estado.pack()

        tk.Label(self, text="Capacidad").pack()
        self.entry_capacidad = tk.Entry(self)
        self.entry_capacidad.pack()

        tk.Label(self, text="Velocidad").pack()
        self.entry_velocida_mhz = tk.Entry(self)
        self.entry_velocida_mhz.pack()

        tk.Label(self, text="Tipo").pack()
        self.entry_tipo = tk.Entry(self)
        self.entry_tipo.pack()

        tk.Button(self, text="Guardar", command=self.agregar_ram).pack(pady=10)

    def agregar_ram(self):
        if(
            
            not self.entry_nombre.get()
            or not self.entry_marca.get()
            or not self.entry_stock.get()
            or not self.entry_precio.get()
            or not self.entry_estado.get()
            or not self.entry_capacidad.get()
            or not self.entry_velocida_mhz.get()
            or not self.entry_tipo.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            ram = {
                "id": generar_id_unico(),
                "nombre": self.entry_nombre.get(),
                "marca": self.entry_marca.get(),
                "stock": int(self.entry_stock.get()),
                "precio": float(self.entry_precio.get()),
                "estado": self.entry_estado.get(),
                "capacidad": int(self.entry_capacidad.get()),
                "velocidad_mhz": float(self.entry_velocida_mhz.get()),
                "tipo": self.entry_tipo.get()
            }
        except ValueError:
            messagebox.showerror("Error", "ID, Stock, Precio, Capacidad y Velocidad deben ser numericos.")
            return
        
        data["RAM"].append(ram)
        guardar_json()

        messagebox.showinfo("Éxito", "La RAM se agregado correctamente")

        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_estado.delete(0, tk.END)
        self.entry_capacidad.delete(0, tk.END)
        self.entry_velocida_mhz.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        
class PantallaAgregarDisco(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "380x500"

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=5)

        btn_regresar = tk.Button(
            barra_superior,
            text="← Regresar",
            command=lambda: controlador.mostrar_pantalla(PantallaAgregarProducto)
        )
        btn_regresar.pack(side="left")

        tk.Label(self, text="Agregar Disco", font=("Arial", 11, "bold")).pack(pady=2)

        tk.Label(self, text="ID").pack()

        self.entry_id = tk.Entry(self, justify="center")
        self.entry_id.pack()

        self.entry_id.insert(0, str(generar_id_unico()))
        self.entry_id.config(state="readonly")

        tk.Label(self, text="Nombre").pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        tk.Label(self, text="Marca").pack()
        self.entry_marca = tk.Entry(self)
        self.entry_marca.pack()

        tk.Label(self, text="Stock").pack()
        self.entry_stock = tk.Entry(self)
        self.entry_stock.pack()

        tk.Label(self, text="Precio").pack()
        self.entry_precio = tk.Entry(self)
        self.entry_precio.pack()

        tk.Label(self, text="Estado").pack()
        self.entry_estado = tk.Entry(self)
        self.entry_estado.pack()

        tk.Label(self, text="Capacidad").pack()
        self.entry_capacidad_mb = tk.Entry(self)
        self.entry_capacidad_mb.pack()

        tk.Label(self, text="Tipo").pack()
        self.entry_tipo = tk.Entry(self)
        self.entry_tipo.pack()

        tk.Label(self, text="Velocidad").pack()
        self.entry_velocidad = tk.Entry(self)
        self.entry_velocidad.pack()

        tk.Button(self, text="Guardar", command=self.agregar_disco).pack(pady=10)

    def agregar_disco(self):
        if(
            
            not self.entry_nombre.get()
            or not self.entry_marca.get()
            or not self.entry_stock.get()
            or not self.entry_precio.get()
            or not self.entry_estado.get()
            or not self.entry_capacidad_mb.get()
            or not self.entry_tipo.get()
            or not self.entry_velocidad.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            disco = {
                "id": generar_id_unico(),
                "nombre": self.entry_nombre.get(),
                "marca": self.entry_marca.get(),
                "stock": int(self.entry_stock.get()),
                "precio": float(self.entry_precio.get()),
                "estado": self.entry_estado.get(),
                "capacidad": int(self.entry_capacidad_mb.get()),
                "tipo": self.entry_tipo.get(),
                "velocidad_mb": float(self.entry_velocidad.get()),  

            }
        except ValueError:
            messagebox.showerror("Error", "ID, Stock, Precio, Capacidad y velocidad deben ser numericos.")
            return

        data["Disco"].append(disco)
        guardar_json()

        messagebox.showinfo("Éxito", "El Disco se agregado correctamente")

        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_estado.delete(0, tk.END)
        self.entry_capacidad_mb.delete(0, tk.END)
        self.entry_tipo.delete(0, tk.END)
        self.entry_velocidad.delete(0, tk.END)



class PantallaRegistrarVenta(tk.Frame): 
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "360x320"

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=10)

        btn_regresar = tk.Button(
            barra_superior,
            text="← Regresar",
            command=lambda: controlador.mostrar_pantalla(MenuPrincipal)
        )
        btn_regresar.pack(side="left")

        tk.Label(self, text="Registrar Venta", font=("Arial", 11, "bold")).pack(pady=5)

        tk.Label(self, text="Categoría de producto").pack(pady=2)

        # Filtramos las llaves del JSON dejando solo las categorías de productos válidas
        categorias_validas = [k for k in data.keys() if k not in ("usuarios", "Ventas")]

        # Lista desplegable (Combobox) con 'state="readonly"' para evitar tipeo
        self.combo_cat = ttk.Combobox(self, values=categorias_validas, state="readonly")
        if categorias_validas:
            self.combo_cat.current(0)  # Selecciona el primer elemento por defecto
        self.combo_cat.pack(pady=2)

        tk.Label(self, text="ID del Producto").pack(pady=2)
        self.entry_id_p = tk.Entry(self)
        self.entry_id_p.pack(pady=2)

        tk.Label(self, text="Cantidad").pack(pady=2)
        self.entry_cant = tk.Entry(self)
        self.entry_cant.pack(pady=2)

        tk.Button(self, text="Confirmar Venta", command=self.procesar_venta).pack(pady=15)

    def procesar_venta(self):
        cat = self.combo_cat.get().strip()  # Lee el valor seleccionado de la desplegable
        
        if not cat:
            messagebox.showerror("Error", "Seleccione una categoría.")
            return

        try:
            id_p = int(self.entry_id_p.get())
            cant = int(self.entry_cant.get())
        except ValueError:
            messagebox.showerror("Error", "ID y Cantidad deben ser numéricos.")
            return

        if cat not in data:
            messagebox.showerror("Error", "Categoría de producto no válida.")
            return

        producto_encontrado = None
        for p in data[cat]:
            if p["id"] == id_p:
                producto_encontrado = p
                break

        if not producto_encontrado:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        if producto_encontrado["stock"] < cant:
            messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto_encontrado['stock']}")
            return

        producto_encontrado["stock"] -= cant
        total = producto_encontrado["precio"] * cant
        id_venta = len(data["Ventas"]) + 1

        data["Ventas"].append({
            "id_venta": id_venta,
            "producto": producto_encontrado["nombre"],
            "cantidad": cant,
            "total": total,
            "vendedor": empleado_logueado.nombre if empleado_logueado else "Desconocido",
            "fecha": str(date.today())
        })

        guardar_json()
        messagebox.showinfo("Éxito", f"Venta realizada.\nTotal: ${total:.2f}")

        self.entry_id_p.delete(0, tk.END)
        self.entry_cant.delete(0, tk.END)
        self.controlador.mostrar_pantalla(MenuPrincipal)

class PantallaAgregarPlacaDeVideo(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "380x500"

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=5)

        btn_regresar = tk.Button(
            barra_superior, 
            text="← Regresar", 
            command=lambda: controlador.mostrar_pantalla(PantallaAgregarProducto)
        )
        btn_regresar.pack(side="left")

        tk.Label(self, text="Agregar Placa de Video", font=("Arial", 11, "bold")).pack(pady=2)

        tk.Label(self, text="ID", font=("Arial", 10, "bold")).pack()

        self.entry_id = tk.Entry(self, justify="center")
        self.entry_id.pack()

        self.entry_id.insert(0, str(generar_id_unico()))
        self.entry_id.config(state="readonly")

        tk.Label(self, text="Nombre").pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        tk.Label(self, text="Marca").pack()
        self.entry_marca = tk.Entry(self)
        self.entry_marca.pack()

        tk.Label(self, text="Stock").pack()
        self.entry_stock = tk.Entry(self)
        self.entry_stock.pack()

        tk.Label(self, text="Precio").pack()
        self.entry_precio = tk.Entry(self)
        self.entry_precio.pack()

        tk.Label(self, text="Estado").pack()
        self.entry_estado = tk.Entry(self)
        self.entry_estado.pack()

        tk.Label(self, text="Vram").pack()
        self.entry_vram = tk.Entry(self)
        self.entry_vram.pack()

        tk.Label(self, text="Chipset").pack()
        self.entry_chipset = tk.Entry(self)
        self.entry_chipset.pack()

        tk.Label(self, text="Consumo").pack()
        self.entry_consumo_wats = tk.Entry(self)
        self.entry_consumo_wats.pack()

        tk.Button(self, text="Guardar", command=self.agregar_placadevideo).pack(pady=10)

    def agregar_placadevideo(self):
        if (
            not self.entry_nombre.get()
            or not self.entry_marca.get()
            or not self.entry_stock.get()
            or not self.entry_precio.get()
            or not self.entry_estado.get()
            or not self.entry_vram.get()
            or not self.entry_chipset.get()
            or not self.entry_consumo_wats.get()
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            placadevideo = {
                "id": generar_id_unico(),
                "nombre": self.entry_nombre.get(),
                "marca": self.entry_marca.get(),
                "stock": int(self.entry_stock.get()),
                "precio": float(self.entry_precio.get()),
                "estado": self.entry_estado.get(),
                "vram": int(self.entry_vram.get()),
                "chipset": self.entry_chipset.get(),
                "consumo": float(self.entry_consumo_wats.get())
            }
        except ValueError:
            messagebox.showerror("Error", "ID, Stock, Precio, Vram y Comsumo deben ser numéricos.")
            return

        data["PlacaDeVideo"].append(PlacaDeVideo)
        guardar_json()

        messagebox.showinfo("Éxito", "Placa de Video agregado correctamente")

        self.entry_nombre.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_estado.delete(0, tk.END)
        self.entry_vram.delete(0, tk.END)
        self.entry_chipset.delete(0, tk.END)
        self.entry_consumo_wats.delete(0, tk.END)


class PantallaAgregarPendrive(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "380x500"

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=5)

        btn_regresar = tk.Button(
            barra_superior, 
            text="← Regresar", 
            command=lambda: controlador.mostrar_pantalla(PantallaAgregarProducto)
        )
        btn_regresar.pack(side="left")

        tk.Label(self, text="Agregar Pendrive", font=("Arial", 11, "bold")).pack(pady=2)

        tk.Label(self, text="ID", font=("Arial", 10, "bold")).pack()

        self.entry_id = tk.Entry(self, justify="center")
        self.entry_id.pack()

        self.entry_id.insert(0, str(generar_id_unico()))
        self.entry_id.config(state="readonly")

        tk.Label(self, text="Nombre").pack()
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.pack()

        tk.Label(self, text="Marca").pack()
        self.entry_marca = tk.Entry(self)
        self.entry_marca.pack()

        tk.Label(self, text="Stock").pack()
        self.entry_stock = tk.Entry(self)
        self.entry_stock.pack()

        tk.Label(self, text="Precio").pack()
        self.entry_precio = tk.Entry(self)
        self.entry_precio.pack()

        tk.Label(self, text="Estado").pack()
        self.entry_estado = tk.Entry(self)
        self.entry_estado.pack()

        tk.Label(self, text="Capacidad").pack()
        self.entry_capacidad = tk.Entry(self)
        self.entry_capacidad.pack()

        tk.Label(self, text="Tipo").pack()
        self.entry_tipo_usb = tk.Entry(self)
        self.entry_tipo_usb.pack()

        tk.Button(self, text="Guardar", command=self.agregar_pendrive).pack(pady=10)

    def agregar_pendrive(self):
        if (
            not self.entry_nombre.get()
            or not self.entry_marca.get()
            or not self.entry_stock.get()
            or not self.entry_precio.get()
            or not self.entry_estado.get()
            or not self.entry_capacidad.get()
            or not self.entry_tipo_usb.get()
            
        ):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            procesador = {
                "id": generar_id_unico(),
                "nombre": self.entry_nombre.get(),
                "marca": self.entry_marca.get(),
                "stock": int(self.entry_stock.get()),
                "precio": float(self.entry_precio.get()),
                "estado": self.entry_estado.get(),
                "Capacidad": int(self.entry_capacidad.get()),
                "Tipo": self.entry_tipo_usb.get()
            }
        except ValueError:
            messagebox.showerror("Error", "ID, Stock, Precio y Capacidad deben ser numéricos.")
            return

        data["Pendrive"].append(Pendrive)
        guardar_json()

        messagebox.showinfo("Éxito", "Pendrive agregado correctamente")

        self.entry_nombre.delete(0, tk.END)
        self.entry_marca.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_estado.delete(0, tk.END)
        self.entry_capacidad.delete(0, tk.END)
        self.entry_tipo_usb.delete(0, tk.END)

def generar_id_unico():
    max_id = 0

    for categoria in ["Procesador", "Ram", "Disco","PlacaDeVideo","Pendrive"]:
        for producto in data.get(categoria, []):
            if producto["id"] > max_id:
                max_id = producto["id"]
    return max_id + 1 


if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()