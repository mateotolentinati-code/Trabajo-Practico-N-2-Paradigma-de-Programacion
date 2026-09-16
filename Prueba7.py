import json
import os
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import messagebox, ttk


# ==========================================
# 1. CLASES DE DOMINIO (Encapsuladas)
# ==========================================

class Persona:
    def __init__(self, nombre: str, apellido: str, dni: str):
        self._nombre = nombre.strip()
        self._apellido = apellido.strip()
        self._dni = str(dni).strip()

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, valor: str):
        if not valor.strip():
            raise ValueError("El apellido no puede estar vacío.")
        self._apellido = valor.strip()

    @property
    def dni(self):
        return self._dni

    def __str__(self):
        return f"Nombre: {self._nombre}\nApellido: {self._apellido}\nDNI: {self._dni}"


class Empleado(Persona):
    def __init__(self, nombre: str, apellido: str, dni: str, usuario: str, clave: str, rol: str = "Vendedor"):
        super().__init__(nombre, apellido, dni)
        self._usuario = usuario.strip()
        self._clave = clave.strip()
        self._rol = rol.strip()

    @property
    def usuario(self):
        return self._usuario

    @property
    def clave(self):
        return self._clave

    @property
    def rol(self):
        return self._rol

    def a_dict(self):
        return {
            "dni": self._dni,
            "nombre": self._nombre,
            "apellido": self._apellido,
            "usuario": self._usuario,
            "clave": self._clave,
            "rol": self._rol
        }

    @classmethod
    def desde_dict(cls, data: dict):
        return cls(
            nombre=data.get("nombre", ""),
            apellido=data.get("apellido", ""),
            dni=data.get("dni", ""),
            usuario=data.get("usuario", ""),
            clave=data.get("clave", ""),
            rol=data.get("rol", "Vendedor")
        )

    def __str__(self):
        return super().__str__() + f"\nUsuario: {self._usuario}\nRol: {self._rol}"


class Producto:
    def __init__(self, id_prod: int, nombre: str, marca: str, stock: int, precio: float, estado: str = "Activo"):
        self._id = int(id_prod)
        self._nombre = nombre.strip()
        self._marca = marca.strip()
        self._precio = float(precio)
        self._stock = int(stock)
        self._estado = estado if self._stock > 0 else "Inactivo"

    @property
    def id(self):
        return self._id

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = valor.strip()

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, valor: str):
        if not valor.strip():
            raise ValueError("La marca no puede estar vacía.")
        self._marca = valor.strip()

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor: int):
        val = int(valor)
        if val < 0:
            raise ValueError("El stock no puede ser negativo.")
        self._stock = val
        if self._stock == 0:
            self._estado = "Inactivo"

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor: float):
        val = float(valor)
        if val < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._precio = val

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor: str):
        if valor not in ("Activo", "Inactivo"):
            raise ValueError("Estado no válido. Debe ser 'Activo' o 'Inactivo'.")
        if valor == "Activo" and self._stock == 0:
            raise ValueError("No se puede activar un producto con stock 0.")
        self._estado = valor

    def a_dict(self):
        return {
            "id": self._id,
            "nombre": self._nombre,
            "marca": self._marca,
            "stock": self._stock,
            "precio": self._precio,
            "estado": self._estado,
        }

    def __str__(self):
        return (
            f"ID: {self._id}\n"
            f"Nombre: {self._nombre}\n"
            f"Marca: {self._marca}\n"
            f"Stock: {self._stock}\n"
            f"Precio: ${self._precio:.2f}\n"
            f"Estado: {self._estado}"
        )


class PlacaDeVideo(Producto):
    def __init__(self, id_prod: int, nombre: str, marca: str, stock: int, precio: float, estado: str, vram: int, chipset: str, consumo_wats: float):
        super().__init__(id_prod, nombre, marca, stock, precio, estado)
        self.vram = vram
        self.chipset = chipset
        self.consumo_wats = consumo_wats

    @property
    def vram(self):
        return self._vram

    @vram.setter
    def vram(self, valor: int):
        if int(valor) <= 0:
            raise ValueError("La VRAM debe ser mayor a 0.")
        self._vram = int(valor)

    @property
    def consumo_wats(self):
        return self._consumo_wats

    @consumo_wats.setter
    def consumo_wats(self, valor: float):
        if float(valor) <= 0:
            raise ValueError("El consumo en Watts debe ser positivo.")
        self._consumo_wats = float(valor)

    def a_dict(self):
        data = super().a_dict()
        data.update({
            "vram": self._vram,
            "chipset": self.chipset,
            "consumo_wats": self._consumo_wats
        })
        return data

    @classmethod
    def desde_dict(cls, d: dict):
        return cls(d["id"], d["nombre"], d["marca"], d["stock"], d["precio"], d.get("estado", "Activo"), d["vram"], d["chipset"], d["consumo_wats"])


