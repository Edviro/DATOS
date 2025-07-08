import re

def validate_email(email):
    """Valida que el email tenga un formato correcto"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_dni(dni):
    """Valida que el DNI tenga un formato correcto (8 dígitos)"""
    pattern = r'^\d{8}$'
    return bool(re.match(pattern, dni))

def validate_phone(phone):
    """Valida que el teléfono tenga un formato correcto"""
    pattern = r'^\d{9}$'
    return bool(re.match(pattern, phone))

def validate_number(value, min_value=None, max_value=None):
    """Valida que el valor sea un número dentro del rango especificado"""
    try:
        num = float(value)
        if min_value is not None and num < min_value:
            return False
        if max_value is not None and num > max_value:
            return False
        return True
    except ValueError:
        return False

def validate_integer(value, min_value=None, max_value=None):
    """Valida que el valor sea un entero dentro del rango especificado"""
    try:
        num = int(value)
        if min_value is not None and num < min_value:
            return False
        if max_value is not None and num > max_value:
            return False
        return True
    except ValueError:
        return False

def validate_required(value):
    """Valida que el valor no esté vacío"""
    return bool(value and value.strip())