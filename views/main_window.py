import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import datetime
import os

# Importaciones de vistas
from .categoria_view import CategoriaView
from .producto_view import ProductoView
from .cliente_view import ClienteView
from .empleado_view import EmpleadoView
from .venta_view import VentaView
from .reporte_view import ReporteView
from .config_view import ConfigView

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Dcorelp - Sistema de Gestión de Ventas v1.0")
        self.root.geometry("1200x700")
        self.root.minsize(800, 600)
        
        # Configurar el tema
        self.style = ttk.Style(theme="cosmo")
        
        # Crear el layout principal
        self.create_menu()
        self.create_layout()
        self.create_statusbar()
        
        # Mostrar la pantalla de inicio por defecto
        self.show_home()
    
    def create_menu(self):
        """Crea el menú principal de la aplicación"""
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        # Menú Archivo
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Configuración", command=self.show_config)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        self.menu.add_cascade(label="Archivo", menu=file_menu)
        
        # Menú Gestión
        gestion_menu = tk.Menu(self.menu, tearoff=0)
        gestion_menu.add_command(label="Categorías", command=self.show_categorias)
        gestion_menu.add_command(label="Productos", command=self.show_productos)
        gestion_menu.add_command(label="Clientes", command=self.show_clientes)
        gestion_menu.add_command(label="Empleados", command=self.show_empleados)
        self.menu.add_cascade(label="Gestión", menu=gestion_menu)
        
        # Menú Ventas
        ventas_menu = tk.Menu(self.menu, tearoff=0)
        ventas_menu.add_command(label="Nueva Venta", command=self.show_nueva_venta)
        ventas_menu.add_command(label="Historial de Ventas", command=self.show_historial_ventas)
        self.menu.add_cascade(label="Ventas", menu=ventas_menu)
        
        # Menú Reportes
        reportes_menu = tk.Menu(self.menu, tearoff=0)
        reportes_menu.add_command(label="Ventas por Período", command=self.show_reporte_ventas)
        reportes_menu.add_command(label="Productos más Vendidos", command=self.show_reporte_productos)
        reportes_menu.add_command(label="Clientes Frecuentes", command=self.show_reporte_clientes)
        reportes_menu.add_command(label="Stock Bajo", command=self.show_reporte_stock)
        self.menu.add_cascade(label="Reportes", menu=reportes_menu)
        
        # Menú Herramientas
        tools_menu = tk.Menu(self.menu, tearoff=0)
        tools_menu.add_command(label="Configuración", command=self.show_config)
        tools_menu.add_separator()
        tools_menu.add_command(label="Manual de Usuario", command=self.show_manual)
        tools_menu.add_separator()
        tools_menu.add_command(label="Acerca de", command=self.show_about)
        self.menu.add_cascade(label="Herramientas", menu=tools_menu)
    
    def create_layout(self):
        """Crea el layout principal de la aplicación"""
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel lateral izquierdo (botones de acceso rápido)
        self.sidebar = ttk.Frame(self.main_frame, width=200, bootstyle=SECONDARY)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Botones del panel lateral
        btn_home = ttk.Button(self.sidebar, text="Inicio", width=20, command=self.show_home)
        btn_home.pack(pady=5)
        
        btn_venta = ttk.Button(self.sidebar, text="Nueva Venta", width=20, bootstyle=SUCCESS, command=self.show_nueva_venta)
        btn_venta.pack(pady=5)
        
        btn_productos = ttk.Button(self.sidebar, text="Productos", width=20, command=self.show_productos)
        btn_productos.pack(pady=5)
        
        btn_clientes = ttk.Button(self.sidebar, text="Clientes", width=20, command=self.show_clientes)
        btn_clientes.pack(pady=5)
        
        btn_reportes = ttk.Button(self.sidebar, text="Reportes", width=20, command=self.show_reporte_ventas)
        btn_reportes.pack(pady=5)
        
        # Área de contenido principal
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def create_statusbar(self):
        """Crea la barra de estado en la parte inferior"""
        self.statusbar = ttk.Frame(self.root, bootstyle=INFO)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Información del usuario
        self.user_label = ttk.Label(self.statusbar, text="Usuario: Admin", padding=5)
        self.user_label.pack(side=tk.LEFT)
        
        # Fecha y hora
        self.date_label = ttk.Label(self.statusbar, text=datetime.datetime.now().strftime("%d/%m/%Y %H:%M"), padding=5)
        self.date_label.pack(side=tk.LEFT)
        
        # Copyright
        self.copyright_label = ttk.Label(self.statusbar, text="© Dcorelp 2025", padding=5)
        self.copyright_label.pack(side=tk.RIGHT)
        
        # Actualizar la hora cada segundo
        self.update_clock()
    
    def update_clock(self):
        """Actualiza el reloj de la barra de estado"""
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.date_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
    
    # Métodos para mostrar diferentes vistas
    def show_home(self):
        """Muestra la pantalla de inicio"""
        self.clear_content_frame()
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título de bienvenida
        title = ttk.Label(welcome_frame, text="Bienvenido a Dcorelp", font=("Helvetica", 24))
        title.pack(pady=20)
        
        # Descripción
        description = ttk.Label(welcome_frame, 
                              text="Sistema de Gestión de Ventas e Inventario\nVersión 1.0.0", 
                              font=("Helvetica", 14))
        description.pack(pady=10)
        
        # Imagen de logo (placeholder)
        logo_frame = ttk.Frame(welcome_frame, width=200, height=200)
        logo_frame.pack(pady=20)
        logo_label = ttk.Label(logo_frame, text="[LOGO]", font=("Helvetica", 36))
        logo_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Accesos rápidos
        quick_access = ttk.LabelFrame(welcome_frame, text="Accesos Rápidos", padding=10)
        quick_access.pack(fill=tk.X, pady=20, padx=50)
        
        # Botones de acceso rápido en grid
        btn_nueva_venta = ttk.Button(quick_access, text="Nueva Venta", 
                                   bootstyle=SUCCESS, width=15, command=self.show_nueva_venta)
        btn_nueva_venta.grid(row=0, column=0, padx=10, pady=10)
        
        btn_productos = ttk.Button(quick_access, text="Productos", 
                                 width=15, command=self.show_productos)
        btn_productos.grid(row=0, column=1, padx=10, pady=10)
        
        btn_clientes = ttk.Button(quick_access, text="Clientes", 
                                width=15, command=self.show_clientes)
        btn_clientes.grid(row=0, column=2, padx=10, pady=10)
        
        btn_reportes = ttk.Button(quick_access, text="Reportes", 
                                width=15, command=self.show_reporte_ventas)
        btn_reportes.grid(row=1, column=0, padx=10, pady=10)
        
        btn_empleados = ttk.Button(quick_access, text="Empleados", 
                                 width=15, command=self.show_empleados)
        btn_empleados.grid(row=1, column=1, padx=10, pady=10)
        
        btn_config = ttk.Button(quick_access, text="Configuración", 
                              width=15, command=self.show_config)
        btn_config.grid(row=1, column=2, padx=10, pady=10)
    
    def clear_content_frame(self):
        """Limpia el contenido del frame principal"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    # Métodos placeholder para las diferentes vistas
    def show_config(self):
        """Muestra la vista de configuración"""
        self.clear_content_frame()
        ConfigView(self.content_frame)
    
    def show_categorias(self):
        self.clear_content_frame()
        self.categoria_view = CategoriaView(self.content_frame)
    
    def show_productos(self):
        self.clear_content_frame()
        self.producto_view = ProductoView(self.content_frame)
    
    def show_clientes(self):
        self.clear_content_frame()
        self.cliente_view = ClienteView(self.content_frame)
    
    def show_empleados(self):
        self.clear_content_frame()
        self.empleado_view = EmpleadoView(self.content_frame)
    
    def show_nueva_venta(self):
        self.clear_content_frame()
        self.venta_view = VentaView(self.content_frame)
    
    def show_historial_ventas(self):
        self.clear_content_frame()
        # Implementar vista de historial de ventas
        ttk.Label(self.content_frame, text="Historial de Ventas", font=("Helvetica", 20)).pack(pady=20)
    
    def show_reporte_ventas(self):
        self.clear_content_frame()
        self.reporte_view = ReporteView(self.content_frame, 'ventas')
    
    def show_reporte_productos(self):
        self.clear_content_frame()
        self.reporte_view = ReporteView(self.content_frame, 'productos')
    
    def show_reporte_clientes(self):
        self.clear_content_frame()
        self.reporte_view = ReporteView(self.content_frame, 'clientes')
    
    def show_reporte_stock(self):
        self.clear_content_frame()
        self.reporte_view = ReporteView(self.content_frame, 'stock')
    
    def show_manual(self):
        self.clear_content_frame()
        ttk.Label(self.content_frame, text="Manual de Usuario", font=("Helvetica", 20)).pack(pady=20)
        # Aquí se implementará la vista del manual de usuario
    
    def show_about(self):
        self.clear_content_frame()
        about_frame = ttk.Frame(self.content_frame)
        about_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(about_frame, text="Acerca de Dcorelp", font=("Helvetica", 20)).pack(pady=20)
        ttk.Label(about_frame, text="Sistema de Gestión de Ventas e Inventario", font=("Helvetica", 14)).pack()
        ttk.Label(about_frame, text="Versión 1.0.0", font=("Helvetica", 12)).pack(pady=5)
        ttk.Label(about_frame, text="© Dcorelp 2025", font=("Helvetica", 10)).pack(pady=5)
        ttk.Label(about_frame, text="Todos los derechos reservados", font=("Helvetica", 10)).pack()