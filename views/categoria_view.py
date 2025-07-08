import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from controllers.categoria_controller import CategoriaController
from utils.validators import validate_required

class CategoriaView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = CategoriaController()
        
        # Variables para los campos del formulario
        self.var_id = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_descripcion = tk.StringVar()
        self.var_search = tk.StringVar()
        
        # Crear la interfaz
        self.create_widgets()
        
        # Cargar datos iniciales
        self.load_categorias()
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame izquierdo (formulario)
        form_frame = ttk.LabelFrame(main_frame, text="Datos de Categoría", padding=10)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Campos del formulario
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_id, state="readonly", width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_nombre, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Descripción:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_descripcion, width=30).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Botones de acción
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Nuevo", command=self.new_categoria, bootstyle=SUCCESS).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Guardar", command=self.save_categoria).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_categoria, bootstyle=DANGER).grid(row=0, column=2, padx=5)
        
        # Frame derecho (tabla)
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Categorías", padding=10)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Barra de búsqueda
        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(search_frame, textvariable=self.var_search, width=30).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(search_frame, text="Buscar", command=self.search_categorias).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Mostrar Todos", command=self.load_categorias).pack(side=tk.LEFT, padx=5)
        
        # Tabla de categorías
        self.tree = ttk.Treeview(table_frame, columns=("id", "nombre", "descripcion"), show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("descripcion", text="Descripción")
        
        self.tree.column("id", width=50)
        self.tree.column("nombre", width=150)
        self.tree.column("descripcion", width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.on_select_categoria)
    
    def load_categorias(self):
        """Carga todas las categorías en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener categorías
        categorias = self.controller.get_all_categorias()
        
        # Insertar en la tabla
        for categoria in categorias:
            self.tree.insert("", tk.END, values=(categoria.id, categoria.nombre, categoria.descripcion))
    
    def search_categorias(self):
        """Busca categorías según el término de búsqueda"""
        search_term = self.var_search.get()
        if not search_term:
            self.load_categorias()
            return
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar categorías
        categorias = self.controller.search_categorias(search_term)
        
        # Insertar en la tabla
        for categoria in categorias:
            self.tree.insert("", tk.END, values=(categoria.id, categoria.nombre, categoria.descripcion))
    
    def on_select_categoria(self, event):
        """Maneja el evento de selección en la tabla"""
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            values = item["values"]
            
            # Actualizar variables
            self.var_id.set(values[0])
            self.var_nombre.set(values[1])
            self.var_descripcion.set(values[2])
    
    def new_categoria(self):
        """Limpia el formulario para una nueva categoría"""
        self.var_id.set("")
        self.var_nombre.set("")
        self.var_descripcion.set("")
    
    def save_categoria(self):
        """Guarda o actualiza una categoría"""
        nombre = self.var_nombre.get()
        descripcion = self.var_descripcion.get()
        
        # Validar campos
        if not validate_required(nombre):
            messagebox.showerror("Error", "El nombre de la categoría es obligatorio")
            return
        
        # Guardar o actualizar
        id_categoria = self.var_id.get()
        if id_categoria:
            # Actualizar
            result = self.controller.update_categoria(int(id_categoria), nombre, descripcion)
            if result:
                messagebox.showinfo("Éxito", "Categoría actualizada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo actualizar la categoría")
        else:
            # Crear nueva
            result = self.controller.create_categoria(nombre, descripcion)
            if result:
                messagebox.showinfo("Éxito", "Categoría creada correctamente")
            else:
                messagebox.showerror("Error", "No se pudo crear la categoría")
        
        # Recargar datos
        self.load_categorias()
        self.new_categoria()
    
    def delete_categoria(self):
        """Elimina una categoría"""
        id_categoria = self.var_id.get()
        if not id_categoria:
            messagebox.showerror("Error", "Debe seleccionar una categoría para eliminar")
            return
        
        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta categoría?\nEsta acción no se puede deshacer."):
            result = self.controller.delete_categoria(int(id_categoria))
            if result:
                messagebox.showinfo("Éxito", "Categoría eliminada correctamente")
                self.load_categorias()
                self.new_categoria()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la categoría")