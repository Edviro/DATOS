from database.models import Venta, DetalleVenta
from database.connection import DatabaseConnection
import datetime

class VentaController:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def get_all_ventas(self):
        """Obtiene todas las ventas con información de cliente y empleado"""
        query = """
        SELECT v.*, c.NombreCli as cliente_nombre, e.NombreEmp as empleado_nombre
        FROM Venta v
        LEFT JOIN Cliente c ON v.idCliente = c.idCliente
        LEFT JOIN Empleado e ON v.idEmpleado = e.idEmpleado
        ORDER BY v.Fecha DESC
        """
        
        rows = self.db.fetch_all(query)
        ventas = []
        
        for row in rows:
            venta = Venta(
                id=row['idVenta'],
                fecha=row['Fecha'],
                total=row['Total'],
                id_cliente=row['idCliente'],
                id_empleado=row['idEmpleado']
            )
            # Agregar información adicional
            venta.cliente_nombre = row['cliente_nombre']
            venta.empleado_nombre = row['empleado_nombre']
            ventas.append(venta)
        
        return ventas
    
    def listar_ventas(self):
        """Alias para get_all_ventas - para compatibilidad con la vista de facturas"""
        return self.get_all_ventas()
    
    def get_venta_by_id(self, id_venta):
        """Obtiene una venta por su ID"""
        query = """SELECT v.*, c.NombreCli, e.NombreEmp 
                 FROM Venta v
                 LEFT JOIN Cliente c ON v.idCliente = c.idCliente
                 LEFT JOIN Empleado e ON v.idEmpleado = e.idEmpleado
                 WHERE v.idVenta = ?"""
        row = self.db.fetch_one(query, (id_venta,))
        if not row:
            return None
        
        return {
            'id': row['idVenta'],
            'fecha': row['Fecha'],
            'total': row['Total'],
            'cliente': row['NombreCli'],
            'empleado': row['NombreEmp'],
            'id_cliente': row['idCliente'],
            'id_empleado': row['idEmpleado']
        }
    
    def obtener_venta(self, id_venta):
        """Obtiene una venta por su ID - retorna objeto Venta"""
        query = """SELECT v.*, c.NombreCli, e.NombreEmp 
                 FROM Venta v
                 LEFT JOIN Cliente c ON v.idCliente = c.idCliente
                 LEFT JOIN Empleado e ON v.idEmpleado = e.idEmpleado
                 WHERE v.idVenta = ?"""
        row = self.db.fetch_one(query, (id_venta,))
        if not row:
            return None
        
        venta = Venta(
            id=row['idVenta'],
            fecha=row['Fecha'],
            total=row['Total'],
            id_cliente=row['idCliente'],
            id_empleado=row['idEmpleado']
        )
        # Agregar información adicional
        venta.cliente_nombre = row['NombreCli']
        venta.empleado_nombre = row['NombreEmp']
        return venta
    
    def get_detalles_venta(self, id_venta):
        """Obtiene los detalles de una venta"""
        query = """SELECT d.*, p.NombrePro 
                 FROM DetalleVenta d
                 JOIN Producto p ON d.idProducto = p.idProducto
                 WHERE d.idVenta = ?"""
        rows = self.db.fetch_all(query, (id_venta,))
        return [{
            'id': row['idDetalleVenta'],
            'cantidad': row['Cantidad'],
            'precio_uni': row['PrecioUni'],
            'subtotal': row['SubTotal'],
            'id_producto': row['idProducto'],
            'producto': row['NombrePro']
        } for row in rows]
    
    def crear_venta(self, id_cliente, id_empleado, detalles):
        """Crea una nueva venta con sus detalles"""
        try:
            # Calcular el total de la venta
            total = sum(detalle['subtotal'] for detalle in detalles)
            
            # Insertar la venta
            query_venta = "INSERT INTO Venta (Fecha, Total, idEmpleado, idCliente) VALUES (?, ?, ?, ?)"
            fecha = datetime.date.today().isoformat()
            cursor = self.db.execute_query(query_venta, (fecha, total, id_empleado, id_cliente))
            id_venta = cursor.lastrowid
            
            # Insertar los detalles de la venta
            query_detalle = "INSERT INTO DetalleVenta (Cantidad, PrecioUni, SubTotal, idProducto, idVenta) VALUES (?, ?, ?, ?, ?)"
            for detalle in detalles:
                self.db.execute_query(query_detalle, (
                    detalle['cantidad'],
                    detalle['precio_uni'],
                    detalle['subtotal'],
                    detalle['id_producto'],
                    id_venta
                ))
                
                # Actualizar el stock del producto
                query_update_stock = "UPDATE Producto SET Stock = Stock - ? WHERE idProducto = ?"
                self.db.execute_query(query_update_stock, (detalle['cantidad'], detalle['id_producto']))
            
            return id_venta
        except Exception as e:
            print(f"Error al crear venta: {str(e)}")
            return None
    
    def buscar_ventas_por_fecha(self, fecha_inicio, fecha_fin):
        """Busca ventas en un rango de fechas"""
        query = """SELECT v.*, c.NombreCli, e.NombreEmp 
                 FROM Venta v
                 LEFT JOIN Cliente c ON v.idCliente = c.idCliente
                 LEFT JOIN Empleado e ON v.idEmpleado = e.idEmpleado
                 WHERE v.Fecha BETWEEN ? AND ?
                 ORDER BY v.Fecha DESC"""
        rows = self.db.fetch_all(query, (fecha_inicio, fecha_fin))
        return [{
            'id': row['idVenta'],
            'fecha': row['Fecha'],
            'total': row['Total'],
            'cliente': row['NombreCli'],
            'empleado': row['NombreEmp'],
            'id_cliente': row['idCliente'],
            'id_empleado': row['idEmpleado']
        } for row in rows]
    
    def buscar_ventas_por_cliente(self, id_cliente):
        """Busca ventas de un cliente específico"""
        query = """SELECT v.*, c.NombreCli as cliente_nombre, e.NombreEmp as empleado_nombre
                 FROM Venta v
                 LEFT JOIN Cliente c ON v.idCliente = c.idCliente
                 LEFT JOIN Empleado e ON v.idEmpleado = e.idEmpleado
                 WHERE v.idCliente = ?
                 ORDER BY v.Fecha DESC"""
        rows = self.db.fetch_all(query, (id_cliente,))
        ventas = []
        
        for row in rows:
            venta = Venta(
                id=row['idVenta'],
                fecha=row['Fecha'],
                total=row['Total'],
                id_cliente=row['idCliente'],
                id_empleado=row['idEmpleado']
            )
            # Agregar información adicional
            venta.cliente_nombre = row['cliente_nombre']
            venta.empleado_nombre = row['empleado_nombre']
            ventas.append(venta)
        
        return ventas