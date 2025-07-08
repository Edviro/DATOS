import configparser
import os
from typing import Dict, Any

class ConfigManager:
    """Gestor de configuración del sistema"""
    
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), 'settings.ini')
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """Carga la configuración desde el archivo"""
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Crea la configuración por defecto"""
        self.config['General'] = {
            'AppName': 'Dcorelp',
            'Version': '1.0.0',
            'Theme': 'cosmo',
            'Language': 'es'
        }
        
        self.config['Currency'] = {
            'Symbol': 'S/',
            'Name': 'Soles',
            'Code': 'PEN',
            'DecimalPlaces': '2',
            'ThousandsSeparator': ',',
            'DecimalSeparator': '.'
        }
        
        self.config['Database'] = {
            'Type': 'sqlite',
            'Path': 'data/dcorelp.db'
        }
        
        self.config['Stock'] = {
            'AlertLevel': '10'
        }
        
        self.config['Reports'] = {
            'ExportPath': 'exports/',
            'Encoding': 'utf-8-sig',
            'DateFormat': '%d/%m/%Y',
            'TimeFormat': '%H:%M:%S'
        }
        
        self.config['Backup'] = {
            'AutoBackup': 'true',
            'BackupPath': 'backups/',
            'BackupInterval': '7'
        }
        
        self.save_config()
    
    def save_config(self):
        """Guarda la configuración en el archivo"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            self.config.write(f)
    
    def get(self, section: str, key: str, fallback: Any = None) -> str:
        """Obtiene un valor de configuración"""
        return self.config.get(section, key, fallback=fallback)
    
    def set(self, section: str, key: str, value: str):
        """Establece un valor de configuración"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        self.save_config()
    
    def get_currency_config(self) -> Dict[str, str]:
        """Obtiene la configuración de moneda"""
        return {
            'symbol': self.get('Currency', 'Symbol', 'S/'),
            'name': self.get('Currency', 'Name', 'Soles'),
            'code': self.get('Currency', 'Code', 'PEN'),
            'decimal_places': int(self.get('Currency', 'DecimalPlaces', '2')),
            'thousands_separator': self.get('Currency', 'ThousandsSeparator', ','),
            'decimal_separator': self.get('Currency', 'DecimalSeparator', '.')
        }
    
    def set_currency_config(self, symbol: str, name: str, code: str, decimal_places: int = 2):
        """Configura los parámetros de moneda"""
        self.set('Currency', 'Symbol', symbol)
        self.set('Currency', 'Name', name)
        self.set('Currency', 'Code', code)
        self.set('Currency', 'DecimalPlaces', str(decimal_places))
        self.save_config()
    
    def get_currency_config(self):
        """Obtiene la configuración completa de moneda"""
        return {
            'symbol': self.get('Currency', 'Symbol', 'S/'),
            'name': self.get('Currency', 'Name', 'Soles'),
            'code': self.get('Currency', 'Code', 'PEN'),
            'decimal_places': int(self.get('Currency', 'DecimalPlaces', '2'))
        }
    
    def get_report_encoding(self) -> str:
        """Obtiene la codificación para reportes"""
        return self.get('Reports', 'Encoding', 'utf-8-sig')
    
    def get_theme(self) -> str:
        """Obtiene el tema de la aplicación"""
        return self.get('General', 'Theme', 'cosmo')
    
    def set_theme(self, theme: str):
        """Establece el tema de la aplicación"""
        self.set('General', 'Theme', theme)
    
    def get_stock_alert_level(self) -> int:
        """Obtiene el nivel de alerta de stock"""
        return int(self.get('Stock', 'AlertLevel', '10'))
    
    def set_stock_alert_level(self, level: int):
        """Establece el nivel de alerta de stock"""
        self.set('Stock', 'AlertLevel', str(level))

# Instancia global del gestor de configuración
config_manager = ConfigManager()