class Procesador(Producto):
    def __init__(self, id_prod: int, nombre: str, marca: str, stock: int, precio: float, estado: str, hilos: int, frecuencia: float, socket: str):
        super().__init__(id_prod, nombre, marca, stock, precio, estado)
        self.hilos = hilos
        self.frecuencia = frecuencia
        self.socket = socket

    @property
    def hilos(self):
        return self._hilos

    @hilos.setter
    def hilos(self, valor: int):
        if int(valor) <= 0:
            raise ValueError("Los hilos deben ser mayores a 0.")
        self._hilos = int(valor)

    @property
    def frecuencia(self):
        return self._frecuencia

    @frecuencia.setter
    def frecuencia(self, valor: float):
        if float(valor) <= 0:
            raise ValueError("La frecuencia debe ser positiva.")
        self._frecuencia = float(valor)

    def a_dict(self):
        data = super().a_dict()
        data.update({
            "hilos": self._hilos,
            "frecuencia": self._frecuencia,
            "socket": self.socket
        })
        return data

    @classmethod
    def desde_dict(cls, d: dict):
        return cls(d["id"], d["nombre"], d["marca"], d["stock"], d["precio"], d.get("estado", "Activo"), d["hilos"], d["frecuencia"], d["socket"])


class Ram(Producto):
    def __init__(self, id_prod: int, nombre: str, marca: str, stock: int, precio: float, estado: str, capacidad_gb: int, velocidad_mhz: float, tipo: str):
        super().__init__(id_prod, nombre, marca, stock, precio, estado)
        self.capacidad_gb = capacidad_gb
        self.velocidad_mhz = velocidad_mhz
        self.tipo = tipo

    @property
    def capacidad_gb(self):
        return self._capacidad_gb

    @capacidad_gb.setter
    def capacidad_gb(self, valor: int):
        if int(valor) <= 0:
            raise ValueError("La capacidad debe ser mayor a 0 GB.")
        self._capacidad_gb = int(valor)

    def a_dict(self):
        data = super().a_dict()
        data.update({
            "capacidad_gb": self._capacidad_gb,
            "velocidad_mhz": self.velocidad_mhz,
            "tipo": self.tipo
        })
        return data

    @classmethod
    def desde_dict(cls, d: dict):
        return cls(d["id"], d["nombre"], d["marca"], d["stock"], d["precio"], d.get("estado", "Activo"), d["capacidad_gb"], d["velocidad_mhz"], d["tipo"])


class Disco(Producto):
    def __init__(self, id_prod: int, nombre: str, marca: str, stock: int, precio: float, estado: str, capacidad_gb: int, tipo: str, velocidad: float):
        super().__init__(id_prod, nombre, marca, stock, precio, estado)
        self.capacidad_gb = capacidad_gb
        self.tipo = tipo
        self.velocidad = velocidad

    def a_dict(self):
        data = super().a_dict()
        data.update({
            "capacidad_gb": self.capacidad_gb,
            "tipo": self.tipo,
            "velocidad": self.velocidad
        })
        return data

    @classmethod
    def desde_dict(cls, d: dict):
        return cls(d["id"], d["nombre"], d["marca"], d["stock"], d["precio"], d.get("estado", "Activo"), d["capacidad_gb"], d["tipo"], d["velocidad"])


class Pendrive(Producto):
    def __init__(self, id_prod: int, nombre: str, marca: str, stock: int, precio: float, estado: str, capacidad: int, tipo_usb: str):
        super().__init__(id_prod, nombre, marca, stock, precio, estado)
        self.capacidad = capacidad
        self.tipo_usb = tipo_usb

    def a_dict(self):
        data = super().a_dict()
        data.update({
            "capacidad": self.capacidad,
            "tipo_usb": self.tipo_usb
        })
        return data

    @classmethod
    def desde_dict(cls, d: dict):
        return cls(d["id"], d["nombre"], d["marca"], d["stock"], d["precio"], d.get("estado", "Activo"), d["capacidad"], d["tipo_usb"])


class Venta:
    def __init__(self, id_venta: int, producto_nombre: str, cantidad: int, total: float, vendedor: str, fecha: str):
        self._id_venta = id_venta
        self._producto_nombre = producto_nombre
        self._cantidad = cantidad
        self._total = total
        self._vendedor = vendedor
        self._fecha = fecha

    @property
    def id_venta(self):
        return self._id_venta

    @property
    def total(self):
        return self._total

    def a_dict(self):
        return {
            "id_venta": self._id_venta,
            "producto": self._producto_nombre,
            "cantidad": self._cantidad,
            "total": self._total,
            "vendedor": self._vendedor,
            "fecha": self._fecha,
        }

    @classmethod
    def desde_dict(cls, d: dict):
        return cls(
            id_venta=d["id_venta"],
            producto_nombre=d["producto"],
            cantidad=d["cantidad"],
            total=d["total"],
            vendedor=d.get("vendedor", "Desconocido"),
            fecha=d.get("fecha", str(date.today()))
        )


# ==========================================
# 2. CONTROLADOR Y PERSISTENCIA (Gestor)
# ==========================================

