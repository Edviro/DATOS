from database.models import Factura, Cliente, Empleado, Venta, DetalleFactura, Producto
from database.connection import DatabaseConnection
from utils.helpers import export_to_csv, export_to_excel, generate_invoice_pdf, format_currency, format_date
import datetime

class FacturaController:
    def __init__(self):
        self.db = DatabaseConnection()
    
    def crear_factura(self, numero_factura, subtotal, impuesto, total, 
                     estado='Pendiente', observaciones=None, id_venta=None, 
                     id_cliente=None, id_empleado=None):
        """Crea una nueva factura"""
        try:
            factura = Factura(
                numero_factura=numero_factura,
                fecha=datetime.date.today().isoformat(),
                subtotal=subtotal,
                impuesto=impuesto,
                total=total,
                estado=estado,
                observaciones=observaciones,
                id_venta=id_venta,
                id_cliente=id_cliente,
                id_empleado=id_empleado
            )
            return factura.save()
        except Exception as e:
            print(f"Error al crear factura: {e}")
            return None
    
    def actualizar_factura(self, id_factura, numero_factura=None, subtotal=None, 
                          impuesto=None, total=None, estado=None, observaciones=None,
                          id_venta=None, id_cliente=None, id_empleado=None):
        """Actualiza una factura existente"""
        try:
            factura = Factura.get_by_id(id_factura)
            if factura:
                if numero_factura is not None:
                    factura.numero_factura = numero_factura
                if subtotal is not None:
                    factura.subtotal = subtotal
                if impuesto is not None:
                    factura.impuesto = impuesto
                if total is not None:
                    factura.total = total
                if estado is not None:
                    factura.estado = estado
                if observaciones is not None:
                    factura.observaciones = observaciones
                if id_venta is not None:
                    factura.id_venta = id_venta
                if id_cliente is not None:
                    factura.id_cliente = id_cliente
                if id_empleado is not None:
                    factura.id_empleado = id_empleado
                
                return factura.save()
            return None
        except Exception as e:
            print(f"Error al actualizar factura: {e}")
            return None
    
    def eliminar_factura(self, id_factura):
        """Elimina una factura"""
        try:
            factura = Factura.get_by_id(id_factura)
            if factura:
                return factura.delete()
            return False
        except Exception as e:
            print(f"Error al eliminar factura: {e}")
            return False
    
    def obtener_factura(self, id_factura):
        """Obtiene una factura por ID"""
        return Factura.get_by_id(id_factura)
    
    def obtener_factura_por_numero(self, numero_factura):
        """Obtiene una factura por número"""
        return Factura.get_by_numero(numero_factura)
    
    def listar_facturas(self):
        """Lista todas las facturas"""
        return Factura.get_all()
    
    def listar_facturas_por_cliente(self, id_cliente):
        """Lista facturas de un cliente específico"""
        return Factura.get_by_cliente(id_cliente)
    
    def listar_facturas_por_estado(self, estado):
        """Lista facturas por estado"""
        return Factura.get_by_estado(estado)
    
    def generar_numero_factura(self):
        """Genera un número de factura único"""
        try:
            # Obtener el último número de factura
            query = "SELECT MAX(CAST(SUBSTR(NumeroFactura, 5) AS INTEGER)) as ultimo FROM Factura WHERE NumeroFactura LIKE 'FAC-%'"
            result = self.db.fetch_one(query)
            
            if result and result['ultimo']:
                siguiente = result['ultimo'] + 1
            else:
                siguiente = 1
            
            return f"FAC-{siguiente:06d}"
        except Exception as e:
            print(f"Error al generar número de factura: {e}")
            return f"FAC-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def cambiar_estado_factura(self, id_factura, nuevo_estado):
        """Cambia el estado de una factura"""
        estados_validos = ['Pendiente', 'Pagada', 'Cancelada', 'Vencida']
        if nuevo_estado not in estados_validos:
            return False
        
        return self.actualizar_factura(id_factura, estado=nuevo_estado)
    
    def generar_reporte_facturas(self, fecha_inicio=None, fecha_fin=None, estado=None):
        """Genera un reporte de facturas con filtros opcionales"""
        try:
            query_params = []
            conditions = []
            
            if fecha_inicio and fecha_fin:
                conditions.append("f.Fecha BETWEEN ? AND ?")
                query_params.extend([fecha_inicio, fecha_fin])
            
            if estado:
                conditions.append("f.Estado = ?")
                query_params.append(estado)
            
            where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
            
            query = f"""SELECT f.idFactura, f.NumeroFactura, f.Fecha, f.SubTotal, 
                           f.Impuesto, f.Total, f.Estado, f.Observaciones,
                           c.NombreCli, e.NombreEmp, v.idVenta
                    FROM Factura f
                    LEFT JOIN Cliente c ON f.idCliente = c.idCliente
                    LEFT JOIN Empleado e ON f.idEmpleado = e.idEmpleado
                    LEFT JOIN Venta v ON f.idVenta = v.idVenta
                    {where_clause}
                    ORDER BY f.Fecha DESC"""
            
            rows = self.db.fetch_all(query, tuple(query_params))
            return [{
                'id': row['idFactura'],
                'numero': row['NumeroFactura'],
                'fecha': format_date(row['Fecha']),
                'subtotal': row['SubTotal'],
                'impuesto': row['Impuesto'],
                'total': row['Total'],
                'estado': row['Estado'],
                'observaciones': row['Observaciones'],
                'cliente': row['NombreCli'],
                'empleado': row['NombreEmp'],
                'id_venta': row['idVenta']
            } for row in rows]
        except Exception as e:
            print(f"Error al generar reporte de facturas: {e}")
            return []
    
    def exportar_reporte_facturas(self, fecha_inicio=None, fecha_fin=None, estado=None, formato='csv'):
        """Exporta el reporte de facturas en el formato especificado (csv, excel)"""
        try:
            facturas = self.generar_reporte_facturas(fecha_inicio, fecha_fin, estado)
            
            # Preparar datos
            headers = ['Número', 'Fecha', 'Cliente', 'Empleado', 'Subtotal', 'Impuesto', 'Total', 'Estado', 'Observaciones']
            data = []
            
            for factura in facturas:
                data.append([
                    factura['numero'],
                    factura['fecha'],
                    factura['cliente'] or 'N/A',
                    factura['empleado'] or 'N/A',
                    factura['subtotal'],
                    factura['impuesto'],
                    factura['total'],
                    factura['estado'],
                    factura['observaciones'] or ''
                ])
            
            # Generar nombre de archivo
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if formato.lower() == 'excel':
                filename = f"reporte_facturas_{timestamp}.xlsx"
                return export_to_excel(data, filename, headers, "Reporte de Facturas")
            else:
                filename = f"reporte_facturas_{timestamp}.csv"
                return export_to_csv(data, filename, headers)
        
        except Exception as e:
            print(f"Error al exportar reporte: {e}")
            return None
    
    def exportar_factura_pdf(self, factura_id):
        """Exporta una factura individual en formato PDF"""
        try:
            # Obtener datos completos de la factura
            query = """
            SELECT f.*, c.NombreCli as cliente_nombre, e.NombreEmp as empleado_nombre
            FROM Factura f
            LEFT JOIN Cliente c ON f.idCliente = c.idCliente
            LEFT JOIN Empleado e ON f.idEmpleado = e.idEmpleado
            WHERE f.idFactura = ?
            """
            
            factura_data = self.db.fetch_one(query, (factura_id,))
            
            if not factura_data:
                return None
            
            # Preparar datos para el PDF
            pdf_data = {
                'numero': factura_data['NumeroFactura'],
                'fecha': factura_data['Fecha'],
                'subtotal': factura_data['SubTotal'],
                'impuesto': factura_data['Impuesto'],
                'total': factura_data['Total'],
                'estado': factura_data['Estado'],
                'observaciones': factura_data['Observaciones'],
                'cliente': factura_data['cliente_nombre'] or 'Cliente no especificado',
                'empleado': factura_data['empleado_nombre'] or 'Empleado no especificado'
            }
            
            # Generar nombre de archivo
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"factura_{pdf_data['numero']}_{timestamp}.pdf"
            
            return generate_invoice_pdf(pdf_data, filename)
        
        except Exception as e:
            print(f"Error al exportar factura a PDF: {e}")
            return None
    
    def exportar_factura_excel(self, factura_id):
        """Exporta una factura individual en formato Excel"""
        try:
            # Obtener datos completos de la factura
            query = """
            SELECT f.*, c.NombreCli as cliente_nombre, e.NombreEmp as empleado_nombre
            FROM Factura f
            LEFT JOIN Cliente c ON f.idCliente = c.idCliente
            LEFT JOIN Empleado e ON f.idEmpleado = e.idEmpleado
            WHERE f.idFactura = ?
            """
            
            factura_data = self.db.fetch_one(query, (factura_id,))
            
            if not factura_data:
                return None
            
            # Preparar datos para Excel
            headers = ['Campo', 'Valor']
            data = [
                ['Número de Factura', factura_data['NumeroFactura']],
                ['Fecha', factura_data['Fecha']],
                ['Cliente', factura_data['cliente_nombre'] or 'No especificado'],
                ['Empleado', factura_data['empleado_nombre'] or 'No especificado'],
                ['Subtotal', format_currency(factura_data['SubTotal'])],
                ['Impuesto', format_currency(factura_data['Impuesto'])],
                ['Total', format_currency(factura_data['Total'])],
                ['Estado', factura_data['Estado']],
                ['Observaciones', factura_data['Observaciones'] or 'Sin observaciones']
            ]
            
            # Generar nombre de archivo
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"factura_{factura_data['NumeroFactura']}_{timestamp}.xlsx"
            
            return export_to_excel(data, filename, headers, f"Factura {factura_data['NumeroFactura']}")
        
        except Exception as e:
            print(f"Error al exportar factura a Excel: {e}")
            return None
    
    def obtener_estadisticas_facturas(self):
        """Obtiene estadísticas generales de facturas"""
        try:
            query = """SELECT 
                        COUNT(*) as total_facturas,
                        SUM(CASE WHEN Estado = 'Pendiente' THEN 1 ELSE 0 END) as pendientes,
                        SUM(CASE WHEN Estado = 'Pagada' THEN 1 ELSE 0 END) as pagadas,
                        SUM(CASE WHEN Estado = 'Cancelada' THEN 1 ELSE 0 END) as canceladas,
                        SUM(CASE WHEN Estado = 'Vencida' THEN 1 ELSE 0 END) as vencidas,
                        SUM(Total) as total_monto,
                        AVG(Total) as promedio_monto
                    FROM Factura"""
            
            result = self.db.fetch_one(query)
            return {
                'total_facturas': result['total_facturas'] or 0,
                'pendientes': result['pendientes'] or 0,
                'pagadas': result['pagadas'] or 0,
                'canceladas': result['canceladas'] or 0,
                'vencidas': result['vencidas'] or 0,
                'total_monto': result['total_monto'] or 0,
                'promedio_monto': result['promedio_monto'] or 0
            }
        except Exception as e:
            print(f"Error al obtener estadísticas: {e}")
            return {}
    
    def crear_factura_desde_venta(self, id_venta, impuesto_porcentaje=0):
        """Crea una factura automáticamente desde una venta"""
        try:
            venta = Venta.get_by_id(id_venta)
            if not venta:
                return None
            
            numero_factura = self.generar_numero_factura()
            subtotal = venta.total
            impuesto = subtotal * (impuesto_porcentaje / 100)
            total = subtotal + impuesto
            
            return self.crear_factura(
                numero_factura=numero_factura,
                subtotal=subtotal,
                impuesto=impuesto,
                total=total,
                id_venta=id_venta,
                id_cliente=venta.id_cliente,
                id_empleado=venta.id_empleado
            )
        except Exception as e:
            print(f"Error al crear factura desde venta: {e}")
            return None
    
    def agregar_producto_factura(self, id_factura, id_producto, cantidad):
        """Agrega un producto a una factura y recalcula totales"""
        try:
            producto = Producto.get_by_id(id_producto)
            if not producto:
                return False
            
            # Calcular subtotal del producto
            subtotal_producto = producto.precio * cantidad
            
            # Crear detalle de factura
            detalle = DetalleFactura(
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=subtotal_producto,
                id_producto=id_producto,
                id_factura=id_factura
            )
            
            if detalle.save():
                # Recalcular totales de la factura
                self.recalcular_totales_factura(id_factura)
                return True
            return False
        except Exception as e:
            print(f"Error al agregar producto a factura: {e}")
            return False
    
    def eliminar_producto_factura(self, id_detalle_factura):
        """Elimina un producto de una factura y recalcula totales"""
        try:
            detalle = DetalleFactura.get_by_id(id_detalle_factura)
            if detalle:
                id_factura = detalle.id_factura
                if detalle.delete():
                    # Recalcular totales de la factura
                    self.recalcular_totales_factura(id_factura)
                    return True
            return False
        except Exception as e:
            print(f"Error al eliminar producto de factura: {e}")
            return False
    
    def obtener_detalles_factura(self, id_factura):
        """Obtiene todos los detalles de una factura"""
        try:
            return DetalleFactura.get_by_factura(id_factura)
        except Exception as e:
            print(f"Error al obtener detalles de factura: {e}")
            return []
    
    def recalcular_totales_factura(self, id_factura, impuesto_porcentaje=0):
        """Recalcula los totales de una factura basado en sus detalles"""
        try:
            detalles = DetalleFactura.get_by_factura(id_factura)
            subtotal = sum(detalle.subtotal for detalle in detalles)
            impuesto = subtotal * (impuesto_porcentaje / 100)
            total = subtotal + impuesto
            
            return self.actualizar_factura(
                id_factura=id_factura,
                subtotal=subtotal,
                impuesto=impuesto,
                total=total
            )
        except Exception as e:
            print(f"Error al recalcular totales de factura: {e}")
            return False
    
    def crear_factura_con_productos(self, numero_factura, productos_data, impuesto_porcentaje=0,
                                   estado='Pendiente', observaciones=None, id_cliente=None, id_empleado=None):
        """Crea una factura nueva con productos automáticamente"""
        try:
            # Crear factura inicial con totales en 0
            factura_id = self.crear_factura(
                numero_factura=numero_factura,
                subtotal=0,
                impuesto=0,
                total=0,
                estado=estado,
                observaciones=observaciones,
                id_cliente=id_cliente,
                id_empleado=id_empleado
            )
            
            if not factura_id:
                return None
            
            # Agregar productos
            for producto_data in productos_data:
                id_producto = producto_data['id_producto']
                cantidad = producto_data['cantidad']
                
                if not self.agregar_producto_factura(factura_id, id_producto, cantidad):
                    # Si falla, eliminar la factura creada
                    self.eliminar_factura(factura_id)
                    return None
            
            # Recalcular totales finales
            self.recalcular_totales_factura(factura_id, impuesto_porcentaje)
            
            return factura_id
        except Exception as e:
            print(f"Error al crear factura con productos: {e}")
            return None