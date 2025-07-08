import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from controllers.producto_controller import ProductoController
from controllers.categoria_controller import CategoriaController
from utils.validators import validate_required, validate_number, validate_integer
from utils.helpers import format_currency

class ProductoView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ProductoController()
        self.categoria_controller = CategoriaController()
        
        # Variables para los campos del formulario
        self.var_id = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_stock = tk.StringVar()
        self.var_categoria = tk.StringVar()
        self.var_search = tk.StringVar()
        
        # Crear la interfaz
        self.create_widgets()
        
        # Cargar datos iniciales
        self.load_productos()
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame izquierdo (formulario)
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Producto", padding=10)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Campos del formulario
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_id, state="readonly", width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_nombre, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Precio:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_precio, width=15).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Stock:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_stock, width=10).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Categoría:").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        # Combobox para categorías
        self.combo_categorias = ttk.Combobox(form_frame, textvariable=self.var_categoria, width=25)
        self.combo_categorias.grid(row=4, column=1, sticky=tk.W, pady=5)
        self.load_categorias_combo()
        
        # Botones de acción
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Nuevo", command=self.new_producto, bootstyle=SUCCESS).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Guardar", command=self.save_producto).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_producto, bootstyle=DANGER).grid(row=0, column=2, padx=5)
        
        # Frame derecho (tabla)
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Productos", padding=10)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Barra de búsqueda
        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(search_frame, textvariable=self.var_search, width=30).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(search_frame, text="Buscar", command=self.search_productos).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Mostrar Todos", command=self.load_productos).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Stock Bajo", command=self.show_stock_bajo, bootstyle=WARNING).pack(side=tk.LEFT, padx=5)
        
        # Tabla de productos
        columns = ("id", "nombre", "precio", "stock", "categoria")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("precio", text="Precio")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("categoria", text="Categoría")
        
        self.tree.column("id", width=50)
        self.tree.column("nombre", width=200)
        self.tree.column("precio", width=100)
        self.tree.column("stock", width=80)
        self.tree.column("categoria", width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.on_select_producto)
    
    def load_categorias_combo(self):
        """Carga las categorías en el combobox"""
        categorias = self.categoria_controller.get_all_categorias()
        self.categorias_data = {f"{c.id}: {c.nombre}": c.id for c in categorias}
        self.combo_categorias['values'] = list(self.categorias_data.keys())
    
    def load_productos(self):
        """Carga todos los productos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener productos
        productos = self.controller.get_all_productos()
        
        # Insertar en la tabla
        for producto in productos:
            categoria_nombre = self.controller.get_categoria_nombre(producto.id_categoria)
            self.tree.insert("", tk.END, values=(
                producto.id, 
                producto.nombre, 
                format_currency(producto.precio), 
                producto.stock,
                categoria_nombre
            ))
    
    def search_productos(self):
        """Busca productos según el término de búsqueda"""
        search_term = self.var_search.get()
        if not search_term:
            self.load_productos()
            return
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar productos
        productos = self.controller.search_productos(search_term)
        
        # Insertar en la tabla
        for producto in productos:
            categoria_nombre = self.controller.get_categoria_nombre(producto.id_categoria)
            self.tree.insert("", tk.END, values=(
                producto.id, 
                producto.nombre, 
                format_currency(producto.precio), 
                producto.stock,
                categoria_nombre
            ))
    
    def show_stock_bajo(self):
        """Muestra productos con stock bajo"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener productos con stock bajo
        productos = self.controller.get_productos_stock_bajo()
        
        # Insertar en la tabla
        for producto in productos:
            categoria_nombre = self.controller.get_categoria_nombre(producto.id_categoria)
            self.tree.insert("", tk.END, values=(
                producto.id, 
                producto.nombre, 
                format_currency(producto.precio), 
                producto.stock,
                categoria_nombre
            ), tags=('stock_bajo',))
        
        # Configurar estilo para stock bajo
        self.tree.tag_configure('stock_bajo', background='#ffcccc')
    
    def on_select_producto(self, event):
        """Maneja el evento de selección en la tabla"""
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            values = item["values"]
            
            # Actualizar variables
            self.var_id.set(values[0])
            self.var_nombre.set(values[1])
            
            # Formatear precio (quitar símbolo de moneda)
            precio_str = values[2]
            if isinstance(precio_str, str):
                precio_str = precio_str.replace("S/", "").replace("$", "").strip()
            self.var_precio.set(precio_str)
            
            self.var_stock.set(values[3])
            
            # Buscar la categoría en el combobox
            categoria_nombre = values[4]
            for key, value in self.categorias_data.items():
                if f"{value}:" in key and categoria_nombre in key:
                    self.var_categoria.set(key)
                    break
    
    def new_producto(self):
        """Limpia el formulario para un nuevo producto"""
        self.var_id.set("")
        self.var_nombre.set("")
        self.var_precio.set("")
        self.var_stock.set("")
        self.var_categoria.set("")
    
    def save_producto(self):
        """Guarda o actualiza un producto"""
        nombre = self.var_nombre.get()
        precio = self.var_precio.get()
        stock = self.var_stock.get()
        categoria = self.var_categoria.get()
        
        # Validar campos
        if not validate_required(nombre):
            messagebox.showerror("Error", "El nombre del producto es obligatorio")
            return
        
        if not validate_number(precio, min_value=0):
            messagebox.showerror("Error", "El precio debe ser un número mayor o igual a 0")
            return
        
        if not validate_integer(stock, min_value=0):
            messagebox.showerror("Error", "El stock debe ser un número entero mayor o igual a 0")
            return
        
        if not categoria:
            messagebox.showerror("Error", "Debe seleccionar una categoría")
            return
        
        # Obtener ID de categoría
        id_categoria = self.categorias_data.get(categoria)
        if not id_categoria:
            messagebox.showerror("Error", "Categoría no válida")
            return
        
        # Guardar o actualizar
        id_producto = self.var_id.get()
        if id_producto:
            # Actualizar
            result = self.controller.update_producto(
                int(id_producto), nombre, float(precio), int(stock), id_categoria
            )
            if result:
                messagebox.showinfo("Éxito", "Producto actualizado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el producto")
        else:
            # Crear nuevo
            result = self.controller.create_producto(
                nombre, float(precio), int(stock), id_categoria
            )
            if result:
                messagebox.showinfo("Éxito", "Producto creado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo crear el producto")
        
        # Recargar datos
        self.load_productos()
        self.new_producto()
    
    def delete_producto(self):
        """Elimina un producto"""
        id_producto = self.var_id.get()
        if not id_producto:
            messagebox.showerror("Error", "Debe seleccionar un producto para eliminar")
            return
        
        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?\nEsta acción no se puede deshacer."):
            result = self.controller.delete_producto(int(id_producto))
            if result:
                messagebox.showinfo("Éxito", "Producto eliminado correctamente")
                self.load_productos()
                self.new_producto()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto")