import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from controllers.venta_controller import VentaController
from controllers.factura_controller import FacturaController
from controllers.cliente_controller import ClienteController
from controllers.empleado_controller import EmpleadoController
from database.models import DetalleVenta
import datetime

class GenerarFacturaView:
    def __init__(self, parent):
        self.parent = parent
        self.venta_controller = VentaController()
        self.factura_controller = FacturaController()
        self.cliente_controller = ClienteController()
        self.empleado_controller = EmpleadoController()
        
        self.setup_ui()
        self.cargar_ventas()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, text="Generar Factura desde Venta", 
                               font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Frame para filtros
        filter_frame = ttk.LabelFrame(main_frame, text="Filtros", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Filtro por cliente
        ttk.Label(filter_frame, text="Cliente:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.cliente_var = tk.StringVar()
        self.cliente_combo = ttk.Combobox(filter_frame, textvariable=self.cliente_var, 
                                         state="readonly", width=30)
        self.cliente_combo.grid(row=0, column=1, padx=(0, 20))
        
        # Filtro por fecha
        ttk.Label(filter_frame, text="Desde:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.fecha_desde = ttk.DateEntry(filter_frame)
        self.fecha_desde.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(filter_frame, text="Hasta:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        self.fecha_hasta = ttk.DateEntry(filter_frame)
        self.fecha_hasta.grid(row=0, column=5, padx=(0, 20))
        
        # Botón filtrar
        btn_filtrar = ttk.Button(filter_frame, text="Filtrar", command=self.filtrar_ventas)
        btn_filtrar.grid(row=0, column=6)
        
        # Frame para la lista de ventas
        ventas_frame = ttk.LabelFrame(main_frame, text="Ventas Disponibles", padding=10)
        ventas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Treeview para ventas
        columns = ('ID', 'Fecha', 'Cliente', 'Empleado', 'Total', 'Facturada')
        self.ventas_tree = ttk.Treeview(ventas_frame, columns=columns, show='headings', height=10)
        
        # Configurar columnas
        self.ventas_tree.heading('ID', text='ID')
        self.ventas_tree.heading('Fecha', text='Fecha')
        self.ventas_tree.heading('Cliente', text='Cliente')
        self.ventas_tree.heading('Empleado', text='Empleado')
        self.ventas_tree.heading('Total', text='Total')
        self.ventas_tree.heading('Facturada', text='Facturada')
        
        self.ventas_tree.column('ID', width=60)
        self.ventas_tree.column('Fecha', width=100)
        self.ventas_tree.column('Cliente', width=200)
        self.ventas_tree.column('Empleado', width=150)
        self.ventas_tree.column('Total', width=100)
        self.ventas_tree.column('Facturada', width=80)
        
        # Scrollbar para el treeview
        scrollbar = ttk.Scrollbar(ventas_frame, orient=tk.VERTICAL, command=self.ventas_tree.yview)
        self.ventas_tree.configure(yscrollcommand=scrollbar.set)
        
        self.ventas_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para configuración de factura
        config_frame = ttk.LabelFrame(main_frame, text="Configuración de Factura", padding=10)
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Porcentaje de impuesto
        ttk.Label(config_frame, text="Impuesto (%):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.impuesto_var = tk.DoubleVar(value=18.0)  # IVA por defecto
        impuesto_spin = ttk.Spinbox(config_frame, from_=0, to=100, increment=0.1, 
                                   textvariable=self.impuesto_var, width=10)
        impuesto_spin.grid(row=0, column=1, padx=(0, 20))
        
        # Estado de la factura
        ttk.Label(config_frame, text="Estado:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.estado_var = tk.StringVar(value="Pendiente")
        estado_combo = ttk.Combobox(config_frame, textvariable=self.estado_var, 
                                   values=["Pendiente", "Pagada", "Cancelada"], 
                                   state="readonly", width=15)
        estado_combo.grid(row=0, column=3, padx=(0, 20))
        
        # Observaciones
        ttk.Label(config_frame, text="Observaciones:").grid(row=1, column=0, sticky=tk.NW, padx=(0, 10), pady=(10, 0))
        self.observaciones_text = tk.Text(config_frame, height=3, width=50)
        self.observaciones_text.grid(row=1, column=1, columnspan=3, pady=(10, 0), sticky=tk.W)
        
        # Frame para botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X)
        
        # Botones
        btn_generar = ttk.Button(buttons_frame, text="Generar Factura", 
                                bootstyle=SUCCESS, command=self.generar_factura)
        btn_generar.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_ver_detalle = ttk.Button(buttons_frame, text="Ver Detalle de Venta", 
                                    command=self.ver_detalle_venta)
        btn_ver_detalle.pack(side=tk.LEFT, padx=(0, 10))
        
        btn_actualizar = ttk.Button(buttons_frame, text="Actualizar Lista", 
                                   command=self.cargar_ventas)
        btn_actualizar.pack(side=tk.LEFT)
    
    def cargar_ventas(self):
        """Carga todas las ventas en el treeview"""
        # Limpiar treeview
        for item in self.ventas_tree.get_children():
            self.ventas_tree.delete(item)
        
        # Cargar clientes para el filtro
        clientes = self.cliente_controller.listar_clientes()
        cliente_values = ["Todos"] + [f"{c.id} - {c.nombre}" for c in clientes]
        self.cliente_combo['values'] = cliente_values
        self.cliente_combo.set("Todos")
        
        # Obtener ventas con información completa
        try:
            query = """
            SELECT v.idVenta, v.Fecha, v.Total, v.idCliente, v.idEmpleado,
                   c.NombreCli, e.NombreEmp,
                   CASE WHEN f.idFactura IS NOT NULL THEN 'Sí' ELSE 'No' END as Facturada
            FROM Venta v
            LEFT JOIN Cliente c ON v.idCliente = c.idCliente
            LEFT JOIN Empleado e ON v.idEmpleado = e.idEmpleado
            LEFT JOIN Factura f ON v.idVenta = f.idVenta
            ORDER BY v.Fecha DESC
            """
            
            from database.connection import DatabaseConnection
            db = DatabaseConnection()
            ventas = db.fetch_all(query)
            
            for venta in ventas:
                self.ventas_tree.insert('', 'end', values=(
                    venta['idVenta'],
                    venta['Fecha'],
                    venta['NombreCli'] or 'Sin cliente',
                    venta['NombreEmp'] or 'Sin empleado',
                    f"${venta['Total']:.2f}",
                    venta['Facturada']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ventas: {e}")
    
    def filtrar_ventas(self):
        """Filtra las ventas según los criterios seleccionados"""
        # Limpiar treeview
        for item in self.ventas_tree.get_children():
            self.ventas_tree.delete(item)
        
        try:
            conditions = []
            params = []
            
            # Filtro por cliente
            if self.cliente_var.get() and self.cliente_var.get() != "Todos":
                cliente_id = self.cliente_var.get().split(" - ")[0]
                conditions.append("v.idCliente = ?")
                params.append(cliente_id)
            
            # Filtro por fecha
            if self.fecha_desde.entry.get():
                conditions.append("v.Fecha >= ?")
                params.append(self.fecha_desde.entry.get())
            
            if self.fecha_hasta.entry.get():
                conditions.append("v.Fecha <= ?")
                params.append(self.fecha_hasta.entry.get())
            
            where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""
            
            query = f"""
            SELECT v.idVenta, v.Fecha, v.Total, v.idCliente, v.idEmpleado,
                   c.NombreCli, e.NombreEmp,
                   CASE WHEN f.idFactura IS NOT NULL THEN 'Sí' ELSE 'No' END as Facturada
            FROM Venta v
            LEFT JOIN Cliente c ON v.idCliente = c.idCliente
            LEFT JOIN Empleado e ON v.idEmpleado = e.idEmpleado
            LEFT JOIN Factura f ON v.idVenta = f.idVenta
            {where_clause}
            ORDER BY v.Fecha DESC
            """
            
            from database.connection import DatabaseConnection
            db = DatabaseConnection()
            ventas = db.fetch_all(query, tuple(params))
            
            for venta in ventas:
                self.ventas_tree.insert('', 'end', values=(
                    venta['idVenta'],
                    venta['Fecha'],
                    venta['NombreCli'] or 'Sin cliente',
                    venta['NombreEmp'] or 'Sin empleado',
                    f"${venta['Total']:.2f}",
                    venta['Facturada']
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al filtrar ventas: {e}")
    
    def generar_factura(self):
        """Genera una factura desde la venta seleccionada"""
        selected = self.ventas_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una venta para generar la factura.")
            return
        
        # Obtener datos de la venta seleccionada
        item = self.ventas_tree.item(selected[0])
        venta_id = item['values'][0]
        facturada = item['values'][5]
        
        if facturada == "Sí":
            messagebox.showwarning("Advertencia", "Esta venta ya tiene una factura generada.")
            return
        
        try:
            # Obtener la venta completa
            from database.models import Venta
            venta = Venta.get_by_id(venta_id)
            
            if not venta:
                messagebox.showerror("Error", "No se pudo encontrar la venta.")
                return
            
            # Calcular valores (con validación robusta)
            try:
                subtotal = float(venta.total) if venta.total else 0.0
            except (ValueError, TypeError):
                subtotal = 0.0
                
            try:
                impuesto_porcentaje = float(self.impuesto_var.get())
            except (ValueError, TypeError):
                impuesto_porcentaje = 18.0  # Valor por defecto
                
            impuesto = subtotal * (impuesto_porcentaje / 100)
            total = subtotal + impuesto
            
            # Obtener observaciones
            observaciones = self.observaciones_text.get("1.0", tk.END).strip()
            if not observaciones:
                observaciones = None
            
            # Crear la factura
            numero_factura = self.factura_controller.generar_numero_factura()
            
            factura_id = self.factura_controller.crear_factura(
                numero_factura=numero_factura,
                subtotal=subtotal,
                impuesto=impuesto,
                total=total,
                estado=self.estado_var.get(),
                observaciones=observaciones,
                id_venta=venta.id,
                id_cliente=venta.id_cliente,
                id_empleado=venta.id_empleado
            )
            
            if factura_id:
                messagebox.showinfo("Éxito", 
                                   f"Factura {numero_factura} generada exitosamente.\n"
                                   f"Subtotal: ${subtotal:.2f}\n"
                                   f"Impuesto ({impuesto_porcentaje}%): ${impuesto:.2f}\n"
                                   f"Total: ${total:.2f}")
                
                # Actualizar la lista
                self.cargar_ventas()
                
                # Limpiar observaciones
                self.observaciones_text.delete("1.0", tk.END)
            else:
                messagebox.showerror("Error", "No se pudo generar la factura.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar factura: {e}")
    
    def ver_detalle_venta(self):
        """Muestra el detalle de la venta seleccionada"""
        selected = self.ventas_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione una venta para ver el detalle.")
            return
        
        # Obtener datos de la venta seleccionada
        item = self.ventas_tree.item(selected[0])
        venta_id = item['values'][0]
        
        try:
            # Obtener detalles de la venta
            detalles = DetalleVenta.get_by_venta(venta_id)
            
            if not detalles:
                messagebox.showinfo("Información", "Esta venta no tiene detalles registrados.")
                return
            
            # Crear ventana de detalle
            detalle_window = tk.Toplevel(self.parent)
            detalle_window.title(f"Detalle de Venta #{venta_id}")
            detalle_window.geometry("600x400")
            detalle_window.transient(self.parent)
            detalle_window.grab_set()
            
            # Treeview para detalles
            columns = ('Producto', 'Cantidad', 'Precio Unit.', 'Subtotal')
            detalle_tree = ttk.Treeview(detalle_window, columns=columns, show='headings')
            
            for col in columns:
                detalle_tree.heading(col, text=col)
                detalle_tree.column(col, width=120)
            
            # Cargar detalles
            total_venta = 0
            for detalle in detalles:
                # Obtener nombre del producto
                from database.models import Producto
                producto = Producto.get_by_id(detalle.id_producto)
                nombre_producto = producto.nombre if producto else f"Producto #{detalle.id_producto}"
                
                detalle_tree.insert('', 'end', values=(
                    nombre_producto,
                    detalle.cantidad,
                    f"${detalle.precio:.2f}",
                    f"${detalle.subtotal:.2f}"
                ))
                total_venta += detalle.subtotal
            
            detalle_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Mostrar total
            total_label = ttk.Label(detalle_window, text=f"Total de la Venta: ${total_venta:.2f}", 
                                   font=("Helvetica", 12, "bold"))
            total_label.pack(pady=10)
            
            # Botón cerrar
            btn_cerrar = ttk.Button(detalle_window, text="Cerrar", 
                                   command=detalle_window.destroy)
            btn_cerrar.pack(pady=10)
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar detalle: {e}")