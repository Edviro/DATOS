from .connection import DatabaseConnection

class BaseModel:
    """Clase base para todos los modelos"""
    def __init__(self):
        self.db = DatabaseConnection()

class Categoria(BaseModel):
    def __init__(self, id=None, nombre=None, descripcion=None):
        super().__init__()
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
    
    def save(self):
        """Guarda o actualiza una categoría en la base de datos"""
        if self.id is None:
            # Insertar nueva categoría
            query = "INSERT INTO Categoria (NombreCat, Descripcion) VALUES (?, ?)"
            cursor = self.db.execute_query(query, (self.nombre, self.descripcion))
            self.id = cursor.lastrowid
        else:
            # Actualizar categoría existente
            query = "UPDATE Categoria SET NombreCat = ?, Descripcion = ? WHERE idCategoria = ?"
            self.db.execute_query(query, (self.nombre, self.descripcion, self.id))
        return self.id
    
    def delete(self):
        """Elimina una categoría de la base de datos"""
        if self.id:
            query = "DELETE FROM Categoria WHERE idCategoria = ?"
            self.db.execute_query(query, (self.id,))
            return True
        return False
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene una categoría por su ID"""
        db = DatabaseConnection()
        query = "SELECT * FROM Categoria WHERE idCategoria = ?"
        row = db.fetch_one(query, (id,))
        if row:
            return cls(id=row['idCategoria'], nombre=row['NombreCat'], descripcion=row['Descripcion'])
        return None
    
    @classmethod
    def get_all(cls):
        """Obtiene todas las categorías"""
        db = DatabaseConnection()
        query = "SELECT * FROM Categoria ORDER BY NombreCat"
        rows = db.fetch_all(query)
        return [cls(id=row['idCategoria'], nombre=row['NombreCat'], descripcion=row['Descripcion']) for row in rows]

class Producto(BaseModel):
    def __init__(self, id=None, nombre=None, precio=None, stock=None, id_categoria=None):
        super().__init__()
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock
        self.id_categoria = id_categoria
    
    def save(self):
        """Guarda o actualiza un producto en la base de datos"""
        if self.id is None:
            # Insertar nuevo producto
            query = "INSERT INTO Producto (NombrePro, Precio, Stock, idCategoria) VALUES (?, ?, ?, ?)"
            cursor = self.db.execute_query(query, (self.nombre, self.precio, self.stock, self.id_categoria))
            self.id = cursor.lastrowid
        else:
            # Actualizar producto existente
            query = "UPDATE Producto SET NombrePro = ?, Precio = ?, Stock = ?, idCategoria = ? WHERE idProducto = ?"
            self.db.execute_query(query, (self.nombre, self.precio, self.stock, self.id_categoria, self.id))
        return self.id
    
    def delete(self):
        """Elimina un producto de la base de datos"""
        if self.id:
            query = "DELETE FROM Producto WHERE idProducto = ?"
            self.db.execute_query(query, (self.id,))
            return True
        return False
    
    def update_stock(self, cantidad):
        """Actualiza el stock de un producto"""
        if self.id:
            self.stock += cantidad
            query = "UPDATE Producto SET Stock = ? WHERE idProducto = ?"
            self.db.execute_query(query, (self.stock, self.id))
            return True
        return False
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene un producto por su ID"""
        db = DatabaseConnection()
        query = "SELECT * FROM Producto WHERE idProducto = ?"
        row = db.fetch_one(query, (id,))
        if row:
            return cls(id=row['idProducto'], nombre=row['NombrePro'], precio=row['Precio'], 
                       stock=row['Stock'], id_categoria=row['idCategoria'])
        return None
    
    @classmethod
    def get_all(cls):
        """Obtiene todos los productos"""
        db = DatabaseConnection()
        query = "SELECT * FROM Producto ORDER BY NombrePro"
        rows = db.fetch_all(query)
        return [cls(id=row['idProducto'], nombre=row['NombrePro'], precio=row['Precio'], 
                   stock=row['Stock'], id_categoria=row['idCategoria']) for row in rows]
    
    @classmethod
    def get_by_categoria(cls, id_categoria):
        """Obtiene productos por categoría"""
        db = DatabaseConnection()
        query = "SELECT * FROM Producto WHERE idCategoria = ? ORDER BY NombrePro"
        rows = db.fetch_all(query, (id_categoria,))
        return [cls(id=row['idProducto'], nombre=row['NombrePro'], precio=row['Precio'], 
                   stock=row['Stock'], id_categoria=row['idCategoria']) for row in rows]

