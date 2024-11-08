#donde realizaremos todos los querys de db
#import User
from db import dbconnection
from werkzeug.security import check_password_hash, generate_password_hash
def login(telefono, password):
    try:
        
        with dbconnection.cursor() as cursor: #para que el cursor se cierre automaticamente
            cursor.execute("EXEC sp_ConsultarUsuario ?, ?", (telefono, check_password_hash(password)))
            row_login = cursor.fetchall()
        print(row_login) #intente meter los datos arrojados a un string para poder utilizarlos mas tarde e imprimirlos
    except Exception as ex:
        raise Exception(f"Error al ejecutar Login para el usuario {telefono}: {str(ex)}") #f es para poder colocar variables dentro del string mas facil

def user_register(nombre, apellido, telefono, hashed_password):
    try:
        with dbconnection.cursor() as cursor:
            cursor.execute("EXEC sp_CrearUsuario ?, ?, ?, ?", (nombre, apellido, telefono, hashed_password))
        print("Registro completado con éxito")
        return True  # Indica que el registro fue exitoso
    except Exception as ex:
        print(f"Error al registrar usuario: {str(ex)}")
        return False  

        
def deleteUser (nombre, apellido, telefono, correo):
    try:
        with dbconnection.cursor() as cursor:
            cursor.execute("EXEC sp_EliminarUsuario ?, ?, ?, ?", (nombre, apellido, telefono, correo))
        print("El usuario ha sido eliminado con exito")
    except Exception as ex:
        print (f"Error al eliminar el usuario: {str(ex)}")
        
def modifyUser (nombre, apellido, telefono, correo):
    try:
        with dbconnection.cursor() as cursor:
            cursor.execute("EXEC sp_EliminarUsuario ?, ?, ?, ?", (nombre, apellido, telefono, correo))
        print("El usuario ha sido modificado con exito")
    except Exception as ex:
        print (f"Error al modificar el usuario: {str(ex)}")
    
"""
connection = dbconnection()
if connection:
    print("La conexión fue establecida correctamente.")
    # Cierra la conexión cuando termines
    connection.close()
    print("Conexión cerrada correctamente.")
else:
    print("No se pudo establecer la conexión a la base de datos.")    
    
    """