MAPPING_CLASES = {
    "Procesador": Procesador,
    "Ram": Ram,
    "Disco": Disco,
    "PlacaDeVideo": PlacaDeVideo,
    "Pendrive": Pendrive
}


class GestorInventario:
    def __init__(self, ruta_archivo="data.json"):
        self.path = Path(__file__).parent / ruta_archivo
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.productos = {cat: [] for cat in MAPPING_CLASES.keys()}
        self.usuarios = []
        self.ventas = []
        self.empleado_logueado = None
        self._cargar_datos()

    def _cargar_datos(self):
        if not self.path.exists():
            self.usuarios.append(Empleado("Juan", "Perez", "12345678", "admin", "1234", rol="Admin"))
            self.guardar()
            return

        with open(self.path, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.usuarios = [Empleado.desde_dict(u) for u in data.get("usuarios", [])]

        for cat, clase in MAPPING_CLASES.items():
            self.productos[cat] = [clase.desde_dict(item) for item in data.get(cat, [])]

        self.ventas = [Venta.desde_dict(v) for v in data.get("Ventas", [])]

    def guardar(self):
        data = {
            "usuarios": [u.a_dict() for u in self.usuarios],
            "Ventas": [v.a_dict() for v in self.ventas]
        }
        for cat in MAPPING_CLASES.keys():
            data[cat] = [p.a_dict() for p in self.productos[cat]]

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.flush()
            os.fsync(file.fileno())

    def autenticar(self, usuario, clave):
        for usr in self.usuarios:
            if usr.usuario == usuario and usr.clave == clave:
                self.empleado_logueado = usr
                return True
        return False

    def generar_id_unico(self) -> int:
        max_id = 0
        for lista_prod in self.productos.values():
            for prod in lista_prod:
                if prod.id > max_id:
                    max_id = prod.id
        return max_id + 1

    def agregar_producto(self, categoria: str, producto: Producto):
        if categoria in self.productos:
            self.productos[categoria].append(producto)
            self.guardar()

    def buscar_producto_por_id(self, categoria: str, id_prod: int) -> Producto:
        for prod in self.productos.get(categoria, []):
            if prod.id == id_prod:
                return prod
        return None

    def registrar_venta(self, categoria: str, id_prod: int, cantidad: int):
        if not self.empleado_logueado:
            raise PermissionError("Debe haber una sesión iniciada para realizar ventas.")

        producto = self.buscar_producto_por_id(categoria, id_prod)
        if not producto:
            raise ValueError("Producto no encontrado.")

        if producto.estado != "Activo":
            raise ValueError("No se puede vender un producto inactivo.")

        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente. Disponible: {producto.stock}")

        producto.stock -= cantidad

        total = producto.precio * cantidad
        nueva_venta = Venta(
            id_venta=len(self.ventas) + 1,
            producto_nombre=producto.nombre,
            cantidad=cantidad,
            total=total,
            vendedor=self.empleado_logueado.nombre,
            fecha=str(date.today())
        )
        self.ventas.append(nueva_venta)
        self.guardar()


# ==========================================
# 3. INTERFAZ GRÁFICA DE USUARIO (Tkinter)
# ==========================================

class Aplicacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventario - Orientado a Objetos")
        self.gestor = GestorInventario()

        self.contenedor = tk.Frame(self)
        self.contenedor.pack(fill="both", expand=True)
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

        self.pantallas = {}

        for PantallaClase in (
            MenuPrincipal,
            PantallaAgregarProducto,
            PantallaAgregarProcesador,
            PantallaAgregarRAM,
            PantallaAgregarDisco,
            PantallaAgregarPlacaDeVideo,
            PantallaAgregarPendrive,
            PantallaModificarProducto,
            PantallaRegistrarVenta,
            PantallaBuscarProducto,
        ):
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
        emp = self.gestor.empleado_logueado
        if emp:
            self.pantallas[MenuPrincipal].lbl_usuario.config(
                text=f"Operador: {emp.nombre} {emp.apellido} ({emp.rol})"
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
            u = entry_usuario.get().strip()
            c = entry_clave.get().strip()

            if self.gestor.autenticar(u, c):
                emp = self.gestor.empleado_logueado
                messagebox.showinfo("Bienvenido", f"Sesión iniciada como: {emp.nombre} {emp.apellido}")
                self.actualizar_operador()
                ventana_login.destroy()
                self.deiconify()
                self.mostrar_pantalla(MenuPrincipal)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

        tk.Button(ventana_login, text="Ingresar", command=validar).pack(pady=15)
        ventana_login.protocol("WM_DELETE_WINDOW", self.destroy)

    def cerrar_sesion(self):
        self.gestor.empleado_logueado = None
        self.withdraw() # ocultar ventana principal 
        self.abrir_login()  #Abrir el dialogo de inicio de sesion

class MenuPrincipal(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "320x380"

        self.lbl_usuario = tk.Label(self, text="Operador: No autenticado", font=("Arial", 10, "italic"))
        self.lbl_usuario.pack(pady=10)

        self.btn_agregar = tk.Button(self, text="Agregar Producto", command=lambda: controlador.mostrar_pantalla(PantallaAgregarProducto))
        self.btn_agregar.pack(pady=5)

        self.btn_modificar = tk.Button(self, text="Modificar Producto", command=lambda: controlador.mostrar_pantalla(PantallaModificarProducto))
        self.btn_modificar.pack(pady=5)

        self.btn_buscar = tk.Button(self, text="Buscar Producto", command=lambda: controlador.mostrar_pantalla(PantallaBuscarProducto))
        self.btn_buscar.pack(pady=5)

        self.btn_venta = tk.Button(self, text="Registrar Venta", command=lambda: controlador.mostrar_pantalla(PantallaRegistrarVenta))
        self.btn_venta.pack(pady=5)

        self.btn_ver_ventas = tk.Button(self, text="Ver Ventas Realizadas", command=self.ver_ventas)
        self.btn_ver_ventas.pack(pady=5)

        self.btn_cerrar_sesion = tk.Button(
            self,
            text="Cerrar Sesion",
            fg="white",
            bg="#d9534f",
            command=controlador.cerrar_sesion
        )
        self.btn_cerrar_sesion.pack(pady=15)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.aplicar_permisos()

    def aplicar_permisos(self):
        emp = self.controlador.gestor.empleado_logueado
        if not emp:
            return

        self.lbl_usuario.config(
            text=f"Operador: {emp.nombre} {emp.apellido} ({emp.rol})"
        )

        if emp.rol == "Vendedor":
            self.btn_agregar.config(state="disabled")
            self.btn_modificar.config(state="disabled")
            self.btn_ver_ventas.config(state="disabled")
            self.btn_buscar.config(state="normal")
            self.btn_venta.config(state="normal")
        else:
            self.btn_agregar.config(state="normal")
            self.btn_modificar.config(state="normal")
            self.btn_ver_ventas.config(state="normal")
            self.btn_buscar.config(state="normal")
            self.btn_venta.config(state="normal")

    def ver_ventas(self):
        ventana_listado = tk.Toplevel(self)
        ventana_listado.title("Historial de Ventas")
        ventana_listado.geometry("450x300")

        txt = tk.Text(ventana_listado)
        txt.pack(fill=tk.BOTH, expand=True)

        ventas = self.controlador.gestor.ventas
        if not ventas:
            txt.insert(tk.END, "No hay ventas registradas todavía.")
        else:
            for v in ventas:
                txt.insert(
                    tk.END,
                    f"Venta #{v.id_venta} | Fecha: {v._fecha}\n"
                    f"Producto: {v._producto_nombre} x{v._cantidad}\n"
                    f"Total: ${v.total:.2f} | Atendido por: {v._vendedor}\n"
                    f"{'-'*45}\n"
                )


class PantallaAgregarProducto(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "300x280"

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=10)

        btn_regresar = tk.Button(barra_superior, text="← Regresar", command=lambda: controlador.mostrar_pantalla(MenuPrincipal))
        btn_regresar.pack(side="left")

        tk.Label(self, text="Seleccione Tipo de Producto", font=("Arial", 11, "bold")).pack(pady=10)

        tk.Button(self, text="Procesador", command=lambda: controlador.mostrar_pantalla(PantallaAgregarProcesador)).pack(pady=4)
        tk.Button(self, text="RAM", command=lambda: controlador.mostrar_pantalla(PantallaAgregarRAM)).pack(pady=4)
        tk.Button(self, text="Disco", command=lambda: controlador.mostrar_pantalla(PantallaAgregarDisco)).pack(pady=4)
        tk.Button(self, text="Placa de Video", command=lambda: controlador.mostrar_pantalla(PantallaAgregarPlacaDeVideo)).pack(pady=4)
        tk.Button(self, text="Pendrive", command=lambda: controlador.mostrar_pantalla(PantallaAgregarPendrive)).pack(pady=4)


class BasePantallaAgregar(tk.Frame):
    def __init__(self, parent, controlador, titulo: str):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "380x520"

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=5)

        btn_regresar = tk.Button(barra_superior, text="← Regresar", command=lambda: controlador.mostrar_pantalla(PantallaAgregarProducto))
        btn_regresar.pack(side="left")

        tk.Label(self, text=titulo, font=("Arial", 11, "bold")).pack(pady=2)

        tk.Label(self, text="ID", font=("Arial", 10, "bold")).pack()
        self.entry_id = tk.Entry(self, justify="center")
        self.entry_id.pack()

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

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.entry_id.config(state="normal")
        self.entry_id.delete(0, tk.END)
        self.entry_id.insert(0, str(self.controlador.gestor.generar_id_unico()))
        self.entry_id.config(state="readonly")


class PantallaAgregarProcesador(BasePantallaAgregar):
    def __init__(self, parent, controlador):
        super().__init__(parent, controlador, "Agregar Procesador")

        tk.Label(self, text="Hilos").pack()
        self.entry_hilos = tk.Entry(self)
        self.entry_hilos.pack()

        tk.Label(self, text="Frecuencia (GHz)").pack()
        self.entry_frecuencia = tk.Entry(self)
        self.entry_frecuencia.pack()

        tk.Label(self, text="Socket").pack()
        self.entry_socket = tk.Entry(self)
        self.entry_socket.pack()

        tk.Button(self, text="Guardar", command=self.guardar).pack(pady=10)

    def guardar(self):
        try:
            p = Procesador(
                id_prod=self.controlador.gestor.generar_id_unico(),
                nombre=self.entry_nombre.get(),
                marca=self.entry_marca.get(),
                stock=int(self.entry_stock.get()),
                precio=float(self.entry_precio.get()),
                estado="Activo",
                hilos=int(self.entry_hilos.get()),
                frecuencia=float(self.entry_frecuencia.get()),
                socket=self.entry_socket.get()
            )
            self.controlador.gestor.agregar_producto("Procesador", p)
            messagebox.showinfo("Éxito", "Procesador guardado exitosamente.")
            self.tkraise()
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))


