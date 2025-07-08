import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controllers.factura_controller import FacturaController
from controllers.cliente_controller import ClienteController
from controllers.empleado_controller import EmpleadoController
from controllers.venta_controller import VentaController
from controllers.producto_controller import ProductoController
from utils.validators import validate_required, validate_number, validate_integer
from utils.helpers import format_currency
import datetime

class FacturaView:
    def __init__(self, parent):
        self.parent = parent
        self.factura_controller = FacturaController()
        self.cliente_controller = ClienteController()
        self.empleado_controller = EmpleadoController()
        self.venta_controller = VentaController()
        self.producto_controller = ProductoController()
        
        # Variables para manejo de productos
        self.productos_factura = []
        self.factura_actual_id = None
        
        self.setup_ui()
        self.cargar_datos()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(main_frame, text="Gestión de Facturas", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de lista de facturas
        self.setup_lista_tab()
        
        # Pestaña de crear/editar factura
        self.setup_form_tab()
    
    def setup_lista_tab(self):
        """Configura la pestaña de lista de facturas"""
        lista_frame = ttk.Frame(self.notebook)
        self.notebook.add(lista_frame, text="Lista de Facturas")
        
        # Frame de filtros
        filter_frame = ttk.LabelFrame(lista_frame, text="Filtros")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Filtro por estado
        ttk.Label(filter_frame, text="Estado:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.estado_filter = ttk.Combobox(filter_frame, values=['Todos', 'Pendiente', 'Pagada', 'Cancelada', 'Vencida'])
        self.estado_filter.set('Todos')
        self.estado_filter.grid(row=0, column=1, padx=5, pady=5)
        self.estado_filter.bind('<<ComboboxSelected>>', self.filtrar_facturas)
        
        # Botones de acción
        button_frame = ttk.Frame(filter_frame)
        button_frame.grid(row=0, column=2, padx=20, pady=5)
        
        ttk.Button(button_frame, text="Actualizar", command=self.cargar_facturas).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Nueva Factura", command=self.nueva_factura).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Editar", command=self.editar_factura).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Eliminar", command=self.eliminar_factura).pack(side=tk.LEFT, padx=2)
        
        # Botones de exportación
        export_frame = ttk.Frame(filter_frame)
        export_frame.grid(row=1, column=0, columnspan=3, pady=5)
        
        ttk.Button(export_frame, text="Exportar PDF", command=self.exportar_factura_pdf).pack(side=tk.LEFT, padx=2)
        ttk.Button(export_frame, text="Exportar Excel", command=self.exportar_factura_excel).pack(side=tk.LEFT, padx=2)
        
        # Treeview para mostrar facturas
        tree_frame = ttk.Frame(lista_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        columns = ('ID', 'Número', 'Fecha', 'Cliente', 'Total', 'Estado')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.tree.heading('ID', text='ID')
        self.tree.heading('Número', text='Número')
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Cliente', text='Cliente')
        self.tree.heading('Total', text='Total')
        self.tree.heading('Estado', text='Estado')
        
        self.tree.column('ID', width=50)
        self.tree.column('Número', width=120)
        self.tree.column('Fecha', width=100)
        self.tree.column('Cliente', width=200)
        self.tree.column('Total', width=100)
        self.tree.column('Estado', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Doble clic para editar
        self.tree.bind('<Double-1>', lambda e: self.editar_factura())
    
    def setup_form_tab(self):
        """Configura la pestaña del formulario"""
        form_frame = ttk.Frame(self.notebook)
        self.notebook.add(form_frame, text="Crear/Editar Factura")
        
        # Frame del formulario
        form_container = ttk.LabelFrame(form_frame, text="Datos de la Factura")
        form_container.pack(fill=tk.X, padx=10, pady=10)
        
        # Variables del formulario
        self.factura_id = tk.StringVar()
        self.numero_factura = tk.StringVar()
        self.fecha_factura = tk.StringVar()
        self.subtotal_var = tk.StringVar()
        self.impuesto_var = tk.StringVar()
        self.total_var = tk.StringVar()
        self.estado_var = tk.StringVar()
        self.observaciones_var = tk.StringVar()
        self.cliente_var = tk.StringVar()
        self.empleado_var = tk.StringVar()
        self.venta_var = tk.StringVar()
        
        # Campos del formulario
        row = 0
        
        # Número de factura
        ttk.Label(form_container, text="Número de Factura:").grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        numero_entry = ttk.Entry(form_container, textvariable=self.numero_factura, width=30, state="readonly")
        numero_entry.grid(row=row, column=1, padx=5, pady=5)
        ttk.Button(form_container, text="Generar", command=self.generar_numero).grid(row=row, column=2, padx=5, pady=5)
        row += 1
        
        # Fecha
        ttk.Label(form_container, text="Fecha:").grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(form_container, textvariable=self.fecha_factura, width=30).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Cliente
        ttk.Label(form_container, text="Cliente:").grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        self.cliente_combo = ttk.Combobox(form_container, textvariable=self.cliente_var, width=27, state="readonly")
        self.cliente_combo.grid(row=row, column=1, padx=5, pady=5)
        self.cliente_combo.bind('<<ComboboxSelected>>', self.on_cliente_selected)
        row += 1
        
        # Venta relacionada (opcional)
        ttk.Label(form_container, text="Venta (opcional):").grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        self.venta_combo = ttk.Combobox(form_container, textvariable=self.venta_var, width=27, state="readonly")
        self.venta_combo.grid(row=row, column=1, padx=5, pady=5)
        self.venta_combo.bind('<<ComboboxSelected>>', self.on_venta_selected)
        row += 1
        
        # Sección de productos - SIMPLIFICADA
        productos_frame = ttk.LabelFrame(form_container, text="Productos de la Factura", padding="10")
        productos_frame.grid(row=row, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        row += 1
        
        # Selección de producto
        producto_input_frame = ttk.Frame(productos_frame)
        producto_input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(producto_input_frame, text="Producto:").pack(side=tk.LEFT, padx=(0, 5))
        self.producto_var = tk.StringVar()
        self.producto_combo = ttk.Combobox(producto_input_frame, textvariable=self.producto_var, 
                                          width=25, state="readonly")
        self.producto_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(producto_input_frame, text="Cantidad:").pack(side=tk.LEFT, padx=(0, 5))
        self.cantidad_var = tk.StringVar(value="1")
        cantidad_spin = tk.Spinbox(producto_input_frame, textvariable=self.cantidad_var, 
                                  from_=1, to=1000, width=8)
        cantidad_spin.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(producto_input_frame, text="Agregar", 
                  command=self.agregar_producto).pack(side=tk.LEFT, padx=5)
        ttk.Button(producto_input_frame, text="Eliminar", 
                  command=self.eliminar_producto).pack(side=tk.LEFT, padx=5)
        
        # Lista de productos agregados
        productos_list_frame = ttk.Frame(productos_frame)
        productos_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview para productos
        columns = ('Producto', 'Cantidad', 'Precio Unit.', 'Subtotal')
        self.productos_tree = ttk.Treeview(productos_list_frame, columns=columns, show='headings', height=6)
        
        for col in columns:
            self.productos_tree.heading(col, text=col)
            self.productos_tree.column(col, width=120)
        
        # Scrollbar para productos
        productos_scrollbar = ttk.Scrollbar(productos_list_frame, orient=tk.VERTICAL, command=self.productos_tree.yview)
        self.productos_tree.configure(yscrollcommand=productos_scrollbar.set)
        
        self.productos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        productos_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para cálculos automáticos - MOVIDO DESPUÉS DE PRODUCTOS
        calc_frame = ttk.LabelFrame(form_container, text="Totales", padding=10)
        calc_frame.grid(row=row, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        row += 1
        
        # Organizar cálculos en una fila
        ttk.Label(calc_frame, text="Subtotal:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.subtotal_display = ttk.Label(calc_frame, textvariable=self.subtotal_var, 
                                         font=("Helvetica", 10, "bold"), foreground="blue")
        self.subtotal_display.grid(row=0, column=1, padx=5, sticky=tk.W)
        
        ttk.Label(calc_frame, text="Impuesto %:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.impuesto_porcentaje = tk.DoubleVar(value=18.0)
        impuesto_spin = ttk.Spinbox(calc_frame, from_=0, to=100, increment=0.1, 
                                   textvariable=self.impuesto_porcentaje, width=8,
                                   command=self.calcular_totales)
        impuesto_spin.grid(row=0, column=3, padx=5)
        impuesto_spin.bind('<KeyRelease>', lambda e: self.calcular_totales())
        
        ttk.Label(calc_frame, text="Impuesto $:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.impuesto_display = ttk.Label(calc_frame, textvariable=self.impuesto_var, 
                                         font=("Helvetica", 10, "bold"), foreground="orange")
        self.impuesto_display.grid(row=0, column=5, padx=5, sticky=tk.W)
        
        ttk.Label(calc_frame, text="Total:").grid(row=0, column=6, sticky=tk.W, padx=5)
        self.total_display = ttk.Label(calc_frame, textvariable=self.total_var, 
                                      font=("Helvetica", 12, "bold"), foreground="green")
        self.total_display.grid(row=0, column=7, padx=5, sticky=tk.W)
        
        # Estado
        ttk.Label(form_container, text="Estado:").grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        self.estado_combo = ttk.Combobox(form_container, textvariable=self.estado_var, 
                                        values=['Pendiente', 'Pagada', 'Cancelada', 'Vencida'], width=27, state="readonly")
        self.estado_combo.grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Observaciones
        ttk.Label(form_container, text="Observaciones:").grid(row=row, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(form_container, textvariable=self.observaciones_var, width=30).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Botones del formulario
        button_frame = ttk.Frame(form_container)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Guardar", command=self.guardar_factura).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", command=self.limpiar_formulario).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.cancelar_edicion).pack(side=tk.LEFT, padx=5)
    

    def on_cliente_selected(self, event=None):
        """Maneja la selección de cliente y filtra las ventas"""
        self.cargar_ventas_por_cliente()
    
    def on_venta_selected(self, event=None):
        """Maneja la selección de venta y carga automáticamente los datos"""
        if self.venta_var.get():
            try:
                venta_id = int(self.venta_var.get().split(' - ')[0])
                venta = self.venta_controller.obtener_venta(venta_id)
                if venta:
                    # Limpiar productos actuales
                    for item in self.productos_tree.get_children():
                        self.productos_tree.delete(item)
                    
                    # Cargar productos de la venta
                    detalles_venta = self.venta_controller.get_detalles_venta(venta_id)
                    for detalle in detalles_venta:
                        self.productos_tree.insert('', tk.END, values=(
                            detalle['producto'],
                            detalle['cantidad'],
                            format_currency(float(detalle['precio_uni'])),
                            format_currency(float(detalle['subtotal']))
                        ))
                    
                    # Actualizar totales automáticamente
                    self.actualizar_subtotal_automatico()
                    
                    # Auto-seleccionar empleado si existe
                    if venta.id_empleado:
                        self.empleado_var.set(str(venta.id_empleado))
            except (ValueError, IndexError, TypeError, AttributeError):
                pass
    
    def calcular_totales(self):
        """Calcula automáticamente impuesto y total basado en el subtotal actual"""
        try:
            # Obtener subtotal (limpiar cualquier formato previo)
            subtotal_str = str(self.subtotal_var.get()).replace('S/', '').replace('$', '').replace(',', '').strip()
            if not subtotal_str or subtotal_str == '':
                subtotal = 0.0
            else:
                subtotal = float(subtotal_str)
            
            # Calcular impuesto
            try:
                porcentaje = float(self.impuesto_porcentaje.get())
            except (ValueError, TypeError):
                porcentaje = 18.0  # Valor por defecto
                
            impuesto = subtotal * (porcentaje / 100)
            
            # Calcular total
            total = subtotal + impuesto
            
            # Actualizar variables con formato (sin cambiar el subtotal)
            self.impuesto_var.set(format_currency(impuesto))
            self.total_var.set(format_currency(total))
            
        except (ValueError, TypeError) as e:
            # En caso de error, establecer valores por defecto
            self.impuesto_var.set('S/ 0.00')
            self.total_var.set('S/ 0.00')
    

    
    def cargar_datos(self):
        """Carga los datos iniciales"""
        self.cargar_facturas()
        self.cargar_combos()
        
        # Establecer fecha actual
        self.fecha_factura.set(datetime.date.today().isoformat())
        self.estado_var.set('Pendiente')
        
        # Inicializar cálculos
        self.calcular_totales()
    
    def cargar_combos(self):
        """Carga los datos de los comboboxes"""
        # Cargar clientes
        clientes = self.cliente_controller.listar_clientes()
        cliente_values = [f"{c.id} - {c.nombre}" for c in clientes]
        self.cliente_combo['values'] = cliente_values
        
        # Cargar empleados (para uso interno)
        self.empleados = self.empleado_controller.listar_empleados()
        
        # Cargar productos
        productos = self.producto_controller.listar_productos()
        producto_values = [f"{p.id} - {p.nombre} - {format_currency(p.precio)}" for p in productos]
        self.producto_combo['values'] = producto_values
        
        # Establecer placeholder para productos
        if not self.producto_var.get():
            self.producto_combo.set("Seleccionar producto...")
        
        # Cargar todas las ventas inicialmente
        self.cargar_ventas_por_cliente()
    
    def cargar_ventas_por_cliente(self):
        """Carga las ventas filtradas por el cliente seleccionado"""
        if self.cliente_var.get():
            # Obtener ID del cliente seleccionado
            try:
                id_cliente = int(self.cliente_var.get().split(' - ')[0])
                # Obtener ventas del cliente específico
                ventas = self.venta_controller.buscar_ventas_por_cliente(id_cliente)
            except (ValueError, IndexError):
                # Si hay error, cargar todas las ventas
                ventas = self.venta_controller.listar_ventas()
        else:
            # Si no hay cliente seleccionado, cargar todas las ventas
            ventas = self.venta_controller.listar_ventas()
        
        # Actualizar el combobox de ventas
        venta_values = [f"{v.id} - {v.fecha} - {format_currency(v.total)}" for v in ventas]
        self.venta_combo['values'] = venta_values
        
        # Limpiar selección de venta si había una
        self.venta_var.set('')
    
    def cargar_facturas(self):
        """Carga las facturas en el treeview"""
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener facturas
        facturas = self.factura_controller.generar_reporte_facturas()
        
        # Insertar facturas en el treeview
        for factura in facturas:
            self.tree.insert('', tk.END, values=(
                factura['id'],
                factura['numero'],
                factura['fecha'],
                factura['cliente'] or 'N/A',
                format_currency(factura['total']),
                factura['estado']
            ))
    
    def agregar_producto(self):
        """Agrega un producto a la lista de productos de la factura"""
        if not self.producto_var.get() or self.producto_var.get() == "Seleccionar producto...":
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto")
            return
            
        try:
            # Obtener datos del producto
            producto_id = int(self.producto_var.get().split(' - ')[0])
            cantidad = int(self.cantidad_var.get())
            
            if cantidad <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a 0")
                return
            
            # Obtener producto completo
            producto = self.producto_controller.obtener_producto(producto_id)
            if not producto:
                messagebox.showerror("Error", "Producto no encontrado")
                return
            
            # Calcular subtotal
            precio_unitario = float(producto.precio)
            subtotal = cantidad * precio_unitario
            
            # Verificar si el producto ya está en la lista
            for item in self.productos_tree.get_children():
                values = self.productos_tree.item(item, 'values')
                if values[0] == producto.nombre:
                    # Actualizar cantidad existente
                    nueva_cantidad = int(values[1]) + cantidad
                    nuevo_subtotal = nueva_cantidad * precio_unitario
                    self.productos_tree.item(item, values=(
                        producto.nombre,
                        nueva_cantidad,
                        format_currency(precio_unitario),
                        format_currency(nuevo_subtotal)
                    ))
                    self.actualizar_subtotal_automatico()
                    return
            
            # Agregar nuevo producto a la lista
            self.productos_tree.insert('', tk.END, values=(
                producto.nombre,
                cantidad,
                format_currency(precio_unitario),
                format_currency(subtotal)
            ))
            
            # Actualizar subtotal automáticamente
            self.actualizar_subtotal_automatico()
            
            # Limpiar selección
            self.producto_var.set('')
            self.producto_combo.set("Seleccionar producto...")
            self.cantidad_var.set('1')
            
        except (ValueError, IndexError) as e:
            messagebox.showerror("Error", f"Error al agregar producto: {str(e)}")
    
    def eliminar_producto(self):
        """Elimina el producto seleccionado de la lista"""
        selected_item = self.productos_tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Debe seleccionar un producto para eliminar")
            return
        
        # Eliminar producto
        self.productos_tree.delete(selected_item[0])
        
        # Actualizar subtotal automáticamente
        self.actualizar_subtotal_automatico()
    
    def actualizar_subtotal_automatico(self):
        """Calcula automáticamente el subtotal basado en los productos agregados"""
        total_subtotal = 0.0
        
        # Sumar todos los subtotales de productos
        for item in self.productos_tree.get_children():
            values = self.productos_tree.item(item, 'values')
            subtotal_str = values[3].replace('S/', '').replace('$', '').replace(',', '')
            total_subtotal += float(subtotal_str)
        
        # Actualizar el subtotal y recalcular totales
        self.subtotal_var.set(format_currency(total_subtotal))
        self.calcular_totales()
    
    def cargar_productos_factura(self, factura_id):
        """Carga los productos existentes de una factura para edición"""
        try:
            # Limpiar lista actual
            for item in self.productos_tree.get_children():
                self.productos_tree.delete(item)
            
            # Obtener detalles de la factura
            detalles = self.factura_controller.obtener_detalles_factura(factura_id)
            
            for detalle in detalles:
                # Obtener información del producto
                producto = self.producto_controller.obtener_producto(detalle.id_producto)
                if producto:
                    self.productos_tree.insert('', tk.END, values=(
                        producto.nombre,
                        detalle.cantidad,
                        format_currency(float(detalle.precio_unitario)),
                        format_currency(float(detalle.subtotal))
                    ))
        
        except Exception as e:
            print(f"Error al cargar productos de factura: {str(e)}")
    
    def filtrar_facturas(self, event=None):
        """Filtra las facturas por estado"""
        estado = self.estado_filter.get()
        
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener facturas filtradas
        if estado == 'Todos':
            facturas = self.factura_controller.generar_reporte_facturas()
        else:
            facturas = self.factura_controller.generar_reporte_facturas(estado=estado)
        
        # Insertar facturas filtradas
        for factura in facturas:
            self.tree.insert('', tk.END, values=(
                factura['id'],
                factura['numero'],
                factura['fecha'],
                factura['cliente'] or 'N/A',
                format_currency(factura['total']),
                factura['estado']
            ))
    
    def nueva_factura(self):
        """Prepara el formulario para una nueva factura"""
        self.limpiar_formulario()
        self.generar_numero()
        self.notebook.select(1)  # Cambiar a la pestaña del formulario
    
    def editar_factura(self):
        """Edita la factura seleccionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una factura para editar")
            return
        
        item = self.tree.item(selection[0])
        factura_id = item['values'][0]
        
        # Obtener la factura
        factura = self.factura_controller.obtener_factura(factura_id)
        if not factura:
            messagebox.showerror("Error", "No se pudo cargar la factura")
            return
        
        # Cargar datos en el formulario
        self.factura_id.set(str(factura.id))
        self.factura_actual_id = factura.id
        self.numero_factura.set(factura.numero_factura)
        self.fecha_factura.set(factura.fecha)
        # Cargar valores numéricos con formato de moneda
        self.subtotal_var.set(format_currency(float(factura.subtotal) if factura.subtotal else 0.0))
        self.impuesto_var.set(format_currency(float(factura.impuesto) if factura.impuesto else 0.0))
        self.total_var.set(format_currency(float(factura.total) if factura.total else 0.0))
        self.estado_var.set(factura.estado)
        self.observaciones_var.set(factura.observaciones or '')
        
        # Seleccionar cliente y venta si existen
        if factura.id_cliente:
            for value in self.cliente_combo['values']:
                if value.startswith(f"{factura.id_cliente} - "):
                    self.cliente_var.set(value)
                    break
        if factura.id_empleado:
            self.empleado_var.set(str(factura.id_empleado))
        if factura.id_venta:
            for value in self.venta_combo['values']:
                if value.startswith(f"{factura.id_venta} - "):
                    self.venta_var.set(value)
                    break
        
        # Cargar productos de la factura
        self.cargar_productos_factura(factura.id)
        
        self.notebook.select(1)  # Cambiar a la pestaña del formulario
    
    def eliminar_factura(self):
        """Elimina la factura seleccionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una factura para eliminar")
            return
        
        item = self.tree.item(selection[0])
        factura_id = item['values'][0]
        numero = item['values'][1]
        
        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la factura {numero}?"):
            if self.factura_controller.eliminar_factura(factura_id):
                messagebox.showinfo("Éxito", "Factura eliminada correctamente")
                self.cargar_facturas()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la factura")
    
    def guardar_factura(self):
        """Guarda la factura (nueva o editada)"""
        try:
            # Validar campos requeridos
            if not self.numero_factura.get():
                messagebox.showerror("Error", "Debe generar un número de factura")
                return
            
            if not self.cliente_var.get():
                messagebox.showerror("Error", "Debe seleccionar un cliente")
                return
            
            # Verificar que hay productos o subtotal
            productos_count = len(self.productos_tree.get_children())
            subtotal_str = str(self.subtotal_var.get()).replace('S/', '').replace('$', '').replace(',', '').strip()
            subtotal_value = float(subtotal_str) if subtotal_str and subtotal_str != '' else 0.0
            
            if productos_count == 0 and subtotal_value == 0.0:
                messagebox.showerror("Error", "Debe agregar productos o seleccionar una venta")
                return
            
            # Auto-seleccionar empleado (primer empleado disponible)
            if not self.empleado_var.get():
                if self.empleados:
                    self.empleado_var.set(str(self.empleados[0].id))
                else:
                    messagebox.showerror("Error", "No hay empleados disponibles")
                    return
            
            # Extraer IDs de los comboboxes
            id_cliente = int(self.cliente_var.get().split(' - ')[0])
            id_empleado = int(self.empleado_var.get())
            
            id_venta = None
            if self.venta_var.get():
                id_venta = int(self.venta_var.get().split(' - ')[0])
            
            # Extraer valores numéricos
            impuesto_text = str(self.impuesto_var.get()).replace('S/', '').replace('$', '').replace(',', '').strip()
            total_text = str(self.total_var.get()).replace('S/', '').replace('$', '').replace(',', '').strip()
            
            subtotal = subtotal_value
            impuesto = float(impuesto_text) if impuesto_text else 0.0
            total = float(total_text) if total_text else 0.0
            
            # Preparar lista de productos
            productos_lista = []
            for item in self.productos_tree.get_children():
                values = self.productos_tree.item(item, 'values')
                # Buscar el ID del producto por nombre
                producto_nombre = values[0]
                producto_id = None
                for value in self.producto_combo['values']:
                    if producto_nombre in value:
                        producto_id = int(value.split(' - ')[0])
                        break
                
                if producto_id:
                    cantidad = int(values[1])
                    precio_str = values[2].replace('S/', '').replace('$', '').replace(',', '').strip()
                    precio_unitario = float(precio_str)
                    productos_lista.append({
                        'id_producto': producto_id,
                        'cantidad': cantidad,
                        'precio_unitario': precio_unitario
                    })
            
            # Determinar si es nueva o edición
            if self.factura_id.get():
                # Editar factura existente
                result = self.factura_controller.actualizar_factura(
                    id_factura=int(self.factura_id.get()),
                    numero_factura=self.numero_factura.get(),
                    subtotal=subtotal,
                    impuesto=impuesto,
                    total=total,
                    estado=self.estado_var.get(),
                    observaciones=self.observaciones_var.get(),
                    id_venta=id_venta,
                    id_cliente=id_cliente,
                    id_empleado=id_empleado
                )
                
                # Actualizar productos si hay
                if productos_lista and result:
                    factura_id = int(self.factura_id.get())
                    # Eliminar productos existentes
                    try:
                        detalles_existentes = self.factura_controller.obtener_detalles_factura(factura_id)
                        for detalle in detalles_existentes:
                            self.factura_controller.eliminar_producto_factura(factura_id, detalle.id)
                    except:
                        pass  # Si no hay detalles existentes, continuar
                    
                    # Agregar nuevos productos
                    for producto in productos_lista:
                        self.factura_controller.agregar_producto_factura(
                            factura_id, producto['id_producto'], 
                            producto['cantidad'], producto['precio_unitario']
                        )
                
                mensaje = "Factura actualizada correctamente"
            else:
                # Crear nueva factura
                if productos_lista:
                    # Crear factura con productos
                    result = self.factura_controller.crear_factura_con_productos(
                        numero_factura=self.numero_factura.get(),
                        productos_data=productos_lista,
                        impuesto_porcentaje=self.impuesto_porcentaje.get(),
                        estado=self.estado_var.get(),
                        observaciones=self.observaciones_var.get(),
                        id_cliente=id_cliente,
                        id_empleado=id_empleado
                    )
                else:
                    # Crear factura tradicional
                    result = self.factura_controller.crear_factura(
                        numero_factura=self.numero_factura.get(),
                        subtotal=subtotal,
                        impuesto=impuesto,
                        total=total,
                        estado=self.estado_var.get(),
                        observaciones=self.observaciones_var.get(),
                        id_venta=id_venta,
                        id_cliente=id_cliente,
                        id_empleado=id_empleado
                    )
                mensaje = "Factura creada correctamente"
            
            if result:
                messagebox.showinfo("Éxito", mensaje)
                self.limpiar_formulario()
                self.cargar_facturas()
                self.notebook.select(0)  # Volver a la lista
            else:
                messagebox.showerror("Error", "No se pudo guardar la factura")
        
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos numéricos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def generar_numero(self):
        """Genera un número de factura automático"""
        numero = self.factura_controller.generar_numero_factura()
        self.numero_factura.set(numero)
    
    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.factura_actual = None
        self.venta_seleccionada = None
        self.factura_actual_id = None
        self.productos_factura = []
        self.factura_id.set('')
        self.numero_factura.set('')
        self.fecha_factura.set(datetime.date.today().isoformat())
        self.cliente_var.set('')
        self.empleado_var.set('')
        self.venta_var.set('')
        self.subtotal_var.set('S/ 0.00')
        self.impuesto_porcentaje.set(18.0)
        self.impuesto_var.set('S/ 0.00')
        self.total_var.set('S/ 0.00')
        self.estado_var.set('Pendiente')
        self.observaciones_var.set('')
        
        # Limpiar lista de productos
        for item in self.productos_tree.get_children():
            self.productos_tree.delete(item)
        
        # Restablecer selección de producto
        self.producto_var.set('')
        self.producto_combo.set("Seleccionar producto...")
        self.cantidad_var.set('1')
    
    def cancelar_edicion(self):
        """Cancela la edición y vuelve a la lista"""
        self.limpiar_formulario()
        self.notebook.select(0)
    

    
    def exportar_factura_pdf(self):
        """Exporta la factura seleccionada a PDF"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una factura para exportar")
            return
        
        item = self.tree.item(selection[0])
        factura_id = item['values'][0]
        
        archivo = self.factura_controller.exportar_factura_pdf(factura_id)
        
        if archivo:
            messagebox.showinfo("Éxito", f"Factura PDF exportada a: {archivo}")
        else:
            messagebox.showerror("Error", "No se pudo exportar la factura")
    
    def exportar_factura_excel(self):
        """Exporta la factura seleccionada a Excel"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una factura para exportar")
            return
        
        item = self.tree.item(selection[0])
        factura_id = item['values'][0]
        
        archivo = self.factura_controller.exportar_factura_excel(factura_id)
        
        if archivo:
            messagebox.showinfo("Éxito", f"Factura Excel exportada a: {archivo}")
        else:
            messagebox.showerror("Error", "No se pudo exportar la factura")