from database.models import Cliente
from database.connection import DatabaseConnection

class ClienteController:
    def __init__(self):
        pass
    
    def get_all_clientes(self):
        """Obtiene todos los clientes"""
        return Cliente.get_all()
    
    def get_cliente_by_id(self, id):
        """Obtiene un cliente por su ID"""
        return Cliente.get_by_id(id)
    
    def create_cliente(self, nombre, telefono, dni, direccion):
        """Crea un nuevo cliente"""
        cliente = Cliente(nombre=nombre, telefono=telefono, dni=dni, direccion=direccion)
        return cliente.save()
    
    def update_cliente(self, id, nombre, telefono, dni, direccion):
        """Actualiza un cliente existente"""
        cliente = Cliente.get_by_id(id)
        if cliente:
            cliente.nombre = nombre
            cliente.telefono = telefono
            cliente.dni = dni
            cliente.direccion = direccion
            return cliente.save()
        return False
    
    def delete_cliente(self, id):
        """Elimina un cliente"""
        cliente = Cliente.get_by_id(id)
        if cliente:
            return cliente.delete()
        return False
    
    def search_clientes(self, term):
        """Busca clientes por término"""
        db = DatabaseConnection()
        query = """SELECT * FROM Cliente 
                 WHERE NombreCli LIKE ? 
                 OR Dni LIKE ?
                 OR TelefonoCli LIKE ?"""
        search_term = f"%{term}%"
        rows = db.fetch_all(query, (search_term, search_term, search_term))
        return [Cliente(id=row['idCliente'], nombre=row['NombreCli'], 
                      telefono=row['TelefonoCli'], dni=row['Dni'], 
                      direccion=row['DireccionClie']) for row in rows]
    
    def get_clientes_frecuentes(self, limite=10):
        """Obtiene los clientes más frecuentes (con más compras)"""
        db = DatabaseConnection()
        query = """SELECT c.*, COUNT(v.idVenta) as total_compras 
                 FROM Cliente c
                 LEFT JOIN Venta v ON c.idCliente = v.idCliente
                 GROUP BY c.idCliente
                 ORDER BY total_compras DESC
                 LIMIT ?"""
        rows = db.fetch_all(query, (limite,))
        return [Cliente(id=row['idCliente'], nombre=row['NombreCli'], 
                      telefono=row['TelefonoCli'], dni=row['Dni'], 
                      direccion=row['DireccionClie']) for row in rows]