class Venta(BaseModel):
    def __init__(self, id=None, fecha=None, total=None, id_cliente=None, id_empleado=None):
        super().__init__()
        self.id = id
        self.fecha = fecha
        self.total = total
        self.id_cliente = id_cliente
        self.id_empleado = id_empleado
    
    def save(self):
        if self.id is None:
            query = "INSERT INTO Venta (Fecha, Total, idCliente, idEmpleado) VALUES (?, ?, ?, ?)"
            cursor = self.db.execute_query(query, (self.fecha, self.total, self.id_cliente, self.id_empleado))
            self.id = cursor.lastrowid
        else:
            query = "UPDATE Venta SET Fecha = ?, Total = ?, idCliente = ?, idEmpleado = ? WHERE idVenta = ?"
            self.db.execute_query(query, (self.fecha, self.total, self.id_cliente, self.id_empleado, self.id))
        return self.id
    
    def delete(self):
        if self.id:
            query = "DELETE FROM Venta WHERE idVenta = ?"
            self.db.execute_query(query, (self.id,))
            return True
        return False
    
    @classmethod
    def get_by_id(cls, id):
        db = DatabaseConnection()
        query = "SELECT * FROM Venta WHERE idVenta = ?"
        row = db.fetch_one(query, (id,))
        if row:
            return cls(id=row['idVenta'], fecha=row['Fecha'], total=row['Total'], 
                      id_cliente=row['idCliente'], id_empleado=row['idEmpleado'])
        return None
    
    @classmethod
    def get_all(cls):
        db = DatabaseConnection()
        query = "SELECT * FROM Venta ORDER BY Fecha DESC"
        rows = db.fetch_all(query)
        return [cls(id=row['idVenta'], fecha=row['Fecha'], total=row['Total'], 
                   id_cliente=row['idCliente'], id_empleado=row['idEmpleado']) for row in rows]

class DetalleVenta(BaseModel):
    def __init__(self, id=None, id_venta=None, id_producto=None, cantidad=None, precio=None, subtotal=None):
        super().__init__()
        self.id = id
        self.id_venta = id_venta
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.precio = precio
        self.subtotal = subtotal
    
    def save(self):
        if self.id is None:
            query = "INSERT INTO DetalleVenta (idVenta, idProducto, Cantidad, PrecioUni, SubTotal) VALUES (?, ?, ?, ?, ?)"
            cursor = self.db.execute_query(query, (self.id_venta, self.id_producto, self.cantidad, self.precio, self.subtotal))
            self.id = cursor.lastrowid
        else:
            query = "UPDATE DetalleVenta SET idVenta = ?, idProducto = ?, Cantidad = ?, PrecioUni = ?, SubTotal = ? WHERE idDetalleVenta = ?"
            self.db.execute_query(query, (self.id_venta, self.id_producto, self.cantidad, self.precio, self.subtotal, self.id))
        return self.id
    
    def delete(self):
        if self.id:
            query = "DELETE FROM DetalleVenta WHERE idDetalleVenta = ?"
            self.db.execute_query(query, (self.id,))
            return True
        return False
    
    @classmethod
    def get_by_venta(cls, id_venta):
        db = DatabaseConnection()
        query = "SELECT * FROM DetalleVenta WHERE idVenta = ?"
        rows = db.fetch_all(query, (id_venta,))
        return [cls(id=row['idDetalleVenta'], id_venta=row['idVenta'], id_producto=row['idProducto'], 
                   cantidad=row['Cantidad'], precio=row['PrecioUni'], subtotal=row['SubTotal']) for row in rows]
    
