from database.models import Empleado
from database.connection import DatabaseConnection

class EmpleadoController:
    def __init__(self):
        pass
    
    def get_all_empleados(self):
        """Obtiene todos los empleados"""
        return Empleado.get_all()
    
    def get_empleado_by_id(self, id):
        """Obtiene un empleado por su ID"""
        return Empleado.get_by_id(id)
    
    def create_empleado(self, nombre, correo, telefono, direccion):
        """Crea un nuevo empleado"""
        empleado = Empleado(nombre=nombre, correo=correo, telefono=telefono, direccion=direccion)
        return empleado.save()
    
    def update_empleado(self, id, nombre, correo, telefono, direccion):
        """Actualiza un empleado existente"""
        empleado = Empleado.get_by_id(id)
        if empleado:
            empleado.nombre = nombre
            empleado.correo = correo
            empleado.telefono = telefono
            empleado.direccion = direccion
            return empleado.save()
        return False
    
    def delete_empleado(self, id):
        """Elimina un empleado"""
        empleado = Empleado.get_by_id(id)
        if empleado:
            return empleado.delete()
        return False
    
    def search_empleados(self, term):
        """Busca empleados por término"""
        db = DatabaseConnection()
        query = """SELECT * FROM Empleado 
                 WHERE NombreEmp LIKE ? 
                 OR CorreoEmp LIKE ?
                 OR Telefono LIKE ?"""
        search_term = f"%{term}%"
        rows = db.fetch_all(query, (search_term, search_term, search_term))
        return [Empleado(id=row['idEmpleado'], nombre=row['NombreEmp'], 
                       correo=row['CorreoEmp'], telefono=row['Telefono'], 
                       direccion=row['DireccionEmp']) for row in rows]