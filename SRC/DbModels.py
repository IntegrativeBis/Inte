from db import dbconnection
connection = dbconnection()  # Obtenemos la conexión
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
        