class Cliente(BaseModel):
    def __init__(self, id=None, nombre=None, telefono=None, dni=None, direccion=None):
        super().__init__()
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.dni = dni
        self.direccion = direccion
    
    def save(self):
        if self.id is None:
            query = "INSERT INTO Cliente (NombreCli, TelefonoCli, Dni, DireccionClie) VALUES (?, ?, ?, ?)"
            cursor = self.db.execute_query(query, (self.nombre, self.telefono, self.dni, self.direccion))
            self.id = cursor.lastrowid
        else:
            query = "UPDATE Cliente SET NombreCli = ?, TelefonoCli = ?, Dni = ?, DireccionClie = ? WHERE idCliente = ?"
            self.db.execute_query(query, (self.nombre, self.telefono, self.dni, self.direccion, self.id))
        return self.id
    
    def delete(self):
        if self.id:
            query = "DELETE FROM Cliente WHERE idCliente = ?"
            self.db.execute_query(query, (self.id,))
            return True
        return False
    
    @classmethod
    def get_by_id(cls, id):
        db = DatabaseConnection()
        query = "SELECT * FROM Cliente WHERE idCliente = ?"
        row = db.fetch_one(query, (id,))
        if row:
            return cls(id=row['idCliente'], nombre=row['NombreCli'], 
                      telefono=row['TelefonoCli'], dni=row['Dni'], 
                      direccion=row['DireccionClie'])
        return None
    
    @classmethod
    def get_all(cls):
        db = DatabaseConnection()
        query = "SELECT * FROM Cliente ORDER BY NombreCli"
        rows = db.fetch_all(query)
        return [cls(id=row['idCliente'], nombre=row['NombreCli'], 
                   telefono=row['TelefonoCli'], dni=row['Dni'], 
                   direccion=row['DireccionClie']) for row in rows]

class Empleado(BaseModel):
    def __init__(self, id=None, nombre=None, correo=None, telefono=None, direccion=None):
        super().__init__()
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
    
    def save(self):
        if self.id is None:
            query = "INSERT INTO Empleado (NombreEmp, CorreoEmp, Telefono, DireccionEmp) VALUES (?, ?, ?, ?)"
            cursor = self.db.execute_query(query, (self.nombre, self.correo, self.telefono, self.direccion))
            self.id = cursor.lastrowid
        else:
            query = "UPDATE Empleado SET NombreEmp = ?, CorreoEmp = ?, Telefono = ?, DireccionEmp = ? WHERE idEmpleado = ?"
            self.db.execute_query(query, (self.nombre, self.correo, self.telefono, self.direccion, self.id))
        return self.id
    
    def delete(self):
        if self.id:
            query = "DELETE FROM Empleado WHERE idEmpleado = ?"
            self.db.execute_query(query, (self.id,))
            return True
        return False
    
    @classmethod
    def get_by_id(cls, id):
        db = DatabaseConnection()
        query = "SELECT * FROM Empleado WHERE idEmpleado = ?"
        row = db.fetch_one(query, (id,))
        if row:
            return cls(id=row['idEmpleado'], nombre=row['NombreEmp'], 
                      correo=row['CorreoEmp'], telefono=row['Telefono'], 
                      direccion=row['DireccionEmp'])
        return None
    
    @classmethod
    def get_all(cls):
        db = DatabaseConnection()
        query = "SELECT * FROM Empleado ORDER BY NombreEmp"
        rows = db.fetch_all(query)
        return [cls(id=row['idEmpleado'], nombre=row['NombreEmp'], 
                   correo=row['CorreoEmp'], telefono=row['Telefono'], 
                   direccion=row['DireccionEmp']) for row in rows]

