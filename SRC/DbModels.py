from db import dbconnection
from flask import jsonify
connection = dbconnection()  # Obtenemos la conexión

#AQUI ESTAN TODOS LOS QUERYS QUE REFERENCIAN AL USUARIO
def login(celular, contrasena):
    try:
        print("estoy realizando la confirmacion del login")
        with connection.cursor() as cursor: #para que el cursor se cierre automaticamente
            print("voy a usar el cursor")
            cursor.execute("EXEC sp_ReadUser ?, ?", (celular, contrasena))
            row_login = cursor.fetchone()
        print(row_login) #intente meter los datos arrojados a un string para poder utilizarlos mas tarde e imprimirlos
        return row_login
    except Exception as ex:
        raise Exception(f"Error al ejecutar Login para el celular: {celular}: {str(ex)}") #f es para poder colocar variables dentro del string mas facil

def register_user(nombre, apellido, celular, contrasena):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_CreateUser ?, ?, ?, ?, ?", (nombre, apellido, 1, celular, contrasena))
        print("Registro completado con éxito")
        return True  # Indica que el registro fue exitoso
    except Exception as ex:
        print(f"Error al registrar usuario: {str(ex)}")
        return False  

def delete_user (celular, contrasena):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_DeleteUser ?, ?", (celular, contrasena))
        print("El usuario ha sido eliminado con exito")
    except Exception as ex:
        print (f"Error al eliminar el usuario: {str(ex)}")
        
def modify_user (celular, nombre, apellido):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_UpdateUser ?, ?, ?", (celular, nombre, apellido))
        print("El usuario ha sido modificado con exito")
    except Exception as ex:
        print (f"Error al modificar el usuario: {str(ex)}")
        
def modify_password (celular, nuevacontrasena):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_UpdatePassword ?, ?", (celular, nuevacontrasena))
        print("El usuario ha sido modificado con exito")
    except Exception as ex:
        print (f"Error al modificar el usuario: {str(ex)}")
        
# A PARTIR DE AQUI COMIENZA TODO LO RELACIONADO CON LOS PRODUCTOS --------------------------------------------------------------------

def busqueda_productos_AD(termino): #AD = ALL DESCRIPTION BY A DESCRIPTION
    resultados = []
    try:
        query = "SELECT TOP 6 IdProducto, Descripcion, PActual, PNormal, IdTienda, Imagen FROM TProducto WHERE LOWER(Descripcion) LIKE ?"
        with connection.cursor() as cursor:
            cursor.execute(query, ('%' + termino.lower() + '%',))
            productos = cursor.fetchall()
            query = "SELECT Tienda FROM TTiendas WHERE Idtienda LIKE ?"
            for producto in productos:
                id_tienda = producto[4]
                query_tienda = "SELECT DTienda FROM TTiendas WHERE IdTienda = ?"
                cursor.execute(query_tienda, (id_tienda,))
                tienda = cursor.fetchone()
                #tienda = 1 EN UN RATO SE QUITA ESO SE NECESITA LA TABLA TIENDA
                resultados.append({
                    'id_producto': producto[0],
                    'descripcion': producto[1],
                    'precio': producto[2], #PRECIO ACTUAL SIEMPRE EXISTE, EL NORMAL ES CUANDO HAY OFERTA(PRECIO ACTRUAL) Y TIENE QUE SALIR EL PRECIO ORIGINAL DIFERENTE
                    'precio_oferta': producto[3], #PRECIO NORMAL EN CASO QUE TENGA OFERTA SE OTORGA EL PRECIO BASE
                    'tienda': tienda,
                    'imagen': producto[5]
            })
        return resultados
    except Exception as e:
        print(f"Error al buscar productos AD: {e}")
        return resultados  # Devuelve lista vacía en caso de error
    
    
    
def busqueda_productos(termino): #BY DESCRIPTION ESTO ES PARA LA BARRA BUSCADORA
    resultados = []
    try:
        query = "SELECT TOP 8 IdProducto, Descripcion FROM TProducto WHERE LOWER(Descripcion) LIKE ? "
        with connection.cursor() as cursor:
            # Ejecutar consulta con parámetros
            cursor.execute(query, ('%' + termino.lower() + '%',))
            productos = cursor.fetchall()
        for producto in productos:
            resultados.append({
                'id_producto': producto[0],
                'descripcion': producto[1]
            })
        return resultados
    except Exception as e:
        print(f"Error al buscar productos en la barra: {e}") #can only concatenate str (not "int") to str
        return resultados  # Devuelve lista vacía en caso de error

def busqueda_productos_by_id(id_producto):
    producto = {} #lista vacia que se retorna cuando el query no funciono
    try:
        query = "SELECT * FROM TProducto WHERE IdProducto LIKE ? "
        with connection.cursor() as cursor:
            cursor.execute(query, ('%' + str(id_producto) + '%',))
            atributo = cursor.fetchone()
            id_tienda = atributo[4]
            query_tienda = "SELECT DTienda FROM TTiendas WHERE IdTienda = ?"
            cursor.execute(query_tienda, id_tienda)
            tienda = cursor.fetchone()
            print(f"imprimire: {tienda}")#SE IMPRIME EN PARENTESIS
            #tienda = 1 EN UN RATO SE QUITA ESO SE NECESITA LA TABLA TIENDA 
            producto = {
                'id_producto': atributo[0],
                'descripcion': atributo[1],
                'id_categoria': atributo[2],
                'imagen': atributo[3],
                'tienda': tienda, 
                'precio_normal': atributo[5], #PRECIO NORMAL EN CASO QUE TENGA OFERTA SE OTORGA EL PRECIO BASE
                'precio_actual': atributo[6], #PRECIO ACTUAL SIEMPRE EXISTE, EL NORMAL ES CUANDO HAY OFERTA(PRECIO ACTRUAL) Y TIENE QUE SALIR EL PRECIO ORIGINAL DIFERENTE
                'URL': atributo[7]
            }
        return producto
    except Exception as e:
        print(f"Error al buscar productos por ID: {e}")
    
#AQUI VA TODO LO RELACIONADO CON EL CARRIT0