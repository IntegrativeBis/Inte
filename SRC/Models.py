#donde realizaremos todos los querys de db
import User
@classmethod
def login(self, db, user):
    try:
        cursor = db.connection.cursor()
        
        cursor.execute("EXEC sp_ConsultarUsuario ?", (user.telefono))
        row = cursor.fetchone()
        if row != None:
            user = User(row[0], row[1], row[2], User.Confirm_Password(row[3], user.password), row[4])
            return user
        else:
            return None
    except Exception as ex:
        raise Exception(ex)
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