class Factura(BaseModel):
    def __init__(self, id=None, numero_factura=None, fecha=None, subtotal=None, 
                 impuesto=None, total=None, estado='Pendiente', observaciones=None,
                 id_venta=None, id_cliente=None, id_empleado=None):
        super().__init__()
        self.id = id
        self.numero_factura = numero_factura
        self.fecha = fecha
        self.subtotal = subtotal
        self.impuesto = impuesto
        self.total = total
        self.estado = estado
        self.observaciones = observaciones
        self.id_venta = id_venta
        self.id_cliente = id_cliente
        self.id_empleado = id_empleado
    
    def save(self):
        """Guarda o actualiza una factura en la base de datos"""
        if self.id is None:
            query = """INSERT INTO Factura (NumeroFactura, Fecha, SubTotal, Impuesto, Total, 
                      Estado, Observaciones, idVenta, idCliente, idEmpleado) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor = self.db.execute_query(query, (self.numero_factura, self.fecha, self.subtotal,
                                                 self.impuesto, self.total, self.estado, 
                                                 self.observaciones, self.id_venta, 
                                                 self.id_cliente, self.id_empleado))
            self.id = cursor.lastrowid
        else:
            query = """UPDATE Factura SET NumeroFactura = ?, Fecha = ?, SubTotal = ?, 
                      Impuesto = ?, Total = ?, Estado = ?, Observaciones = ?, 
                      idVenta = ?, idCliente = ?, idEmpleado = ? WHERE idFactura = ?"""
            self.db.execute_query(query, (self.numero_factura, self.fecha, self.subtotal,
                                        self.impuesto, self.total, self.estado, 
                                        self.observaciones, self.id_venta, 
                                        self.id_cliente, self.id_empleado, self.id))
        return self.id
    
    def delete(self):
        """Elimina una factura de la base de datos"""
        if self.id:
            query = "DELETE FROM Factura WHERE idFactura = ?"
            self.db.execute_query(query, (self.id,))
            return True
        return False
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene una factura por su ID"""
        db = DatabaseConnection()
        query = "SELECT * FROM Factura WHERE idFactura = ?"
        row = db.fetch_one(query, (id,))
        if row:
            return cls(id=row['idFactura'], numero_factura=row['NumeroFactura'],
                      fecha=row['Fecha'], subtotal=row['SubTotal'], 
                      impuesto=row['Impuesto'], total=row['Total'],
                      estado=row['Estado'], observaciones=row['Observaciones'],
                      id_venta=row['idVenta'], id_cliente=row['idCliente'],
                      id_empleado=row['idEmpleado'])
        return None
    
    @classmethod
    def get_all(cls):
        """Obtiene todas las facturas"""
        db = DatabaseConnection()
        query = "SELECT * FROM Factura ORDER BY Fecha DESC"
        rows = db.fetch_all(query)
        return [cls(id=row['idFactura'], numero_factura=row['NumeroFactura'],
                   fecha=row['Fecha'], subtotal=row['SubTotal'], 
                   impuesto=row['Impuesto'], total=row['Total'],
                   estado=row['Estado'], observaciones=row['Observaciones'],
                   id_venta=row['idVenta'], id_cliente=row['idCliente'],
                   id_empleado=row['idEmpleado']) for row in rows]
    
    @classmethod
    def get_by_numero(cls, numero_factura):
        """Obtiene una factura por su número"""
        db = DatabaseConnection()
        query = "SELECT * FROM Factura WHERE NumeroFactura = ?"
        row = db.fetch_one(query, (numero_factura,))
        if row:
            return cls(id=row['idFactura'], numero_factura=row['NumeroFactura'],
                      fecha=row['Fecha'], subtotal=row['SubTotal'], 
                      impuesto=row['Impuesto'], total=row['Total'],
                      estado=row['Estado'], observaciones=row['Observaciones'],
                      id_venta=row['idVenta'], id_cliente=row['idCliente'],
                      id_empleado=row['idEmpleado'])
        return None
    
    @classmethod
    def get_by_cliente(cls, id_cliente):
        """Obtiene facturas por cliente"""
        db = DatabaseConnection()
        query = "SELECT * FROM Factura WHERE idCliente = ? ORDER BY Fecha DESC"
        rows = db.fetch_all(query, (id_cliente,))
        return [cls(id=row['idFactura'], numero_factura=row['NumeroFactura'],
                   fecha=row['Fecha'], subtotal=row['SubTotal'], 
                   impuesto=row['Impuesto'], total=row['Total'],
                   estado=row['Estado'], observaciones=row['Observaciones'],
                   id_venta=row['idVenta'], id_cliente=row['idCliente'],
                   id_empleado=row['idEmpleado']) for row in rows]
    
    @classmethod
    def get_by_estado(cls, estado):
        """Obtiene facturas por estado"""
        db = DatabaseConnection()
        query = "SELECT * FROM Factura WHERE Estado = ? ORDER BY Fecha DESC"
        rows = db.fetch_all(query, (estado,))
        return [cls(id=row['idFactura'], numero_factura=row['NumeroFactura'],
                   fecha=row['Fecha'], subtotal=row['SubTotal'], 
                   impuesto=row['Impuesto'], total=row['Total'],
                   estado=row['Estado'], observaciones=row['Observaciones'],
                   id_venta=row['idVenta'], id_cliente=row['idCliente'],
                   id_empleado=row['idEmpleado']) for row in rows]

