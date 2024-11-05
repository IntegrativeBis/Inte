#donde realizaremos todos los querys de db
#import User
from db import dbconnection
#@classmethod
def login(telefono, password):
    try:
        with dbconnection.cursor() as cursor: #para que el cursor se cierre automaticamente
            cursor.execute("EXEC sp_ConsultarUsuario ?, ?", (telefono, password))
            row_login = cursor.fetchall()
        print(row_login) #intente meter los datos arrojados a un string para poder utilizarlos mas tarde e imprimirlos
    except Exception as ex:
        raise Exception(f"Error al ejecutar Login para el usuario {telefono}: {str(ex)}") #f es para poder colocar variables dentro del string mas facil

def user_register(nombre, apellido, telefono, correo):
    try:
        with dbconnection.cursor() as cursor:
            cursor.execute("EXEC sp_CrearUsuario ?, ?, ?, ?", (nombre, apellido, telefono, correo))
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
    

    
    
    
    
    
"""if row != None: #esto es la segunda parte del login que salio del video
            user = User(row[0], row[1], row[2], User.Confirm_Password(row[3], user.password), row[4])
            return user
        else:
            return None"""    
    
    
@classmethod
def get_by_id(self, db, id):
    try:
        cursor = db.connection.cursor()
        cursor.execute("EXEC sp ConsultarUsuario ?", (id))
        row = cursor.fetchone()
        if row != None:
            return User(row[0], row[1], None, row[2])
        else:
            return None
    except Exception as ex:
        raise Exception(ex)
