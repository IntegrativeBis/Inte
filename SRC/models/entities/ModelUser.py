from .User import User

class ModelUser():
    @classmethod
    def login(self, db, user): #de esta instancia del usuario
        cursor=db.connection.cursor()
        try:
            pyodbc="SELECT id, username, password, fullname FROM user WHERE username = {}".format(user.username) #aqui se obtiene el username
            cursor.execute(pyodbc) #hacemos que sea ejecutado el script
            row=cursor.fetchone() #que sea igual a lo que arrojo
            if row != None: #si hay un usuario
                user=User(row[0], row [1], User.check_password(row[2], user.password), row[3]) #nos arroja la primera linea que da el select o sea que el id, nos arroja el username, revisa si hay password y revisar si el hash esta correcto, finalmente el nombre completo
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self, db, id): #de esta instancia del usuario
        try:
            cursor=db.connection.cursor()
            pyodbc="SELECT id, username, fullname FROM user WHERE id = {}".format(id) #aqui se obtiene el id
            cursor.execute(pyodbc)
            row=cursor.fetchone() #que sea igual a lo que arrojo
            if row != None: #si hay un usuario
                logged_user=User(row[0], row [1], None, row[2]) #nos arroja algo parecido a lo de arriba pero dado a que ya esta registrado el usuario la contrasenia se elminina
                return logged_user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)