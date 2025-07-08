from database.connection import DatabaseConnection
from utils.helpers import export_to_csv, format_currency, format_date
import datetime

class ReporteController:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def generar_reporte_ventas(self, fecha_inicio, fecha_fin):
        """Genera un reporte de ventas por período"""
        query = """SELECT v.idVenta, v.Fecha, v.Total, c.NombreCli, e.NombreEmp 
                 FROM Venta v
                 LEFT JOIN Cliente c ON v.idCliente = c.idCliente
                 LEFT JOIN Empleado e ON v.idEmpleado = e.idEmpleado
                 WHERE v.Fecha BETWEEN ? AND ?
                 ORDER BY v.Fecha DESC"""
        rows = self.db.fetch_all(query, (fecha_inicio, fecha_fin))
        return [{
            'id': row['idVenta'],
            'fecha': format_date(row['Fecha']),
            'total': row['Total'],
            'cliente': row['NombreCli'],
            'empleado': row['NombreEmp']
        } for row in rows]
    
    def exportar_reporte_ventas(self, fecha_inicio, fecha_fin):
        """Exporta el reporte de ventas a CSV"""
        ventas = self.generar_reporte_ventas(fecha_inicio, fecha_fin)
        data = [[v['id'], v['fecha'], v['cliente'], v['empleado'], format_currency(v['total'])] for v in ventas]
        headers = ['ID', 'Fecha', 'Cliente', 'Empleado', 'Total']
        filename = f"reporte_ventas_{datetime.date.today().strftime('%Y%m%d')}.csv"
        return export_to_csv(data, filename, headers)
    
    def generar_reporte_productos_vendidos(self, fecha_inicio=None, fecha_fin=None, limite=10):
        """Genera un reporte de productos más vendidos"""
        query_params = []
        fecha_condition = ""
        
        if fecha_inicio and fecha_fin:
            fecha_condition = "WHERE v.Fecha BETWEEN ? AND ?"
            query_params.extend([fecha_inicio, fecha_fin])
        
        query = f"""SELECT p.idProducto, p.NombrePro, c.NombreCat, 
                      SUM(d.Cantidad) as cantidad_vendida, 
                      SUM(d.SubTotal) as total_vendido
                 FROM DetalleVenta d
                 JOIN Producto p ON d.idProducto = p.idProducto
                 JOIN Venta v ON d.idVenta = v.idVenta
                 LEFT JOIN Categoria c ON p.idCategoria = c.idCategoria
                 {fecha_condition}
                 GROUP BY p.idProducto
                 ORDER BY cantidad_vendida DESC
                 LIMIT ?"""
        
        query_params.append(limite)
        rows = self.db.fetch_all(query, tuple(query_params))
        
        return [{
            'id': row['idProducto'],
            'nombre': row['NombrePro'],
            'categoria': row['NombreCat'],
            'cantidad_vendida': row['cantidad_vendida'],
            'total_vendido': row['total_vendido']
        } for row in rows]
    
    def exportar_reporte_productos(self, fecha_inicio=None, fecha_fin=None, limite=10):
        """Exporta el reporte de productos más vendidos a CSV"""
        productos = self.generar_reporte_productos_vendidos(fecha_inicio, fecha_fin, limite)
        data = [[p['id'], p['nombre'], p['categoria'], p['cantidad_vendida'], format_currency(p['total_vendido'])] for p in productos]
        headers = ['ID', 'Producto', 'Categoría', 'Cantidad Vendida', 'Total Vendido']
        filename = f"reporte_productos_{datetime.date.today().strftime('%Y%m%d')}.csv"
        return export_to_csv(data, filename, headers)
    
    def generar_reporte_clientes_frecuentes(self, limite=10):
        """Genera un reporte de clientes frecuentes"""
        query = """SELECT c.*, COUNT(v.idVenta) as total_compras, SUM(v.Total) as total_gastado
                 FROM Cliente c
                 LEFT JOIN Venta v ON c.idCliente = v.idCliente
                 GROUP BY c.idCliente
                 ORDER BY total_compras DESC
                 LIMIT ?"""
        rows = self.db.fetch_all(query, (limite,))
        return [{
            'id': row['idCliente'],
            'nombre': row['NombreCli'],
            'telefono': row['TelefonoCli'],
            'dni': row['Dni'],
            'direccion': row['DireccionClie'],
            'total_compras': row['total_compras'],
            'total_gastado': row['total_gastado'] or 0
        } for row in rows]
    
    def exportar_reporte_clientes(self, limite=10):
        """Exporta el reporte de clientes frecuentes a CSV"""
        clientes = self.generar_reporte_clientes_frecuentes(limite)
        data = [[c['id'], c['nombre'], c['dni'], c['telefono'], c['total_compras'], format_currency(c['total_gastado'])] for c in clientes]
        headers = ['ID', 'Cliente', 'DNI', 'Teléfono', 'Total Compras', 'Total Gastado']
        filename = f"reporte_clientes_{datetime.date.today().strftime('%Y%m%d')}.csv"
        return export_to_csv(data, filename, headers)
    
    def generar_reporte_stock_bajo(self, limite=10):
        """Genera un reporte de productos con stock bajo"""
        query = """SELECT p.*, c.NombreCat
                 FROM Producto p
                 LEFT JOIN Categoria c ON p.idCategoria = c.idCategoria
                 WHERE p.Stock <= ?
                 ORDER BY p.Stock ASC"""
        rows = self.db.fetch_all(query, (limite,))
        return [{
            'id': row['idProducto'],
            'nombre': row['NombrePro'],
            'precio': row['Precio'],
            'stock': row['Stock'],
            'categoria': row['NombreCat']
        } for row in rows]
    
    def exportar_reporte_stock(self, limite=10):
        """Exporta el reporte de stock bajo a CSV"""
        productos = self.generar_reporte_stock_bajo(limite)
        data = [[p['id'], p['nombre'], p['categoria'], p['stock'], format_currency(p['precio'])] for p in productos]
        headers = ['ID', 'Producto', 'Categoría', 'Stock', 'Precio']
        filename = f"reporte_stock_{datetime.date.today().strftime('%Y%m%d')}.csv"
        return export_to_csv(data, filename, headers)