class DetalleFactura(BaseModel):
    def __init__(self, id=None, cantidad=None, precio_unitario=None, subtotal=None,
                 id_producto=None, id_factura=None):
        super().__init__()
        self.id = id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = subtotal
        self.id_producto = id_producto
        self.id_factura = id_factura
    
    def save(self):
        """Guarda o actualiza un detalle de factura en la base de datos"""
        if self.id is None:
            query = """INSERT INTO DetalleFactura (Cantidad, PrecioUni, SubTotal, idProducto, idFactura) 
                      VALUES (?, ?, ?, ?, ?)"""
            cursor = self.db.execute_query(query, (self.cantidad, self.precio_unitario, 
                                                 self.subtotal, self.id_producto, self.id_factura))
            self.id = cursor.lastrowid
        else:
            query = """UPDATE DetalleFactura SET Cantidad = ?, PrecioUni = ?, SubTotal = ?, 
                      idProducto = ?, idFactura = ? WHERE idDetalleFactura = ?"""
            self.db.execute_query(query, (self.cantidad, self.precio_unitario, self.subtotal,
                                        self.id_producto, self.id_factura, self.id))
        return self.id
    
    def delete(self):
        """Elimina un detalle de factura de la base de datos"""
        if self.id:
            query = "DELETE FROM DetalleFactura WHERE idDetalleFactura = ?"
            self.db.execute_query(query, (self.id,))
            return True
        return False
    
    @classmethod
    def get_by_factura(cls, id_factura):
        """Obtiene todos los detalles de una factura"""
        db = DatabaseConnection()
        query = """SELECT df.*, p.NombrePro as producto_nombre 
                  FROM DetalleFactura df 
                  JOIN Producto p ON df.idProducto = p.idProducto 
                  WHERE df.idFactura = ?"""
        rows = db.fetch_all(query, (id_factura,))
        return [cls(id=row['idDetalleFactura'], cantidad=row['Cantidad'],
                   precio_unitario=row['PrecioUni'], subtotal=row['SubTotal'],
                   id_producto=row['idProducto'], id_factura=row['idFactura']) for row in rows]
    
    @classmethod
    def get_by_id(cls, id):
        """Obtiene un detalle de factura por su ID"""
        db = DatabaseConnection()
        query = "SELECT * FROM DetalleFactura WHERE idDetalleFactura = ?"
        row = db.fetch_one(query, (id,))
        if row:
            return cls(id=row['idDetalleFactura'], cantidad=row['Cantidad'],
                      precio_unitario=row['PrecioUni'], subtotal=row['SubTotal'],
                      id_producto=row['idProducto'], id_factura=row['idFactura'])
        return None
    
    @classmethod
    def delete_by_factura(cls, id_factura):
        """Elimina todos los detalles de una factura"""
        db = DatabaseConnection()
        query = "DELETE FROM DetalleFactura WHERE idFactura = ?"
        db.execute_query(query, (id_factura,))
        return True