class PantallaAgregarRAM(BasePantallaAgregar):
    def __init__(self, parent, controlador):
        super().__init__(parent, controlador, "Agregar Memoria RAM")

        tk.Label(self, text="Capacidad (GB)").pack()
        self.entry_capacidad = tk.Entry(self)
        self.entry_capacidad.pack()

        tk.Label(self, text="Velocidad (MHz)").pack()
        self.entry_velocidad = tk.Entry(self)
        self.entry_velocidad.pack()

        tk.Label(self, text="Tipo").pack()
        self.entry_tipo = tk.Entry(self)
        self.entry_tipo.pack()

        tk.Button(self, text="Guardar", command=self.guardar).pack(pady=10)

    def guardar(self):
        try:
            r = Ram(
                id_prod=self.controlador.gestor.generar_id_unico(),
                nombre=self.entry_nombre.get(),
                marca=self.entry_marca.get(),
                stock=int(self.entry_stock.get()),
                precio=float(self.entry_precio.get()),
                estado="Activo",
                capacidad_gb=int(self.entry_capacidad.get()),
                velocidad_mhz=float(self.entry_velocidad.get()),
                tipo=self.entry_tipo.get()
            )
            self.controlador.gestor.agregar_producto("Ram", r)
            messagebox.showinfo("Éxito", "RAM guardada exitosamente.")
            self.tkraise()
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))


