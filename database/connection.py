import sqlite3
import os

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            # Crear el directorio de datos si no existe
            data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
            
            # Ruta de la base de datos
            cls.db_path = os.path.join(data_dir, 'dcorelp.db')
            cls._instance.connection = None
        return cls._instance
    
    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query, params=()):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    
    def fetch_all(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()
    
    def fetch_one(self, query, params=()):
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
    
    def create_tables(self):
        """Crea todas las tablas de la base de datos si no existen"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # Tabla Categoria
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categoria (
            idCategoria INTEGER PRIMARY KEY AUTOINCREMENT,
            NombreCat TEXT NOT NULL,
            Descripcion TEXT
        )
        ''')
        
        # Tabla Producto
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Producto (
            idProducto INTEGER PRIMARY KEY AUTOINCREMENT,
            NombrePro TEXT NOT NULL,
            Precio REAL NOT NULL,
            Stock INTEGER NOT NULL,
            idCategoria INTEGER,
            FOREIGN KEY (idCategoria) REFERENCES Categoria(idCategoria)
        )
        ''')
        
        # Tabla Cliente
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cliente (
            idCliente INTEGER PRIMARY KEY AUTOINCREMENT,
            NombreCli TEXT NOT NULL,
            TelefonoCli TEXT,
            Dni TEXT UNIQUE,
            DireccionClie TEXT
        )
        ''')
        
        # Tabla Empleado
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Empleado (
            idEmpleado INTEGER PRIMARY KEY AUTOINCREMENT,
            NombreEmp TEXT NOT NULL,
            CorreoEmp TEXT UNIQUE,
            Telefono TEXT,
            DireccionEmp TEXT
        )
        ''')
        
        # Tabla Venta
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Venta (
            idVenta INTEGER PRIMARY KEY AUTOINCREMENT,
            Fecha DATE NOT NULL DEFAULT CURRENT_DATE,
            Total REAL NOT NULL,
            idEmpleado INTEGER,
            idCliente INTEGER,
            FOREIGN KEY (idEmpleado) REFERENCES Empleado(idEmpleado),
            FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente)
        )
        ''')
        
        # Tabla DetalleVenta
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS DetalleVenta (
            idDetalleVenta INTEGER PRIMARY KEY AUTOINCREMENT,
            Cantidad INTEGER NOT NULL,
            PrecioUni REAL NOT NULL,
            SubTotal REAL NOT NULL,
            idProducto INTEGER,
            idVenta INTEGER,
            FOREIGN KEY (idProducto) REFERENCES Producto(idProducto),
            FOREIGN KEY (idVenta) REFERENCES Venta(idVenta)
        )
        ''')
        
        conn.commit()