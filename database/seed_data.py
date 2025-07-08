import os
import sqlite3
from database.connection import DatabaseConnection

def seed_database():
    db = DatabaseConnection()
    
    # Verificar si ya hay datos
    query = "SELECT COUNT(*) as count FROM Categoria"
    result = db.fetch_one(query)
    if result and result['count'] > 0:
        print("La base de datos ya contiene datos. No se realizará la inicialización.")
        return
    
    # Insertar categorías
    categorias = [
        ("Electrónicos", "Productos electrónicos y gadgets"),
        ("Ropa", "Prendas de vestir y accesorios"),
        ("Hogar", "Artículos para el hogar"),
        ("Alimentos", "Productos alimenticios"),
        ("Oficina", "Material de oficina")
    ]
    
    for nombre, descripcion in categorias:
        db.execute_query("INSERT INTO Categoria (NombreCat, Descripcion) VALUES (?, ?)", 
                        (nombre, descripcion))
    
    # Insertar productos de ejemplo
    productos = [
        ("Laptop HP", 899.99, 10, 1),
        ("Smartphone Samsung", 499.99, 15, 1),
        ("Camiseta Básica", 19.99, 50, 2),
        ("Pantalón Jeans", 39.99, 30, 2),
        ("Lámpara LED", 29.99, 20, 3),
        ("Juego de Sábanas", 49.99, 15, 3),
        ("Café Gourmet", 12.99, 40, 4),
        ("Chocolate Premium", 5.99, 100, 4),
        ("Cuaderno Ejecutivo", 8.99, 60, 5),
        ("Set de Bolígrafos", 4.99, 80, 5)
    ]
    
    for nombre, precio, stock, id_categoria in productos:
        db.execute_query("INSERT INTO Producto (NombrePro, Precio, Stock, idCategoria) VALUES (?, ?, ?, ?)", 
                        (nombre, precio, stock, id_categoria))
    
    # Insertar clientes de ejemplo
    clientes = [
        ("Juan Pérez", "555-1234", "12345678A", "Calle Principal 123"),
        ("María García", "555-5678", "87654321B", "Avenida Central 456"),
        ("Carlos López", "555-9012", "23456789C", "Plaza Mayor 789")
    ]
    
    for nombre, telefono, dni, direccion in clientes:
        try:
            db.execute_query("INSERT INTO Cliente (NombreCli, TelefonoCli, Dni, DireccionClie) VALUES (?, ?, ?, ?)", 
                            (nombre, telefono, dni, direccion))
        except sqlite3.IntegrityError:
            print(f"Cliente con DNI {dni} ya existe. Omitiendo.")
    
    # Insertar empleados de ejemplo
    empleados = [
        ("Ana Martínez", "ana@empresa.com", "555-3456", "Calle Secundaria 234"),
        ("Pedro Sánchez", "pedro@empresa.com", "555-7890", "Avenida Norte 567")
    ]
    
    for nombre, correo, telefono, direccion in empleados:
        try:
            db.execute_query("INSERT INTO Empleado (NombreEmp, CorreoEmp, Telefono, DireccionEmp) VALUES (?, ?, ?, ?)", 
                            (nombre, correo, telefono, direccion))
        except sqlite3.IntegrityError:
            print(f"Empleado con correo {correo} ya existe. Omitiendo.")
    
    print("Datos de ejemplo insertados correctamente.")

if __name__ == "__main__":
    seed_database()