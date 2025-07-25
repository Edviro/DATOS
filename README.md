# Sistema de Gestión de Ventas Dcorelp

## Descripción
Sistema completo de gestión de ventas con funcionalidades de facturación, exportación a Excel y PDF, y generación de reportes.

## Características Principales

### Gestión de Facturas
- ✅ Creación y edición de facturas
- ✅ Conexión automática con clientes, empleados y ventas
- ✅ Generación automática de números de factura
- ✅ Estados de factura (Pendiente, Pagada, Cancelada, Vencida)
- ✅ Exportación individual a PDF y Excel
- ✅ Filtrado por estado y fecha

### Exportación Avanzada
- ✅ Exportación de facturas individuales a PDF con formato profesional
- ✅ Exportación de facturas individuales a Excel con formato empresarial
- ✅ Exportación de reportes de facturas a CSV y Excel
- ✅ Formato de moneda automático según configuración del sistema

### Gestión General
- Gestión de productos
- Gestión de clientes
- Gestión de empleados
- Gestión de ventas
- Reportes integrados

### Integración Completa
- ✅ Conexión con base de datos de clientes
- ✅ Conexión con base de datos de empleados
- ✅ Conexión con base de datos de ventas
- ✅ Eliminación de reportes duplicados
- ✅ Interfaz unificada y coherente

## Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### Dependencias Principales
- `ttkbootstrap==1.13.9` - Framework de interfaz gráfica moderna
- `openpyxl==3.1.2` - Exportación a Excel
- `pandas==2.0.3` - Manipulación de datos
- `reportlab==4.0.4` - Generación de PDFs

## Uso

### Ejecutar la Aplicación
```bash
python main.py
```

### Gestión de Facturas

1. **Acceder al módulo de facturas:**
   - Desde el menú: Ventas → Gestión de Facturas
   - Desde la barra lateral: Botón "Facturas"

2. **Crear una nueva factura:**
   - Hacer clic en "Nueva Factura"
   - Completar los campos requeridos
   - Seleccionar cliente, empleado y venta (opcional)
   - Guardar la factura

3. **Exportar facturas:**
   - **PDF Individual:** Seleccionar factura → "Exportar PDF"
   - **Excel Individual:** Seleccionar factura → "Exportar Excel"
   - **Reporte CSV:** Usar filtros → "Exportar CSV"
   - **Reporte Excel:** Usar filtros → "Exportar Excel"

### Características de Exportación

#### Exportación PDF
- Formato profesional de factura
- Información completa del cliente y empleado
- Cálculos automáticos de subtotal, impuestos y total
- Fecha y número de factura

#### Exportación Excel
- Formato empresarial con colores y estilos
- Encabezados formateados
- Datos organizados en columnas
- Fácil manipulación posterior

## Soluciones Implementadas

### Problema: Conexión de Datos
**Solución:** Se implementaron métodos `listar_*` en todos los controladores para asegurar compatibilidad con la vista de facturas.

### Problema: Reportes Duplicados
**Solución:** Se eliminó la funcionalidad de reportes duplicada de la vista de facturas, manteniendo solo la funcionalidad principal en el menú de reportes.

### Problema: Exportación Limitada
**Solución:** Se agregaron funciones avanzadas de exportación a PDF y Excel con formato profesional.

## Soporte

Para reportar problemas o solicitar nuevas características, contacte al equipo de desarrollo.