class PantallaAgregarDisco(BasePantallaAgregar):
    def __init__(self, parent, controlador):
        super().__init__(parent, controlador, "Agregar Disco")

        tk.Label(self, text="Capacidad (GB)").pack()
        self.entry_capacidad = tk.Entry(self)
        self.entry_capacidad.pack()

        tk.Label(self, text="Tipo").pack()
        self.entry_tipo = tk.Entry(self)
        self.entry_tipo.pack()

        tk.Label(self, text="Velocidad").pack()
        self.entry_velocidad = tk.Entry(self)
        self.entry_velocidad.pack()

        tk.Button(self, text="Guardar", command=self.guardar).pack(pady=10)

    def guardar(self):
        try:
            d = Disco(
                id_prod=self.controlador.gestor.generar_id_unico(),
                nombre=self.entry_nombre.get(),
                marca=self.entry_marca.get(),
                stock=int(self.entry_stock.get()),
                precio=float(self.entry_precio.get()),
                estado="Activo",
                capacidad_gb=int(self.entry_capacidad.get()),
                tipo=self.entry_tipo.get(),
                velocidad=float(self.entry_velocidad.get())
            )
            self.controlador.gestor.agregar_producto("Disco", d)
            messagebox.showinfo("Éxito", "Disco guardado exitosamente.")
            self.tkraise()
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))


class PantallaAgregarPlacaDeVideo(BasePantallaAgregar):
    def __init__(self, parent, controlador):
        super().__init__(parent, controlador, "Agregar Placa de Video")

        tk.Label(self, text="VRAM (GB)").pack()
        self.entry_vram = tk.Entry(self)
        self.entry_vram.pack()

        tk.Label(self, text="Chipset").pack()
        self.entry_chipset = tk.Entry(self)
        self.entry_chipset.pack()

        tk.Label(self, text="Consumo (Watts)").pack()
        self.entry_consumo = tk.Entry(self)
        self.entry_consumo.pack()

        tk.Button(self, text="Guardar", command=self.guardar).pack(pady=10)

    def guardar(self):
        try:
            pv = PlacaDeVideo(
                id_prod=self.controlador.gestor.generar_id_unico(),
                nombre=self.entry_nombre.get(),
                marca=self.entry_marca.get(),
                stock=int(self.entry_stock.get()),
                precio=float(self.entry_precio.get()),
                estado="Activo",
                vram=int(self.entry_vram.get()),
                chipset=self.entry_chipset.get(),
                consumo_wats=float(self.entry_consumo.get())
            )
            self.controlador.gestor.agregar_producto("PlacaDeVideo", pv)
            messagebox.showinfo("Éxito", "Placa de video guardada exitosamente.")
            self.tkraise()
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))


