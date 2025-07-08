from database.models import Categoria

class CategoriaController:
    def __init__(self):
        pass
    
    def get_all_categorias(self):
        """Obtiene todas las categorías"""
        return Categoria.get_all()
    
    def get_categoria_by_id(self, id):
        """Obtiene una categoría por su ID"""
        return Categoria.get_by_id(id)
    
    def create_categoria(self, nombre, descripcion):
        """Crea una nueva categoría"""
        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        return categoria.save()
    
    def update_categoria(self, id, nombre, descripcion):
        """Actualiza una categoría existente"""
        categoria = Categoria.get_by_id(id)
        if categoria:
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            return categoria.save()
        return False
    
    def delete_categoria(self, id):
        """Elimina una categoría"""
        categoria = Categoria.get_by_id(id)
        if categoria:
            return categoria.delete()
        return False
    
    def search_categorias(self, term):
        """Busca categorías por término"""
        # Implementar búsqueda en la base de datos
        from database.connection import DatabaseConnection
        db = DatabaseConnection()
        query = "SELECT * FROM Categoria WHERE NombreCat LIKE ? OR Descripcion LIKE ?"
        search_term = f"%{term}%"
        rows = db.fetch_all(query, (search_term, search_term))
        return [Categoria(id=row['idCategoria'], nombre=row['NombreCat'], descripcion=row['Descripcion']) for row in rows]