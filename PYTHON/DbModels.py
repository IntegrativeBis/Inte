from db import dbconnection
from flask import jsonify
connection = dbconnection()  # Obtenemos la conexión

#AQUI ESTAN TODOS LOS QUERYS QUE REFERENCIAN AL USUARIO
def login(celular, contrasena):
    query = "SELECT IdUsuario FROM TUsuarios WHERE Celular = ?"
    try:
        print("estoy realizando la confirmacion del login")
        with connection.cursor() as cursor: 
            print("voy a usar el cursor")
            cursor.execute("EXEC sp_ReadUser ?, ?", (celular, contrasena))
            row_login = cursor.fetchone()
            cursor.execute(query, (celular,))
            id_usuario = cursor.fetchone()
        usuario_info = {
            'id_usuario': id_usuario[0],
            'nombre': row_login[0],
            'apellido': row_login[1]
        }
        print(usuario_info) 
        return usuario_info
    except Exception as ex:
        print(f"Error al ejecutar Login para el celular: {celular}: {str(ex)}") 
        return None

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
        mensaje = "El usuario ha sido eliminado con exito"
        print(mensaje)
        return mensaje
    except Exception as ex:
        print (f"Error al eliminar el usuario: {str(ex)}")
        
def modify_user (celular, nombre, apellido):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_UpdateUser ?, ?, ?", (celular, nombre, apellido))
        mensaje ="El usuario ha sido modificado con exito"
        print(mensaje)
        return mensaje
    except Exception as ex:
        print (f"Error al modificar el usuario: {str(ex)}")
        
def modify_password (celular, nuevacontrasena):
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_UpdatePassword ?, ?", (celular, nuevacontrasena))
        mensaje = "La contrasena ha sido modificado con exito"
        return mensaje 
    except Exception as ex:
        print (f"Error al modificar la contrasena: {str(ex)}")
   
# A PARTIR DE AQUI COMIENZA TODO LO RELACIONADO CON LOS PRODUCTOS --------------------------------------------------------------------

def busqueda_productos_AD(termino, pagina_actual, pagina_final): #AD = ALL DESCRIPTION BY A DESCRIPTION
    resultados = []
    query = "SELECT p.IdProducto, p.Descripcion, p.PActual, p.IdTienda, p.Imagen, t.DTienda FROM TProducto p JOIN TTiendas t ON p.IdTienda = t.IdTienda WHERE LOWER(p.Descripcion) LIKE ? ORDER BY p.IdProducto OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    try:
        while(pagina_actual <= pagina_final):
            offset = (pagina_actual - 1) * 20 # son los resultados por pagina
            with connection.cursor() as cursor:
                cursor.execute(query, ('%' + termino.lower() + '%', offset, 20))
                productos = cursor.fetchall()
                
                for producto in productos:
                    resultados.append({
                        'id_producto': producto[0],
                        'descripcion': producto[1],
                        'precio': producto[2], #PRECIO ACTUAL SIEMPRE EXISTE, EL NORMAL ES CUANDO HAY OFERTA(PRECIO ACTRUAL) Y TIENE QUE SALIR EL PRECIO ORIGINAL DIFERENTE
                        'tienda': producto[5],
                        'imagen': producto[4]
                    })
            pagina_actual += 1
            return resultados
    except Exception as e:
        print(f"Error al buscar productos AD: {e}")
        return resultados  # Devuelve lista vacía en caso de error
        
def busqueda_productos_AD_by_category(id_categoria, pagina_actual, pagina_final): #AD = ALL DESCRIPTION BY category 
    resultados = []
    query = "SELECT TOP 20 IdProducto, Descripcion, PActual, IdTienda, Imagen FROM TProducto WHERE Categoria = ?"
    query_tienda = "SELECT DTienda FROM TTiendas WHERE IdTienda = ?"
    while(pagina_actual <= pagina_final):
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, ('%' + id_categoria + '%',))
                productos = cursor.fetchall()
                for producto in productos:
                    id_tienda = producto[3]
                    cursor.execute(query_tienda, (id_tienda,))
                    tienda = cursor.fetchone()
                    resultados.append({
                        'id_producto': producto[0],
                        'descripcion': producto[1],
                        'precio': producto[2], 
                        'tienda': tienda[0],
                        'imagen': producto[4]
                    })
            pagina_actual += 1
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
        query_producto = "SELECT * FROM TProducto WHERE IdProducto LIKE ? "
        query_tienda = "SELECT DTienda FROM TTiendas WHERE IdTienda = ?"
        query_recomendaciones = "SELECT TOP 4 * FROM TProducto WHERE IdSCategoria = ? AND IdProducto NOT LIKE ? "
        with connection.cursor() as cursor:
            cursor.execute(query_producto, ('%' + str(id_producto) + '%',))
            atributo = cursor.fetchone()
            id_tienda = atributo[4]
            
            cursor.execute(query_tienda, (id_tienda,))
            tienda = cursor.fetchone()
            print(f"imprimire: {tienda[0]}")#SE IMPRIME EN PARENTESIS
            #tienda = 1 EN UN RATO SE QUITA ESO SE NECESITA LA TABLA TIENDA 
            
            cursor.execute(query_recomendaciones, ( atributo[2], atributo[0]))
            productos_recomendados = cursor.fetchall()
            
            producto = { #creamos un diccionario para el producto
                'id_producto': atributo[0],
                'descripcion': atributo[1],
                'id_subcategoria': atributo[2],
                'imagen': atributo[3],
                'tienda': tienda[0], 
                'precio_normal': atributo[5], #PRECIO NORMAL EN CASO QUE TENGA OFERTA SE OTORGA EL PRECIO BASE
                'precio_actual': atributo[6], #PRECIO ACTUAL SIEMPRE EXISTE, EL NORMAL ES CUANDO HAY OFERTA(PRECIO ACTRUAL) Y TIENE QUE SALIR EL PRECIO ORIGINAL DIFERENTE
                'URL': atributo[7]
            }
            recomendaciones = [
                {
                    'id_producto': producto_similar[0],
                    'descripcion': producto_similar[1],
                    'id_subcategoria': producto_similar[2],
                    'imagen': producto_similar[3],
                    'tienda': producto_similar[0], 
                    'precio_normal': producto_similar[5], 
                    'precio_actual': producto_similar[6], 
                    'URL': producto_similar[7]
                }
                for producto_similar in productos_recomendados
            ]
            print(producto, recomendaciones)
        return producto, recomendaciones
        
    except Exception as e:
        print(f"Error al buscar productos por ID: {e}")
        
