import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from config.config_manager import config_manager

class ConfigView:
    def __init__(self, parent):
        self.parent = parent
        
        # Variables para los campos del formulario
        self.var_currency_symbol = tk.StringVar()
        self.var_currency_name = tk.StringVar()
        self.var_currency_code = tk.StringVar()
        self.var_decimal_places = tk.StringVar()
        self.var_theme = tk.StringVar()
        self.var_stock_alert = tk.StringVar()
        self.var_encoding = tk.StringVar()
        
        # Crear la interfaz
        self.create_widgets()
        
        # Cargar configuración actual
        self.load_current_config()
    
    def create_widgets(self):
        """Crea los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = ttk.Label(main_frame, text="Configuración del Sistema", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Notebook para organizar las configuraciones
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de Moneda
        currency_frame = ttk.Frame(notebook)
        notebook.add(currency_frame, text="Moneda")
        self.create_currency_tab(currency_frame)
        
        # Pestaña de Apariencia
        appearance_frame = ttk.Frame(notebook)
        notebook.add(appearance_frame, text="Apariencia")
        self.create_appearance_tab(appearance_frame)
        
        # Pestaña de Stock
        stock_frame = ttk.Frame(notebook)
        notebook.add(stock_frame, text="Inventario")
        self.create_stock_tab(stock_frame)
        
        # Pestaña de Reportes
        reports_frame = ttk.Frame(notebook)
        notebook.add(reports_frame, text="Reportes")
        self.create_reports_tab(reports_frame)
        
        # Botones de acción
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Guardar Cambios", command=self.save_config, bootstyle=SUCCESS).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="Restaurar Valores", command=self.load_current_config).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(btn_frame, text="Valores por Defecto", command=self.reset_to_defaults).pack(side=tk.RIGHT)
    
    def create_currency_tab(self, parent):
        """Crea la pestaña de configuración de moneda"""
        frame = ttk.LabelFrame(parent, text="Configuración de Moneda", padding=20)
        frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Símbolo de moneda
        ttk.Label(frame, text="Símbolo de Moneda:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.var_currency_symbol, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Nombre de moneda
        ttk.Label(frame, text="Nombre de Moneda:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.var_currency_name, width=20).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Código de moneda
        ttk.Label(frame, text="Código de Moneda:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.var_currency_code, width=10).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Decimales
        ttk.Label(frame, text="Lugares Decimales:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        decimal_combo = ttk.Combobox(frame, textvariable=self.var_decimal_places, values=["0", "1", "2", "3"], width=5, state="readonly")
        decimal_combo.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Monedas predefinidas
        predefined_frame = ttk.LabelFrame(parent, text="Monedas Predefinidas", padding=20)
        predefined_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        ttk.Button(predefined_frame, text="Soles Peruanos (S/)", command=lambda: self.set_currency("S/", "Soles", "PEN", 2)).pack(side=tk.LEFT, padx=5)
        ttk.Button(predefined_frame, text="Dólares (US$)", command=lambda: self.set_currency("US$", "Dólares", "USD", 2)).pack(side=tk.LEFT, padx=5)
        ttk.Button(predefined_frame, text="Euros (€)", command=lambda: self.set_currency("€", "Euros", "EUR", 2)).pack(side=tk.LEFT, padx=5)
    
    def create_appearance_tab(self, parent):
        """Crea la pestaña de configuración de apariencia"""
        frame = ttk.LabelFrame(parent, text="Configuración de Apariencia", padding=20)
        frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Tema
        ttk.Label(frame, text="Tema de la Aplicación:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        theme_combo = ttk.Combobox(frame, textvariable=self.var_theme, 
                                  values=["cosmo", "flatly", "journal", "litera", "lumen", "minty", "pulse", "sandstone", "united", "yeti"], 
                                  width=15, state="readonly")
        theme_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
    
    def create_stock_tab(self, parent):
        """Crea la pestaña de configuración de inventario"""
        frame = ttk.LabelFrame(parent, text="Configuración de Inventario", padding=20)
        frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Nivel de alerta de stock
        ttk.Label(frame, text="Nivel de Alerta de Stock Bajo:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.var_stock_alert, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(frame, text="unidades").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
    
    def create_reports_tab(self, parent):
        """Crea la pestaña de configuración de reportes"""
        frame = ttk.LabelFrame(parent, text="Configuración de Reportes", padding=20)
        frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Codificación
        ttk.Label(frame, text="Codificación de Exportación:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        encoding_combo = ttk.Combobox(frame, textvariable=self.var_encoding, 
                                     values=["utf-8-sig", "utf-8", "latin-1", "cp1252"], 
                                     width=15, state="readonly")
        encoding_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Información sobre codificación
        info_label = ttk.Label(frame, text="utf-8-sig: Recomendado para Excel (evita caracteres raros)", 
                              font=("Helvetica", 9), foreground="gray")
        info_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
    
    def set_currency(self, symbol, name, code, decimal_places):
        """Establece una moneda predefinida"""
        self.var_currency_symbol.set(symbol)
        self.var_currency_name.set(name)
        self.var_currency_code.set(code)
        self.var_decimal_places.set(str(decimal_places))
    
    def load_current_config(self):
        """Carga la configuración actual"""
        # Configuración de moneda
        currency_config = config_manager.get_currency_config()
        self.var_currency_symbol.set(currency_config['symbol'])
        self.var_currency_name.set(currency_config['name'])
        self.var_currency_code.set(currency_config['code'])
        self.var_decimal_places.set(str(currency_config['decimal_places']))
        
        # Configuración de apariencia
        self.var_theme.set(config_manager.get_theme())
        
        # Configuración de stock
        self.var_stock_alert.set(str(config_manager.get_stock_alert_level()))
        
        # Configuración de reportes
        self.var_encoding.set(config_manager.get_report_encoding())
    
    def reset_to_defaults(self):
        """Restaura los valores por defecto"""
        self.set_currency("S/", "Soles", "PEN", 2)
        self.var_theme.set("cosmo")
        self.var_stock_alert.set("10")
        self.var_encoding.set("utf-8-sig")
    
    def save_config(self):
        """Guarda la configuración"""
        try:
            # Validar campos
            if not self.var_currency_symbol.get().strip():
                messagebox.showerror("Error", "El símbolo de moneda es obligatorio")
                return
            
            if not self.var_currency_name.get().strip():
                messagebox.showerror("Error", "El nombre de moneda es obligatorio")
                return
            
            try:
                decimal_places = int(self.var_decimal_places.get())
                if decimal_places < 0 or decimal_places > 3:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Los lugares decimales deben ser un número entre 0 y 3")
                return
            
            try:
                stock_alert = int(self.var_stock_alert.get())
                if stock_alert < 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "El nivel de alerta de stock debe ser un número positivo")
                return
            
            # Guardar configuración de moneda
            config_manager.set_currency_config(
                self.var_currency_symbol.get().strip(),
                self.var_currency_name.get().strip(),
                self.var_currency_code.get().strip(),
                decimal_places
            )
            
            # Guardar configuración de apariencia
            config_manager.set_theme(self.var_theme.get())
            
            # Guardar configuración de stock
            config_manager.set_stock_alert_level(stock_alert)
            
            # Guardar configuración de reportes
            config_manager.set('Reports', 'Encoding', self.var_encoding.get())
            
            messagebox.showinfo("Éxito", "Configuración guardada correctamente.\n\nReinicie la aplicación para aplicar todos los cambios.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la configuración: {str(e)}")