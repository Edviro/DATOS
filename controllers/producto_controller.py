from database.models import Producto
from database.connection import DatabaseConnection

class ProductoController:
    def __init__(self):
        pass
    
    def get_all_productos(self):
        """Obtiene todos los productos"""
        return Producto.get_all()
    
    def get_producto_by_id(self, id):
        """Obtiene un producto por su ID"""
        return Producto.get_by_id(id)
    
    def create_producto(self, nombre, precio, stock, id_categoria):
        """Crea un nuevo producto"""
        producto = Producto(nombre=nombre, precio=precio, stock=stock, id_categoria=id_categoria)
        return producto.save()
    
    def update_producto(self, id, nombre, precio, stock, id_categoria):
        """Actualiza un producto existente"""
        producto = Producto.get_by_id(id)
        if producto:
            producto.nombre = nombre
            producto.precio = precio
            producto.stock = stock
            producto.id_categoria = id_categoria
            return producto.save()
        return False
    
    def delete_producto(self, id):
        """Elimina un producto"""
        producto = Producto.get_by_id(id)
        if producto:
            return producto.delete()
        return False
    
    def update_stock(self, id, cantidad):
        """Actualiza el stock de un producto"""
        producto = Producto.get_by_id(id)
        if producto:
            return producto.update_stock(cantidad)
        return False
    
    def get_productos_by_categoria(self, id_categoria):
        """Obtiene productos por categoría"""
        return Producto.get_by_categoria(id_categoria)
    
    def search_productos(self, term):
        """Busca productos por término"""
        db = DatabaseConnection()
        query = """SELECT * FROM Producto 
                 WHERE NombrePro LIKE ? 
                 OR idProducto LIKE ?"""
        search_term = f"%{term}%"
        rows = db.fetch_all(query, (search_term, search_term))
        return [Producto(id=row['idProducto'], nombre=row['NombrePro'], 
                       precio=row['Precio'], stock=row['Stock'], 
                       id_categoria=row['idCategoria']) for row in rows]
    
    def get_productos_stock_bajo(self, limite=10):
        """Obtiene productos con stock bajo"""
        db = DatabaseConnection()
        query = "SELECT * FROM Producto WHERE Stock <= ?"
        rows = db.fetch_all(query, (limite,))
        return [Producto(id=row['idProducto'], nombre=row['NombrePro'], 
                       precio=row['Precio'], stock=row['Stock'], 
                       id_categoria=row['idCategoria']) for row in rows]
    
    def get_categoria_nombre(self, id_categoria):
        """Obtiene el nombre de una categoría por su ID"""
        if id_categoria is None:
            return "Sin categoría"
        
        db = DatabaseConnection()
        query = "SELECT NombreCat FROM Categoria WHERE idCategoria = ?"
        row = db.fetch_one(query, (id_categoria,))
        if row:
            return row['NombreCat']
        return "Categoría no encontrada"