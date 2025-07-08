import datetime
import locale
import os
import csv
from config.config_manager import config_manager

# Configurar el locale para formateo de moneda
try:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
    except locale.Error:
        pass

def format_currency(amount):
    """Formatea un valor como moneda usando la configuración del sistema"""
    try:
        currency_config = config_manager.get_currency_config()
        symbol = currency_config['symbol']
        decimal_places = currency_config['decimal_places']
        thousands_sep = currency_config['thousands_separator']
        decimal_sep = currency_config['decimal_separator']
        
        # Formatear el número
        formatted_amount = f"{float(amount):,.{decimal_places}f}"
        
        # Reemplazar separadores si es necesario
        if thousands_sep != ',' or decimal_sep != '.':
            parts = formatted_amount.split('.')
            if len(parts) == 2:
                integer_part = parts[0].replace(',', thousands_sep)
                decimal_part = parts[1]
                formatted_amount = f"{integer_part}{decimal_sep}{decimal_part}"
            else:
                formatted_amount = parts[0].replace(',', thousands_sep)
        
        return f"{symbol} {formatted_amount}"
    except Exception as e:
        # Fallback en caso de error
        return f"S/ {float(amount):.2f}"

def format_date(date):
    """Formatea una fecha en formato dd/mm/yyyy"""
    if isinstance(date, str):
        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            return date
    return date.strftime("%d/%m/%Y")

def get_current_date():
    """Obtiene la fecha actual en formato yyyy-mm-dd"""
    return datetime.date.today().strftime("%Y-%m-%d")

def export_to_csv(data, filename, headers=None):
    """Exporta datos a un archivo CSV con codificación UTF-8-BOM"""
    filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'exports', filename)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Usar la codificación configurada en el sistema
    encoding = config_manager.get_report_encoding()
    
    with open(filepath, 'w', newline='', encoding=encoding) as f:
        writer = csv.writer(f, delimiter=';')  # Usar punto y coma como separador
        if headers:
            writer.writerow(headers)
        writer.writerows(data)
    
    return filepath

def calculate_subtotal(price, quantity):
    """Calcula el subtotal de un producto"""
    return float(price) * int(quantity)