def busqueda_productos_cantidad_by_idXlista(id_producto):
    producto = {} #lista vacia que se retorna cuando el query no funciono
    try:
        query_producto = "SELECT * FROM TProducto WHERE IdProducto LIKE ? "
        query_tienda = "SELECT DTienda FROM TTiendas WHERE IdTienda = ?"
        with connection.cursor() as cursor:
            cursor.execute(query_producto, ('%' + str(id_producto) + '%',))
            atributo = cursor.fetchone()
            id_tienda = atributo[4]
            
            cursor.execute(query_tienda, (id_tienda,))
            tienda = cursor.fetchone()
            print(f"imprimire: {tienda[0]}")#SE IMPRIME EN PARENTESIS
            
            producto = { #creamos un diccionario para el producto
                'id_producto': atributo[0],
                'descripcion': atributo[1],
                'id_subcategoria': atributo[2],
                'imagen': atributo[3],
                'tienda': tienda[0], 
                'precio_normal': atributo[5], #PRECIO NORMAL EN CASO QUE TENGA OFERTA SE OTORGA EL PRECIO BASE
                'precio_actual': atributo[6], #PRECIO ACTUAL SIEMPRE EXISTE, EL NORMAL ES CUANDO HAY OFERTA(PRECIO ACTRUAL) Y TIENE QUE SALIR EL PRECIO ORIGINAL DIFERENTE
                'URL': atributo[7]
            }
            print(producto)
        return producto
        
    except Exception as e:
        print(f"Error al buscar productos por ID: {e}")

def busqueda_categoria(): #se buscan todas las categorias de manera que puedan aparecer en inicio  
    categoria = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM TCategorias")
            categorias = cursor.fetchmany(2)
            print(categorias)
            categoria = [
                {
                    'id_categoria' : category[0],
                    'nombre_categoria': category[1]
                } 
                for category in categorias
            ]
        print(f"Las categorias son: {categoria}")
        return  categoria
    except Exception as e:
        print(f"Error al buscar la categoria, Error: {e}")  
        return categoria
    
        
#AQUI VA TODO LO RELACIONADO CON EL CARRIT0

def integrar_producto():
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_AddProduct ?", ()) #faltan las variables que necesitamos
        print("Se agrego correctamente el producto")
        return True 
    except Exception as ex:
        print(f"Error al ingresar producto: {str(ex)}")
        return False

def borrar_producto ():#faltan las variables que necesitamos
    mensaje = "se borro puro aire"
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_DeleteProduct ?, ?", ())
        mensaje = "El producto ha sido eliminado con exito"
        print(mensaje)
        return mensaje
    except Exception as ex:
        print (f"Error al eliminar el usuario: {str(ex)}")
        return mensaje
        
def modificar_producto (): #faltan las variables que necesitamos
    try:
        with connection.cursor() as cursor:
            cursor.execute("EXEC sp_UpdateUser ?, ?, ?", ())
        print("El usuario ha sido modificado con exito")
        return True
    except Exception as ex:
        print (f"Error al modificar el usuario: {str(ex)}")
        return False
    
def ver_lista(id_lista):
    lista_con_productos = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT IdProducto, Cantidad FROM TDCarritos WHERE IdCarrito = {id_lista}")
            lista = cursor.fetchall()
        print("la obtencion de la lista ha sido un exito")
        lista_con_productos = {
            'id_producto': lista[0],
            'cantidad': lista[1]
        }
        return lista_con_productos
    except Exception as ex:
        print (f"Error al dar la lista: {str(ex)}")
        return lista_con_productos

def obtener_listas(id_usuario): #se obtiene la cantidad YA ESTA
    listas = {}
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT IdCarritos, Detalle FROM TCarritos WHERE IdUsuario = {id_usuario}")
            listas_info = cursor.fetchall()
            print(listas_info)
        print("la obtencion de la id_lista ha sido un exito")
        listas = {
            'id_lista': listas_info[0],
            'nombre_lista': listas_info[1]  
        }
        
        return listas
    except Exception as ex:
        print (f"Error al obtener lista: {str(ex)}")
        return None
    

        
def hacer_lista(id_usuario, nombre_lista): #YA ESTA HECHO SOLO QUE EL STORE PROCEDURE NO HACE NADA
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"EXEC CrearCarrito {id_usuario}, {nombre_lista}")
        print("la lista ha sido creada un exito")
        return "si"
    except Exception as ex:
        print (f"Error al craear lista: {str(ex)}")
        return None
    