class PantallaAgregarPendrive(BasePantallaAgregar):
    def __init__(self, parent, controlador):
        super().__init__(parent, controlador, "Agregar Pendrive")

        tk.Label(self, text="Capacidad (GB)").pack()
        self.entry_capacidad = tk.Entry(self)
        self.entry_capacidad.pack()

        tk.Label(self, text="Tipo USB").pack()
        self.entry_tipo_usb = tk.Entry(self)
        self.entry_tipo_usb.pack()

        tk.Button(self, text="Guardar", command=self.guardar).pack(pady=10)

    def guardar(self):
        try:
            p = Pendrive(
                id_prod=self.controlador.gestor.generar_id_unico(),
                nombre=self.entry_nombre.get(),
                marca=self.entry_marca.get(),
                stock=int(self.entry_stock.get()),
                precio=float(self.entry_precio.get()),
                estado="Activo",
                capacidad=int(self.entry_capacidad.get()),
                tipo_usb=self.entry_tipo_usb.get()
            )
            self.controlador.gestor.agregar_producto("Pendrive", p)
            messagebox.showinfo("Éxito", "Pendrive guardado exitosamente.")
            self.tkraise()
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))


class PantallaModificarProducto(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "850x700"
        self.producto_actual = None

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=10)

        btn_regresar = tk.Button(barra_superior, text="← Regresar", command=lambda: controlador.mostrar_pantalla(MenuPrincipal))
        btn_regresar.pack(side="left")

        frame_izq = tk.Frame(self)
        frame_izq.pack(side="left", padx=15, pady=10, fill="y")

        tk.Label(frame_izq, text="Modificar Producto", font=("Arial", 12, "bold")).pack(pady=5)
        tk.Label(frame_izq, text="Categoría").pack()

        categorias_validas = list(MAPPING_CLASES.keys())
        self.combo_cat = ttk.Combobox(frame_izq, values=categorias_validas, state="readonly", width=22)
        self.combo_cat.pack(pady=2)
        self.combo_cat.current(0)

        tk.Label(frame_izq, text="ID Producto").pack()
        self.entry_id_p = tk.Entry(frame_izq, width=15)
        self.entry_id_p.pack(pady=2)

        tk.Button(frame_izq, text="Cargar Datos", command=self.cargar_datos_producto).pack(pady=5)

        self.frame_campos = tk.Frame(frame_izq)
        self.frame_campos.pack(fill="both", expand=True, pady=5)

        self.btn_guardar = tk.Button(frame_izq, text="Guardar Cambios", command=self.guardar_modificacion, state="disabled")
        self.btn_guardar.pack(pady=10)

        frame_der = tk.Frame(self)
        frame_der.pack(side="right", fill="both", expand=True, padx=15, pady=10)

        tk.Label(frame_der, text="Productos Registrados", font=("Arial", 11, "bold")).pack()

        self.tree = ttk.Treeview(
            frame_der,
            columns=("ID", "Nombre", "Marca", "Stock", "Precio", "Estado"),
            show="headings",
            height=14
        )

        for col in ("ID", "Nombre", "Marca", "Stock", "Precio", "Estado"):
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Nombre", width=150)
        self.tree.column("Marca", width=100)
        self.tree.column("Stock", width=60, anchor="center")
        self.tree.column("Precio", width=80, anchor="center")
        self.tree.column("Estado", width=80, anchor="center")

        self.tree.tag_configure("inactivo", background="#ff9999", foreground="black")
        self.tree.pack(fill="both", expand=True)

        self.combo_cat.bind("<<ComboboxSelected>>", self.cargar_productos_tabla)
        self.tree.bind("<Double-1>", self.seleccionar_de_tabla)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.cargar_productos_tabla()

    def cargar_productos_tabla(self, event=None):
        self.tree.delete(*self.tree.get_children())
        cat = self.combo_cat.get()

        for p in self.controlador.gestor.productos.get(cat, []):
            tag = ("inactivo",) if p.estado == "Inactivo" else ()
            self.tree.insert("", "end", values=(p.id, p.nombre, p.marca, p.stock, f"${p.precio:.2f}", p.estado), tags=tag)

    def seleccionar_de_tabla(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = seleccion[0]
            valores = self.tree.item(item, "values")
            self.entry_id_p.delete(0, tk.END)
            self.entry_id_p.insert(0, valores[0])
            self.cargar_datos_producto()

    def cargar_datos_producto(self):
        cat = self.combo_cat.get()
        try:
            id_p = int(self.entry_id_p.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un ID válido.")
            return

        self.producto_actual = self.controlador.gestor.buscar_producto_por_id(cat, id_p)
        if not self.producto_actual:
            messagebox.showerror("Error", "Producto no encontrado.")
            return

        for child in self.frame_campos.winfo_children():
            child.destroy()

        self.entries_dinamicos = {}
        tk.Label(self.frame_campos, text="Estado").pack()
        self.combo_estado = ttk.Combobox(self.frame_campos, values=["Activo", "Inactivo"], state="readonly")
        self.combo_estado.pack()
        self.combo_estado.set(self.producto_actual.estado)

        campos_comunes = ["nombre", "marca", "stock", "precio"]
        campos_especificos = {
            "Procesador": ["hilos", "frecuencia", "socket"],
            "Ram": ["capacidad_gb", "velocidad_mhz", "tipo"],
            "Disco": ["capacidad_gb", "tipo", "velocidad"],
            "PlacaDeVideo": ["vram", "chipset", "consumo_wats"],
            "Pendrive": ["capacidad", "tipo_usb"]
        }

        todos = campos_comunes + campos_especificos.get(cat, [])
        for campo in todos:
            lbl_texto = campo.replace("_", " ").capitalize()
            tk.Label(self.frame_campos, text=lbl_texto, font=("Arial", 9)).pack()
            ent = tk.Entry(self.frame_campos)
            ent.insert(0, str(getattr(self.producto_actual, campo, "")))
            ent.pack()
            self.entries_dinamicos[campo] = ent

        self.btn_guardar.config(state="normal")

    def guardar_modificacion(self):
        if not self.producto_actual:
            return
        try:
            self.producto_actual.nombre = self.entries_dinamicos["nombre"].get()
            self.producto_actual.marca = self.entries_dinamicos["marca"].get()
            self.producto_actual.precio = float(self.entries_dinamicos["precio"].get())
            self.producto_actual.stock = int(self.entries_dinamicos["stock"].get())

            cat = self.combo_cat.get()
            if cat == "Procesador":
                self.producto_actual.hilos = int(self.entries_dinamicos["hilos"].get())
                self.producto_actual.frecuencia = float(self.entries_dinamicos["frecuencia"].get())
                self.producto_actual.socket = self.entries_dinamicos["socket"].get()
            elif cat == "Ram":
                self.producto_actual.capacidad_gb = int(self.entries_dinamicos["capacidad_gb"].get())
                self.producto_actual.velocidad_mhz = float(self.entries_dinamicos["velocidad_mhz"].get())
                self.producto_actual.tipo = self.entries_dinamicos["tipo"].get()
            elif cat == "Disco":
                self.producto_actual.capacidad_gb = int(self.entries_dinamicos["capacidad_gb"].get())
                self.producto_actual.tipo = self.entries_dinamicos["tipo"].get()
                self.producto_actual.velocidad = float(self.entries_dinamicos["velocidad"].get())
            elif cat == "PlacaDeVideo":
                self.producto_actual.vram = int(self.entries_dinamicos["vram"].get())
                self.producto_actual.chipset = self.entries_dinamicos["chipset"].get()
                self.producto_actual.consumo_wats = float(self.entries_dinamicos["consumo_wats"].get())
            elif cat == "Pendrive":
                self.producto_actual.capacidad = int(self.entries_dinamicos["capacidad"].get())
                self.producto_actual.tipo_usb = self.entries_dinamicos["tipo_usb"].get()

            self.producto_actual.estado = self.combo_estado.get()

            self.controlador.gestor.guardar()
            messagebox.showinfo("Éxito", "Producto modificado correctamente.")
            self.cargar_productos_tabla()
        except ValueError as e:
            messagebox.showerror("Error de validación", str(e))


class PantallaRegistrarVenta(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "850x450"

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=10)

        btn_regresar = tk.Button(barra_superior, text="← Regresar", command=lambda: controlador.mostrar_pantalla(MenuPrincipal))
        btn_regresar.pack(side="left")

        frame_izq = tk.Frame(self)
        frame_izq.pack(side="left", padx=15, pady=10)

        tk.Label(frame_izq, text="Registrar Venta", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(frame_izq, text="Categoría").pack()

        categorias_validas = list(MAPPING_CLASES.keys())
        self.combo_cat = ttk.Combobox(frame_izq, values=categorias_validas, state="readonly", width=20)
        self.combo_cat.pack(pady=5)
        self.combo_cat.current(0)

        tk.Label(frame_izq, text="ID del Producto").pack()
        self.entry_id_p = tk.Entry(frame_izq)
        self.entry_id_p.pack(pady=5)

        tk.Label(frame_izq, text="Cantidad").pack()
        self.entry_cant = tk.Entry(frame_izq)
        self.entry_cant.pack(pady=5)

        tk.Button(frame_izq, text="Confirmar Venta", command=self.procesar_venta).pack(pady=15)

        frame_der = tk.Frame(self)
        frame_der.pack(side="right", fill="both", expand=True, padx=15, pady=10)

        tk.Label(frame_der, text="Productos Disponibles", font=("Arial", 11, "bold")).pack()

        self.tree = ttk.Treeview(
            frame_der,
            columns=("ID", "Nombre", "Marca", "Stock", "Precio"),
            show="headings",
            height=12
        )

        for col in ("ID", "Nombre", "Marca", "Stock", "Precio"):
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nombre", width=180)
        self.tree.column("Marca", width=100)
        self.tree.column("Stock", width=70, anchor="center")
        self.tree.column("Precio", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.combo_cat.bind("<<ComboboxSelected>>", self.cargar_productos)
        self.tree.bind("<Double-1>", self.seleccionar_producto)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.cargar_productos()

    def cargar_productos(self, event=None):
        self.tree.delete(*self.tree.get_children())
        cat = self.combo_cat.get()

        for p in self.controlador.gestor.productos.get(cat, []):
            if p.estado == "Activo":
                self.tree.insert("", "end", values=(p.id, p.nombre, p.marca, p.stock, f"${p.precio:.2f}"))

    def seleccionar_producto(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = seleccion[0]
            valores = self.tree.item(item, "values")
            self.entry_id_p.delete(0, tk.END)
            self.entry_id_p.insert(0, valores[0])

    def procesar_venta(self):
        cat = self.combo_cat.get().strip()
        try:
            id_p = int(self.entry_id_p.get())
            cant = int(self.entry_cant.get())

            self.controlador.gestor.registrar_venta(cat, id_p, cant)
            messagebox.showinfo("Éxito", "Venta realizada con éxito.")

            self.entry_id_p.delete(0, tk.END)
            self.entry_cant.delete(0, tk.END)
            self.cargar_productos()
            self.controlador.mostrar_pantalla(MenuPrincipal)
        except ValueError as e:
            messagebox.showerror("Error de Venta", str(e))


class PantallaBuscarProducto(tk.Frame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador
        self.dimensiones = "850x500"

        barra_superior = tk.Frame(self)
        barra_superior.pack(fill="x", padx=10, pady=10)

        tk.Button(barra_superior, text="← Regresar", command=lambda: controlador.mostrar_pantalla(MenuPrincipal)).pack(side="left")

        tk.Label(self, text="Buscar Productos", font=("Arial", 12, "bold")).pack(pady=5)

        frame_busqueda = tk.Frame(self)
        frame_busqueda.pack(pady=10)
 
        tk.Label(frame_busqueda, text="Categoría").grid(row=0, column=0, padx=5)

        self.combo_categoria = ttk.Combobox(frame_busqueda, values=list(MAPPING_CLASES.keys()), state="readonly", width=20)
        self.combo_categoria.grid(row=0, column=1)
        self.combo_categoria.current(0)

        tk.Label(frame_busqueda, text="Buscar:").grid(row=0, column=2, padx=5)

        self.entry_busqueda = tk.Entry(frame_busqueda, width=25)
        self.entry_busqueda.grid(row=0, column=3, padx=5)

        self.entry_busqueda.bind("<KeyRelease>", self.filtrar_productos)
        self.combo_categoria.bind("<<ComboboxSelected>>", self.filtrar_productos)

        self.tree = ttk.Treeview(
            self,
            columns=("ID", "Nombre", "Marca", "Stock", "Precio", "Estado"),
            show="headings",
            height=15
        )

        for col in ("ID", "Nombre", "Marca", "Stock", "Precio", "Estado"):
            self.tree.heading(col, text=col)

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Nombre", width=220)
        self.tree.column("Marca", width=120)
        self.tree.column("Stock", width=80, anchor="center")
        self.tree.column("Precio", width=100, anchor="center")
        self.tree.column("Estado", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=15, pady=10)
        self.tree.bind("<Double-1>", self.mostrar_detalle)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.entry_busqueda.delete(0, tk.END)
        self.cargar_productos()

    def cargar_productos(self):
        self.tree.delete(*self.tree.get_children())
        cat = self.combo_categoria.get()

        for p in self.controlador.gestor.productos.get(cat, []):
            self.tree.insert("", "end", values=(p.id, p.nombre, p.marca, p.stock, f"${p.precio:.2f}", p.estado))

    def filtrar_productos(self, event=None):
        texto = self.entry_busqueda.get().lower()
        self.tree.delete(*self.tree.get_children())
        cat = self.combo_categoria.get()

        for p in self.controlador.gestor.productos.get(cat, []):
            if (
                texto in str(p.id).lower()
                or texto in p.nombre.lower()
                or texto in p.marca.lower()
            ):
                self.tree.insert("", "end", values=(p.id, p.nombre, p.marca, p.stock, f"${p.precio:.2f}", p.estado))

    def mostrar_detalle(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return

        item = seleccion[0]
        id_prod = int(self.tree.item(item)["values"][0])
        cat = self.combo_categoria.get()

        producto = self.controlador.gestor.buscar_producto_por_id(cat, id_prod)
        if producto:
            messagebox.showinfo("Detalle del Producto", str(producto))


# ==========================================
# 4. PUNTO DE ENTRADA
# ==========================================

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()