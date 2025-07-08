import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from controllers.cliente_controller import ClienteController
from utils.validators import validate_required, validate_dni, validate_phone

class ClienteView:
    def __init__(self, parent):
        self.parent = parent
        self.controller = ClienteController()
        
        # Variables para los campos del formulario
        self.var_id = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_telefono = tk.StringVar()
        self.var_dni = tk.StringVar()
        self.var_direccion = tk.StringVar()
        self.var_search = tk.StringVar()
        
        # Crear la interfaz
        self.create_widgets()
        
        # Cargar datos iniciales
        self.load_clientes()
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame izquierdo (formulario)
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Cliente", padding=10)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        # Campos del formulario
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_id, state="readonly", width=10).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_nombre, width=30).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Teléfono:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_telefono, width=15).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="DNI:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_dni, width=15).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(form_frame, text="Dirección:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.var_direccion, width=30).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Botones de acción
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Nuevo", command=self.new_cliente, bootstyle=SUCCESS).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Guardar", command=self.save_cliente).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.delete_cliente, bootstyle=DANGER).grid(row=0, column=2, padx=5)
        
        # Frame derecho (tabla)
        table_frame = ttk.LabelFrame(main_frame, text="Lista de Clientes", padding=10)
        table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Barra de búsqueda
        search_frame = ttk.Frame(table_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(search_frame, textvariable=self.var_search, width=30).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(search_frame, text="Buscar", command=self.search_clientes).pack(side=tk.LEFT)
        ttk.Button(search_frame, text="Mostrar Todos", command=self.load_clientes).pack(side=tk.LEFT, padx=5)
        
        # Tabla de clientes
        columns = ("id", "nombre", "telefono", "dni", "direccion")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("telefono", text="Teléfono")
        self.tree.heading("dni", text="DNI")
        self.tree.heading("direccion", text="Dirección")
        
        self.tree.column("id", width=50)
        self.tree.column("nombre", width=200)
        self.tree.column("telefono", width=100)
        self.tree.column("dni", width=100)
        self.tree.column("direccion", width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Evento de selección
        self.tree.bind("<<TreeviewSelect>>", self.on_select_cliente)
    
    def load_clientes(self):
        """Carga todos los clientes en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener clientes
        clientes = self.controller.get_all_clientes()
        
        # Insertar en la tabla
        for cliente in clientes:
            self.tree.insert("", tk.END, values=(
                cliente.id, 
                cliente.nombre, 
                cliente.telefono, 
                cliente.dni,
                cliente.direccion
            ))
    
    def search_clientes(self):
        """Busca clientes según el término de búsqueda"""
        search_term = self.var_search.get()
        if not search_term:
            self.load_clientes()
            return
        
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Buscar clientes
        clientes = self.controller.search_clientes(search_term)
        
        # Insertar en la tabla
        for cliente in clientes:
            self.tree.insert("", tk.END, values=(
                cliente.id, 
                cliente.nombre, 
                cliente.telefono, 
                cliente.dni,
                cliente.direccion
            ))
    
    def on_select_cliente(self, event):
        """Maneja el evento de selección en la tabla"""
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            values = item["values"]
            
            # Actualizar variables
            self.var_id.set(values[0])
            self.var_nombre.set(values[1])
            self.var_telefono.set(values[2])
            self.var_dni.set(values[3])
            self.var_direccion.set(values[4])
    
    def new_cliente(self):
        """Limpia el formulario para un nuevo cliente"""
        self.var_id.set("")
        self.var_nombre.set("")
        self.var_telefono.set("")
        self.var_dni.set("")
        self.var_direccion.set("")
    
    def save_cliente(self):
        """Guarda o actualiza un cliente"""
        nombre = self.var_nombre.get()
        telefono = self.var_telefono.get()
        dni = self.var_dni.get()
        direccion = self.var_direccion.get()
        
        # Validar campos
        if not validate_required(nombre):
            messagebox.showerror("Error", "El nombre del cliente es obligatorio")
            return
        
        if telefono and not validate_phone(telefono):
            messagebox.showerror("Error", "El teléfono debe tener 9 dígitos")
            return
        
        if dni and not validate_dni(dni):
            messagebox.showerror("Error", "El DNI debe tener 8 dígitos")
            return
        
        # Guardar o actualizar
        id_cliente = self.var_id.get()
        if id_cliente:
            # Actualizar
            result = self.controller.update_cliente(int(id_cliente), nombre, telefono, dni, direccion)
            if result:
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el cliente")
        else:
            # Crear nuevo
            result = self.controller.create_cliente(nombre, telefono, dni, direccion)
            if result:
                messagebox.showinfo("Éxito", "Cliente creado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo crear el cliente")
        
        # Recargar datos
        self.load_clientes()
        self.new_cliente()
    
    def delete_cliente(self):
        """Elimina un cliente"""
        id_cliente = self.var_id.get()
        if not id_cliente:
            messagebox.showerror("Error", "Debe seleccionar un cliente para eliminar")
            return
        
        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?\nEsta acción no se puede deshacer."):
            result = self.controller.delete_cliente(int(id_cliente))
            if result:
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.load_clientes()
                self.new_cliente()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente")