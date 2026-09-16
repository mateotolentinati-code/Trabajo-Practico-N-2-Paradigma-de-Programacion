'''

## **Objetivo del Trabajo** 

Este TP2 retoma el mismo dominio de negocio que el TP1 (gestión de turnos médicos), pero exige resolverlo aplicando el paradigma de Programación Orientada a Objetos en Python. El objetivo no es solo "traducir" el código de Pascal a Python, sino rediseñar la solución utilizando clases, encapsulamiento, herencia, polimorfismo y manejo de excepciones, de forma que el grupo pueda explicar y justificar en qué cambia el diseño respecto de la versión estructurada. 

Durante la defensa oral se pedirá explícitamente una comparación entre ambos paradigmas. 

## **1. Historia de Usuario** 

|**Campo**|**Descripción**|
|---|---|
|Como|recepcionista de un consultorio médico|
|Quiero|registrar, consultar, modificar y cancelar turnos de pacientes, con médicos y<br>pacientes representados como objetos propios|
|Para|organizar la agenda del consultorio de forma ordenada, extensible y fácil de<br>mantener|



## **2. Modelo de Clases del Sistema** 

A diferencia del TP1 (donde todo era un único record TTurno), en esta versión el dominio se modela con una jerarquía de clases. 
Como mínimo, el sistema debe incluir: 

#### **2.1 Clase abstracta Persona** 

Clase base con los atributos comunes a pacientes y médicos. No se instancia directamente. 

|**Atributo**|**Tipo**|**Descripción**|
|---|---|---|
|_dni|str|Documento de identidad (privado)|
|_nombre|str|Nombre completo (privado)|



Debe exponerse el acceso a estos atributos mediante @property, y declarar al menos un método pensado para ser sobrescrito por las
subclases (por ejemplo presentacion()), que dispare NotImplementedError si se llama desde la clase base. 

#### **2.2 Clase Paciente (hereda de Persona)** 

|**Atributo**|**Tipo**|**Descripción**|
|---|---|---|
|obra_social|str|Nombre de la obra social o 'particular'|
|historial_turnos|List[int]|IDs de turnos asociados a este paciente|



#### **2.3 Clase Medico (hereda de Persona)** 

|**Atributo**|**Tipo**|**Descripción**|
|---|---|---|
|especialidad|str|Especialidad médica|
|matricula|str|Número de matrícula profesional|



#### **2.4 Clase Turno** 

|**Atributo**|**Tipo**|**Descripción**|
|---|---|---|
|id|int|Identificador único, asignado automáticamente|
|paciente|Paciente|Objeto paciente asociado|
|medico|Medico|Objeto médico asociado|
|fecha|str|Fecha del turno (DD/MM/AAAA)|
|hora|str|Hora del turno (HH:MM)|
|estado|str|pendiente / atendido / cancelado|
|modalidad|str|presencial / virtual|



El campo modalidad es la base del requisito de polimorfismo del punto 4.2: no se pide una clase abstracta Turno con subclases TurnoPresencial
 y TurnoVirtual, pero sí se acepta y se valora especialmente que el grupo elija resolverlo así en lugar de con un simple string. 

#### **2.5 Clase GestorTurnos** 

Clase que encapsula la colección de turnos y las operaciones del CRUD. Internamente puede usar una lista o un diccionario de objetos Turno;
 esa colección debe ser un atributo privado, accedido solo a través de los métodos de la clase. 

## **3. Requerimientos Funcionales (CRUD)** 

#### **3.1 Alta - Registrar Turno** 

- Permitir crear un nuevo objeto Turno a partir de un Paciente y un Médico existentes (o creados en el momento). 

- El sistema debe asignar automáticamente un id correlativo único. 

- No se aceptan campos vacíos: la validación debe lanzar una excepción propia (por ejemplo CampoVacioError), no simplemente imprimir un
 mensaje. 

- El estado inicial siempre debe ser 'pendiente'. 

#### **3.2 Consulta - Buscar Turno** 

- Permitir buscar un turno por su id. 

- Permitir buscar turnos por nombre parcial del paciente (puede devolver una lista de objetos Turno). 

- Si no se encuentra ningún resultado, se debe manejar mediante una excepción propia (por ejemplo TurnoNoEncontradoError) capturada en el menú, mostrando un mensaje claro al usuario. 

- Mostrar todos los datos del turno encontrado con formato legible, delegando la presentación a un método propio del objeto (por ejemplo __str__ o mostrar_detalle()). 

#### **3.3 Modificación - Editar Turno** 

- Permitir modificar: fecha, hora y médico de un turno existente. 

- El id del turno no puede ser modificado (no debe existir un setter público para ese atributo). 

- El paciente asociado no puede ser modificado. 

- Si el turno está 'cancelado' o 'atendido', la modificación debe rechazarse lanzando una excepción propia (por ejemplo TurnoNoModificableError). 

#### **3.4 Baja - Cancelar Turno** 

- El sistema debe pedir confirmación antes de cancelar un turno. 

- Un turno con estado 'atendido' no puede darse de baja (excepción propia). 

- La baja es lógica: cambia el estado a 'cancelado', no elimina el objeto de la colección. 

#### **3.5 Listado - Ver Todos los Turnos** 

- Mostrar todos los turnos registrados en formato de tabla. 

- Diferenciar visualmente los turnos según su estado. 

- Mostrar la cantidad total de turnos al pie del listado. 

- Se valorará el uso de comprensión de listas y/o funciones como filter/map/sorted para filtrar u ordenar el listado (por fecha, por estado, por médico). 

## **4. Requisitos de Diseño Orientado a Objetos** 

Estos requisitos son específicos de este TP2 y serán evaluados de forma independiente de la funcionalidad del CRUD. 

#### **4.1 Encapsulamiento** 

- Todos los atributos de las clases deben ser privados o protegidos (prefijo _ o __). 

- El acceso externo debe hacerse mediante @property y, cuando corresponda, sus respectivos setters con validación. 

- Ningún atributo interno de GestorTurnos debe ser accedido ni modificado directamente desde fuera de la clase. 

#### **4.2 Herencia** 

- Paciente y Medico deben heredar de Persona, reutilizando atributos y/o métodos comunes. 

- Se debe usar super().__init__() correctamente en los constructores de las subclases. 

#### **4.3 Polimorfismo** 

- Debe existir al menos un método que se comporte de forma distinta según el tipo de objeto que lo invoca (por ejemplo, un método presentacion() distinto en Paciente y en Medico, o un método de notificación distinto según la modalidad del turno). 

- Se debe poder explicar en la defensa oral, con el código en pantalla, dónde ocurre el polimorfismo y por qué no podría lograrse igual en Pascal estructurado. 

#### **4.4 Manejo de excepciones** 

- Se deben definir al menos dos excepciones propias, heredadas de Exception (por ejemplo TurnoNoEncontradoError, CampoVacioError, TurnoNoModificableError). 

- El menú principal debe capturar estas excepciones con try/except y mostrar mensajes claros, sin que el programa se caiga ante una entrada inválida. 

#### **4.5 Persistencia** 

Guardado y carga de los turnos en un archivo JSON, de modo que los datos no se pierdan al cerrar el programa. 

## **5. Criterios de Aceptación** 

|**Operación**|**Escenario**|**Acción / Entrada**|**Resultado Esperado**|
|---|---|---|---|
|Alta|Turno válido|Todos los campos completos|Turno creado con id único y<br>estado 'pendiente'|
|Alta|Campo vacío|Intentar guardar sin nombre<br>de paciente|Se lanza CampoVacioError,<br>no se guarda|
|Consulta|Id existente|Buscar por id válido|Muestra todos los datos del<br>turno|
|Consulta|Id inexistente|Buscar id que no existe|Se lanza<br>TurnoNoEncontradoError,<br>mensaje claro|
|Modificación|Turno pendiente|Cambiar fecha y hora|Datos actualizados<br>correctamente|
|Modificación|Turno cancelado|Intentar modificar turno<br>cancelado|Se lanza<br>TurnoNoModificableError|
|Baja|Con confirmación|Confirmar cancelación|Estado cambia a 'cancelado'|
|Baja|Turno atendido|Intentar cancelar turno|Se rechaza con|



|**Operación**|**Escenario**|**Acción / Entrada**|**Resultado Esperado**|
|---|---|---|---|
|||atendido|excepción/mensaje claro|
|Listado|Sin registros|Listar con colección vacía|Mensaje: 'No hay turnos<br>registrados'|
|Listado|Con registros|Listar con datos cargados|Tabla ordenada con total al<br>final|



## **6. Estructura del Programa Requerida** 

El programa debe organizarse en al menos los siguientes elementos (pueden repartirse en varios archivos .py, por ejemplo modelos.py, excepciones.py, gestor.py y main.py): 

|**Elemento**|**Tipo Python**|**Responsabilidad**|
|---|---|---|
|Persona|Clase abstracta / base|Atributos y comportamiento común<br>a pacientes y médicos|
|Paciente|Clase (hereda de Persona)|Representa a un paciente del<br>consultorio|
|Medico|Clase (hereda de Persona)|Representa a un médico del<br>consultorio|
|Turno|Clase|Representa un turno médico y su<br>estado|
|GestorTurnos|Clase|Encapsula la colección de turnos y<br>el CRUD completo|
|CampoVacioError,<br>TurnoNoEncontradoError,<br>TurnoNoModificableError|Clases de excepción<br>(Exception)|Errores de negocio propios del<br>dominio|
|mostrar_menu()|Función|Imprime el menú principal en<br>pantalla|
|main()|Función|Punto de entrada del programa,<br>contiene el bucle del menú|



## **8. Presentación en Clase** 

Durante la defensa, el grupo deberá: 

- Ejecutar el programa en vivo, sin errores, mostrando el CRUD completo con datos de prueba preparados con anticipación. 

- Mostrar en el código dónde está aplicado cada pilar de la POO pedido: encapsulamiento, herencia y polimorfismo. 

- Mostrar al menos un caso de excepción manejada en vivo (campo vacío, id inexistente, turno no modificable, etc.). 

- Explicar una decisión de diseño propia del grupo: por qué modelaron las clases de esa forma, qué alternativas consideraron. 

- Responder una pregunta comparativa del docente sobre las diferencias entre esta solución y la del TP1 en Pascal (por ejemplo: ¿qué pasaba en Pascal cuando querían diferenciar el comportamiento de un turno presencial y uno virtual? ¿Cómo se resuelve eso ahora?). 

- Responder preguntas del docente sobre cualquier parte del código. 

_Nota: cada integrante debe poder explicar cualquier parte del código, no solo la parte que escribió. Se espera además que puedan argumentar, con sus palabras, por qué el mismo problema de negocio se resuelve distinto en un paradigma estructurado y en uno orientado a objetos._ 

'''
import pickle

