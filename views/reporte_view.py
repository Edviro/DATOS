import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import datetime
import os

from controllers.reporte_controller import ReporteController
from utils.helpers import format_currency, format_date

class ReporteView:
    def __init__(self, parent, tipo_reporte='ventas'):
        self.parent = parent
        self.controller = ReporteController()
        self.tipo_reporte = tipo_reporte
        
        # Variables para los filtros
        self.var_fecha_inicio = tk.StringVar(value=datetime.date.today().replace(day=1).strftime("%Y-%m-%d"))
        self.var_fecha_fin = tk.StringVar(value=datetime.date.today().strftime("%Y-%m-%d"))
        self.var_limite = tk.StringVar(value="10")
        
        # Crear la interfaz según el tipo de reporte
        self.create_widgets()
        
        # Cargar datos iniciales
        self.generar_reporte()
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame superior (filtros)
        filter_frame = ttk.LabelFrame(main_frame, text="Filtros", padding=10)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Configurar filtros según el tipo de reporte
        if self.tipo_reporte in ['ventas', 'productos']:
            # Filtro de fechas
            ttk.Label(filter_frame, text="Fecha Inicio:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
            ttk.Entry(filter_frame, textvariable=self.var_fecha_inicio, width=15).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
            
            ttk.Label(filter_frame, text="Fecha Fin:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
            ttk.Entry(filter_frame, textvariable=self.var_fecha_fin, width=15).grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        if self.tipo_reporte in ['productos', 'clientes', 'stock']:
            # Filtro de límite
            ttk.Label(filter_frame, text="Límite:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
            ttk.Entry(filter_frame, textvariable=self.var_limite, width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Botones de acción
        btn_frame = ttk.Frame(filter_frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Generar Reporte", command=self.generar_reporte).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Exportar a CSV", command=self.exportar_reporte).grid(row=0, column=1, padx=5)
        
        # Frame para la tabla
        table_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar columnas según el tipo de reporte
        if self.tipo_reporte == 'ventas':
            columns = ("id", "fecha", "cliente", "empleado", "total")
            headings = {"id": "ID", "fecha": "Fecha", "cliente": "Cliente", "empleado": "Empleado", "total": "Total"}
            widths = {"id": 50, "fecha": 100, "cliente": 200, "empleado": 200, "total": 100}
        elif self.tipo_reporte == 'productos':
            columns = ("id", "nombre", "categoria", "cantidad", "total")
            headings = {"id": "ID", "nombre": "Producto", "categoria": "Categoría", "cantidad": "Cantidad Vendida", "total": "Total Vendido"}
            widths = {"id": 50, "nombre": 200, "categoria": 150, "cantidad": 100, "total": 100}
        elif self.tipo_reporte == 'clientes':
            columns = ("id", "nombre", "dni", "telefono", "compras", "total")
            headings = {"id": "ID", "nombre": "Cliente", "dni": "DNI", "telefono": "Teléfono", "compras": "Total Compras", "total": "Total Gastado"}
            widths = {"id": 50, "nombre": 200, "dni": 100, "telefono": 100, "compras": 100, "total": 100}
        elif self.tipo_reporte == 'stock':
            columns = ("id", "nombre", "categoria", "stock", "precio")
            headings = {"id": "ID", "nombre": "Producto", "categoria": "Categoría", "stock": "Stock", "precio": "Precio"}
            widths = {"id": 50, "nombre": 200, "categoria": 150, "stock": 100, "precio": 100}
        
        # Crear tabla
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Configurar columnas
        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col])
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def generar_reporte(self):
        """Genera el reporte según el tipo seleccionado"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            if self.tipo_reporte == 'ventas':
                fecha_inicio = self.var_fecha_inicio.get()
                fecha_fin = self.var_fecha_fin.get()
                ventas = self.controller.generar_reporte_ventas(fecha_inicio, fecha_fin)
                
                for venta in ventas:
                    self.tree.insert("", tk.END, values=(
                        venta['id'],
                        venta['fecha'],
                        venta['cliente'],
                        venta['empleado'],
                        format_currency(venta['total'])
                    ))
            
            elif self.tipo_reporte == 'productos':
                fecha_inicio = self.var_fecha_inicio.get()
                fecha_fin = self.var_fecha_fin.get()
                limite = int(self.var_limite.get())
                productos = self.controller.generar_reporte_productos_vendidos(fecha_inicio, fecha_fin, limite)
                
                for producto in productos:
                    self.tree.insert("", tk.END, values=(
                        producto['id'],
                        producto['nombre'],
                        producto['categoria'],
                        producto['cantidad_vendida'],
                        format_currency(producto['total_vendido'])
                    ))
            
            elif self.tipo_reporte == 'clientes':
                limite = int(self.var_limite.get())
                clientes = self.controller.generar_reporte_clientes_frecuentes(limite)
                
                for cliente in clientes:
                    self.tree.insert("", tk.END, values=(
                        cliente['id'],
                        cliente['nombre'],
                        cliente['dni'],
                        cliente['telefono'],
                        cliente['total_compras'],
                        format_currency(cliente['total_gastado'])
                    ))
            
            elif self.tipo_reporte == 'stock':
                limite = int(self.var_limite.get())
                productos = self.controller.generar_reporte_stock_bajo(limite)
                
                for producto in productos:
                    self.tree.insert("", tk.END, values=(
                        producto['id'],
                        producto['nombre'],
                        producto['categoria'],
                        producto['stock'],
                        format_currency(producto['precio'])
                    ))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el reporte: {str(e)}")
    
    def exportar_reporte(self):
        """Exporta el reporte a CSV"""
        try:
            if self.tipo_reporte == 'ventas':
                fecha_inicio = self.var_fecha_inicio.get()
                fecha_fin = self.var_fecha_fin.get()
                filepath = self.controller.exportar_reporte_ventas(fecha_inicio, fecha_fin)
            
            elif self.tipo_reporte == 'productos':
                fecha_inicio = self.var_fecha_inicio.get()
                fecha_fin = self.var_fecha_fin.get()
                limite = int(self.var_limite.get())
                filepath = self.controller.exportar_reporte_productos(fecha_inicio, fecha_fin, limite)
            
            elif self.tipo_reporte == 'clientes':
                limite = int(self.var_limite.get())
                filepath = self.controller.exportar_reporte_clientes(limite)
            
            elif self.tipo_reporte == 'stock':
                limite = int(self.var_limite.get())
                filepath = self.controller.exportar_reporte_stock(limite)
            
            messagebox.showinfo("Éxito", f"Reporte exportado correctamente a:\n{filepath}")
            
            # Abrir el directorio donde se guardó el archivo
            os.startfile(os.path.dirname(filepath))
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar el reporte: {str(e)}")