import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import datetime

from controllers.venta_controller import VentaController
from controllers.producto_controller import ProductoController
from controllers.cliente_controller import ClienteController
from controllers.empleado_controller import EmpleadoController
from utils.validators import validate_required, validate_integer
from utils.helpers import format_currency, format_date, calculate_subtotal

class VentaView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = VentaController()
        self.producto_controller = ProductoController()
        self.cliente_controller = ClienteController()
        self.empleado_controller = EmpleadoController()
        
        # Variables para los campos del formulario
        self.var_cliente = tk.StringVar()
        self.var_empleado = tk.StringVar()
        self.var_fecha = tk.StringVar(value=datetime.date.today().strftime("%Y-%m-%d"))
        self.var_total = tk.StringVar(value="0.00")
        
        # Variables para el detalle
        self.var_producto = tk.StringVar()
        self.var_cantidad = tk.StringVar(value="1")
        self.var_precio = tk.StringVar(value="0.00")
        self.var_subtotal = tk.StringVar(value="0.00")
        
        # Lista de detalles de la venta
        self.detalles = []
        
        # Crear la interfaz
        self.create_widgets()
        
        # Cargar datos iniciales
        self.load_combos()
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame superior (datos de la venta)
        top_frame = ttk.LabelFrame(main_frame, text="Datos de la Venta", padding=10)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Grid para los campos
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(3, weight=1)
        
        # Fecha
        ttk.Label(top_frame, text="Fecha:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(top_frame, textvariable=self.var_fecha, state="readonly", width=15).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Cliente
        ttk.Label(top_frame, text="Cliente:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.combo_clientes = ttk.Combobox(top_frame, textvariable=self.var_cliente, width=30)
        self.combo_clientes.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Empleado
        ttk.Label(top_frame, text="Empleado:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_empleados = ttk.Combobox(top_frame, textvariable=self.var_empleado, width=30)
        self.combo_empleados.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Total
        ttk.Label(top_frame, text="Total:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(top_frame, textvariable=self.var_total, state="readonly", width=15).grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Frame medio (agregar productos)
        mid_frame = ttk.LabelFrame(main_frame, text="Agregar Producto", padding=10)
        mid_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Producto
        ttk.Label(mid_frame, text="Producto:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.combo_productos = ttk.Combobox(mid_frame, textvariable=self.var_producto, width=40)
        self.combo_productos.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.combo_productos.bind("<<ComboboxSelected>>", self.on_producto_selected)
        
        # Cantidad
        ttk.Label(mid_frame, text="Cantidad:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(mid_frame, textvariable=self.var_cantidad, width=10).grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        self.var_cantidad.trace_add("write", self.calculate_subtotal)
        
        # Precio
        ttk.Label(mid_frame, text="Precio:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(mid_frame, textvariable=self.var_precio, state="readonly", width=15).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Subtotal
        ttk.Label(mid_frame, text="Subtotal:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(mid_frame, textvariable=self.var_subtotal, state="readonly", width=15).grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Botón agregar
        ttk.Button(mid_frame, text="Agregar Producto", command=self.agregar_producto, bootstyle=SUCCESS).grid(row=1, column=4, padx=5, pady=5)
        
        # Frame inferior (tabla de productos)
        bottom_frame = ttk.LabelFrame(main_frame, text="Detalle de Venta", padding=10)
        bottom_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tabla de productos
        columns = ("id", "producto", "cantidad", "precio", "subtotal")
        self.tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Configurar columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("producto", text="Producto")
        self.tree.heading("cantidad", text="Cantidad")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("subtotal", text="Subtotal")
        
        self.tree.column("id", width=50)
        self.tree.column("producto", width=300)
        self.tree.column("cantidad", width=100)
        self.tree.column("precio", width=100)
        self.tree.column("subtotal", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(bottom_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Eliminar Producto", command=self.eliminar_producto, bootstyle=DANGER).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar Venta", command=self.limpiar_venta).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Registrar Venta", command=self.registrar_venta, bootstyle=SUCCESS).pack(side=tk.RIGHT, padx=5)
    
    def load_combos(self):
        """Carga los datos en los combobox"""
        # Cargar clientes
        clientes = self.cliente_controller.get_all_clientes()
        self.clientes_data = {f"{c.id}: {c.nombre}": c.id for c in clientes}
        self.combo_clientes['values'] = list(self.clientes_data.keys())
        
        # Cargar empleados
        empleados = self.empleado_controller.get_all_empleados()
        self.empleados_data = {f"{e.id}: {e.nombre}": e.id for e in empleados}
        self.combo_empleados['values'] = list(self.empleados_data.keys())
        
        # Cargar productos
        productos = self.producto_controller.get_all_productos()
        self.productos_data = {f"{p.id}: {p.nombre} - {format_currency(p.precio)}": {
            'id': p.id,
            'nombre': p.nombre,
            'precio': p.precio,
            'stock': p.stock
        } for p in productos}
        self.combo_productos['values'] = list(self.productos_data.keys())
    
    def on_producto_selected(self, event):
        """Maneja el evento de selección de producto"""
        producto_key = self.var_producto.get()
        if producto_key in self.productos_data:
            producto = self.productos_data[producto_key]
            self.var_precio.set(format_currency(producto['precio']).replace("S/", "").strip())
            self.calculate_subtotal()
    
    def calculate_subtotal(self, *args):
        """Calcula el subtotal del producto"""
        try:
            precio_str = self.var_precio.get().replace(",", ".")
            # Limpiar caracteres no numéricos excepto el punto decimal
            import re
            precio_limpio = re.sub(r'[^\d.]', '', precio_str)
            if not precio_limpio:
                precio_limpio = "0"
            precio = float(precio_limpio)
            cantidad = int(self.var_cantidad.get())
            subtotal = precio * cantidad
            self.var_subtotal.set(f"{subtotal:.2f}")
        except (ValueError, AttributeError):
            self.var_subtotal.set("0.00")
    
    def agregar_producto(self):
        """Agrega un producto al detalle de la venta"""
        producto_key = self.var_producto.get()
        cantidad_str = self.var_cantidad.get()
        
        # Validar campos
        if not producto_key:
            messagebox.showerror("Error", "Debe seleccionar un producto")
            return
        
        if not validate_integer(cantidad_str, min_value=1):
            messagebox.showerror("Error", "La cantidad debe ser un número entero mayor a 0")
            return
        
        # Obtener datos del producto
        if producto_key not in self.productos_data:
            messagebox.showerror("Error", "Producto no válido")
            return
        
        producto = self.productos_data[producto_key]
        cantidad = int(cantidad_str)
        
        # Verificar stock
        if cantidad > producto['stock']:
            messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto['stock']}")
            return
        
        # Calcular subtotal
        precio_str = self.var_precio.get()
        # Limpiar la cadena de precio para eliminar caracteres no numéricos (excepto el punto decimal)
        import re
        precio_limpio = re.sub(r'[^\d.]', '', precio_str.replace(",", "."))
        try:
            precio = float(precio_limpio)
        except ValueError:
            messagebox.showerror("Error", f"Formato de precio no válido: {precio_str}")
            return
            
        subtotal = precio * cantidad
        
        # Agregar a la lista de detalles
        detalle = {
            'id_producto': producto['id'],
            'producto': producto['nombre'],
            'cantidad': cantidad,
            'precio_uni': precio,
            'subtotal': subtotal
        }
        
        # Verificar si el producto ya está en la lista
        for i, d in enumerate(self.detalles):
            if d['id_producto'] == detalle['id_producto']:
                # Actualizar cantidad y subtotal
                nueva_cantidad = d['cantidad'] + cantidad
                if nueva_cantidad > producto['stock']:
                    messagebox.showerror("Error", f"Stock insuficiente. Disponible: {producto['stock']}")
                    return
                
                self.detalles[i]['cantidad'] = nueva_cantidad
                self.detalles[i]['subtotal'] = nueva_cantidad * precio
                self.actualizar_tabla()
                self.actualizar_total()
                return
        
        # Agregar nuevo detalle
        self.detalles.append(detalle)
        
        # Actualizar tabla y total
        self.actualizar_tabla()
        self.actualizar_total()
        
        # Limpiar campos
        self.var_producto.set("")
        self.var_cantidad.set("1")
        self.var_precio.set("0.00")
        self.var_subtotal.set("0.00")
    
    def actualizar_tabla(self):
        """Actualiza la tabla de detalles"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar detalles
        for detalle in self.detalles:
            self.tree.insert("", tk.END, values=(
                detalle['id_producto'],
                detalle['producto'],
                detalle['cantidad'],
                format_currency(detalle['precio_uni']),
                format_currency(detalle['subtotal'])
            ))
    
    def actualizar_total(self):
        """Actualiza el total de la venta"""
        total = sum(detalle['subtotal'] for detalle in self.detalles)
        self.var_total.set(f"{total:.2f}")
    
    def eliminar_producto(self):
        """Elimina un producto del detalle de la venta"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debe seleccionar un producto para eliminar")
            return
        
        item = self.tree.item(selected_item[0])
        values = item["values"]
        id_producto = values[0]
        
        # Eliminar de la lista de detalles
        self.detalles = [d for d in self.detalles if d['id_producto'] != id_producto]
        
        # Actualizar tabla y total
        self.actualizar_tabla()
        self.actualizar_total()
    
    def limpiar_venta(self):
        """Limpia todos los campos de la venta"""
        self.var_cliente.set("")
        self.var_empleado.set("")
        self.var_producto.set("")
        self.var_cantidad.set("1")
        self.var_precio.set("0.00")
        self.var_subtotal.set("0.00")
        self.var_total.set("0.00")
        self.detalles = []
        self.actualizar_tabla()
    
    def registrar_venta(self):
        """Registra la venta en la base de datos"""
        cliente_key = self.var_cliente.get()
        empleado_key = self.var_empleado.get()
        
        # Validar campos
        if not cliente_key:
            messagebox.showerror("Error", "Debe seleccionar un cliente")
            return
        
        if not empleado_key:
            messagebox.showerror("Error", "Debe seleccionar un empleado")
            return
        
        if not self.detalles:
            messagebox.showerror("Error", "Debe agregar al menos un producto")
            return
        
        # Obtener IDs
        id_cliente = self.clientes_data.get(cliente_key)
        id_empleado = self.empleados_data.get(empleado_key)
        
        if not id_cliente or not id_empleado:
            messagebox.showerror("Error", "Cliente o empleado no válido")
            return
        
        # Registrar venta
        id_venta = self.controller.crear_venta(id_cliente, id_empleado, self.detalles)
        
        if id_venta:
            messagebox.showinfo("Éxito", f"Venta registrada correctamente con ID: {id_venta}")
            self.limpiar_venta()
            # Recargar productos (para actualizar stock)
            self.load_combos()
        else:
            messagebox.showerror("Error", "No se pudo registrar la venta")