class Producto:
    def __init__ (self,id,nombre,marca,stock,precio,estado):
        self.id = id    
        self.nombre = nombre
        self.marca = marca
        self.stock = stock
        self.precio = precio
        self.estado = estado
        # def Asignar id():


class Inventario:
    def __init__ (self):
        self.productos = [] #

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def guardar(self):
        with open("productos.dat", "wb") as archivo: #wb escribir en binario y el archivo se abre y cierra automaticamente
            pickle.dump(self.productos, archivo) #pickle.dump Toma la lista y la guarda dentro de productos.dat

    def cargar(self):
        try:
            with open("productos.dat", "rb") as archivo:
                self.productos = pickle.load(archivo) #pickle.load lee el contenido de productos.dat y reconstruye la lista original.
        except FileNotFoundError:
            self.productos = []


class PlacadeVideo(Producto):
    def __init__ (self, id, nombre, marca, stock, precio, estado, vram,chipset, consumo_wats):
        super().__init__(id, nombre, marca, stock, precio, estado,) #El super llama a la clase contructuro Producto
        self.vram = vram
        self.chipset = chipset
        self.consumo_wats = consumo_wats

class Procesador(Producto):
    def __init__ (self, id, nombre, marca, stock, precio, estado,hilos,frecuencia,socket):
        super().__init__(id, nombre, marca, stock, precio, estado,)
        self.hilos = hilos
        self.frecuencia = frecuencia
        self.socket = socket 


class Ram(Producto):
    def __init__(self, id, nombre, marca, stock, precio, estado, capacidad_gb, velocidad_mhz, tipo ): 
        super().__init__(id, nombre, marca, stock, precio, estado)
        self.capacidad_gb = capacidad_gb
        self.velocidad_mhz = velocidad_mhz
        self.tipo = tipo

class Disco(Producto):
    def __init__ (self, id, nombre, marca, stock, precio, estado, capacidad_gb, tipo, velocidad):
        super().__init__(id, nombre, marca, stock, precio, estado)
        self.capacidad_gb = capacidad_gb
        self.tipo = tipo
        self.velocidad = velocidad

class Pendrive(Producto):
    def __init__ (self,id, nombre, marca, stock, precio, estado, capacidad, tipo_usb):
        super().__init__(id, nombre, marca, stock, precio, estado)
        self.capacidad = capacidad
        self.tipo_usb = tipo_usb


