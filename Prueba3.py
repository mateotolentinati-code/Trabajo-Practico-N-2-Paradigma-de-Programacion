    from pathlib import Path
    import json

    import tkinter as tk    
    from tkinter import messagebox


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
            #aca se descuenta el stock del producto vendido, si hay stock suficiente, se descuenta y devuelve True, sino devuelve False
            if self.producto.stock >= self.cantidad:
                self.producto.stock -= self.cantidad
                return True
            return False
    # =================
    # Inventario
    # =================

    # -----------------
    # Write_json
    # -----------------

    path = Path(r"C:/Paradigma de Programacion/Python/Trabajo Practico N°2/data.json") #Utilizamos la r delante de la ruta para una ruta absoluta

    # Pregunta si el archivo existe y si no existe lo crea

    path.parent.mkdir(parents=True, exist_ok=True)
    '''
    parent → obtiene la carpeta donde va a estar data.json.
    mkdir() → crea la carpeta.
    parents=True → crea también las carpetas superiores que falten.
    exist_ok=True → no da error si ya existen.
    '''
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
            "ventas": [],
        }
        with open(path, "w", encoding="utf-8") as archivo:
            json.dump(data, archivo, indent=4)

    def guardar_json():
        with open(path, "w", encoding="utf-8") as archivo:
            json.dump(data, archivo, indent=4, ensure_ascii=False)


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

    def registrar_venta():
        ventana_v=tk.Toplevel()
        ventana_v.title("Registrar Venta")
        ventana_v.geometry("350x300")

        tk.Label(ventana_v, text="categoria de producto").pack()
        entry_cat=tk.Entry(ventana_v)
        entry_cat.insert(0,"procesador")
        entry_cat.pack()

        tk.Label(ventana_v, text="ID del Producto").pack()
        entry_id_p = tk.Entry(ventana_v)
        entry_id_p.pack()

        tk.Label(ventana_v, text="Cantidad").pack()
        entry_cant = tk.Entry(ventana_v)
        entry_cant.pack()

        def procesar_venta():
            cat=entry_cat.get()
            try:
                id_p=int(entry_id_p.get())
                cant=int(entry_cant.get())
            except ValueError:
                messagebox.showerror("Error", "ID y Cantidad deben ser numéricos.")
                return
            
            if cat not in data:
                messagebox.showerror("Error", "Categoría de producto no válida.")
                return
            
            # 1. Buscar producto por ID dentro del JSON
            producto_encontrado = None
            for p in data[cat]:
                if p["id"] == id_p:
                    producto_encontrado = p
                    break

            if not producto_encontrado:
                messagebox.showerror("Error", "Producto no encontrado.")
                return

            # 2. Controlar si hay stock suficiente
            if producto_encontrado["stock"] < cant:
                messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto_encontrado['stock']}")
                return

            # 3. Descontar del inventario
            producto_encontrado["stock"] -= cant

            # 4. Crear instancia de la clase Venta y asociar al operador activo
            total = producto_encontrado["precio"] * cant
            id_venta = len(data["Ventas"]) + 1
            
            nueva_venta = Venta(id_venta, producto_encontrado["nombre"], cant, total, empleado_logueado.nombre)
            
            # 5. Insertar datos en la lista 'Ventas' del diccionario
            data["Ventas"].append({
                "id_venta": nueva_venta.id_venta,
                "producto": nueva_venta.producto_nombre,
                "cantidad": nueva_venta.cantidad,
                "total": nueva_venta.total,
                "vendedor": nueva_venta.vendedor_nombre,
                "fecha": nueva_venta.fecha
            })

            guardar_json()  # Guarda los cambios de stock y la venta en el JSON
            messagebox.showinfo("Éxito", f"Venta realizada por {empleado_logueado.nombre}.\nTotal: ${total:.2f}")
            ventana_v.destroy()

        tk.Button(ventana_v, text="Confirmar Venta", command=procesar_venta).pack(pady=15)


    def ver_ventas():
        ventana_listado = tk.Toplevel()
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

    def abrir_login():
        ventana_login = tk.Toplevel()
        ventana_login.title("Login")
        ventana_login.geometry("300x200")

        tk.Label(ventana_login, text="Usuario").pack()
        entry_usuario = tk.Entry(ventana_login)
        entry_usuario.pack()

        tk.Label(ventana_login, text="Clave").pack()
        entry_clave = tk.Entry(ventana_login, show="*")
        entry_clave.pack()

        def validar():
            global empleado_logueado
            u = entry_usuario.get().strip()
            c = entry_clave.get().strip()

            # Buscamos en 'usuarios' (en minúscula como en tu JSON)
            for usr in data.get("usuarios", []):
                if usr["usuario"] == u and usr["clave"] == c:
                # Instanciamos coincidiendo con tu __init__(nombre, apellido, dni, usuario, clave)
                    empleado_logueado = empleado(
                        nombre=usr.get("nombre", ""),
                        apellido=usr.get("apellido", ""),
                        dni=usr.get("dni", ""),
                        usuario=usr["usuario"],
                        clave=usr["clave"]
                    )

                    messagebox.showinfo("Bienvenido", f"Sesión iniciada como: {empleado_logueado.nombre} {empleado_logueado.apellido}")
                    lbl_usuario.config(text=f"Operador: {empleado_logueado.nombre} {empleado_logueado.apellido}")
                    ventana_login.destroy()
                    ventana.deiconify()
                    return

            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        tk.Button(ventana_login, text="Ingresar", command=validar).pack(pady=15)
        ventana_login.protocol("WM_DELETE_WINDOW", lambda: ventana.destroy())

    # =================
    # Tkinter
    # =================

    ventana = tk.Tk()
    ventana.title("Inventario")
    ventana.geometry("300x350")

    # NUEVO: Etiqueta para saber qué usuario operando la app
    lbl_usuario = tk.Label(ventana, text="Operador: No autenticado", font=("Arial", 10, "italic"))
    lbl_usuario.pack(pady=5)

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

    #NUEVO: Botones para la funcionalidad de ventas
    tk.Button(
        ventana, 
        text="Registrar Venta", 
        command=registrar_venta
        ).pack(pady=10)

    tk.Button(
        ventana, 
            text="Ver Ventas Realizadas", 
            command=ver_ventas
            ).pack(pady=10)

    # NUEVO: Oculta la interfaz principal y lanza primero el formulario de Login
    ventana.withdraw()
    abrir_login()

    ventana.mainloop()
