from flask import Flask, render_template, request, redirect, url_for, flash
from database.DevelopmentConfig import config, DevelopmentConfig #ME DA UN ERROR NO SE PORQUEEEEE
import pyodbc
from flask_login import Login_manager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect #descargar el flask wtf
#MOdels
from models.entities.ModelUser import ModelUser

#Entities
from models.entities.User import User 


app=Flask(__name__)

csrf=CSRFProtect()
db=pyodbc.connect(DevelopmentConfig.connection) #dentro de esto la viene la conexion con la base
login_manager_app=Login_manager(app)




@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)




@app.route ('/') #es la ruta raiz 
def index():
        return redirect(url_for('login')) #nos va a redireccionar a la ruta login
    
    
    
    
    
    
@app.route ('/login', methods=['GET' , 'POST'])
def login():
    if request.method=='POST': #si hicimos la socitud previamente realizada
        #print(request.form['username']) #los datos que haya colocado se imrpimiran aqui
        #print(request.form['password'])
        user=User(0, request.form['username'], request.form['password'])
        logged_user=ModelUser.login(db,user) #saldra la instancia del usuario
        
        if logged_user!=None: #si hay datos en usuario registrado avanzamo
            
            if logged_user.password: #eso es verdadero
                login_user(logged_user) #se ingresa el usuario logeado y se almacena esto lo importamos
                return redirect(url_for(home))
            
            else:
                flash("invalid password")
                return render_template('auth/login.html')
            
        else: # si no hay datos te vas al login pq no encontramos tu usuario
            flash("User not found")
        return render_template('auth/login.html')

    else: #como sera metodo get pues se ejecutara esto
        return render_template('auth/login.html')
    
    
    
    
@app.route('/logout') #aqui se hara un boton en la ppagina para deslogearte estoy hablando en html aqui ya no
def logout():
    logout_user()
    return redirect(url_for('login'))
    
    
    
    
    
@app.route('/home') #te lleva al home si ya estas registrado
def home():
    cursor = db.cursor()
    cursor.execute("SELECT")
    Result = cursor.fetchall()
    #convertir datos a diccionario EJEMPLO
    InsertedObjects = []
    columnNames = [column[0] for column in cursor.description]
    for record in Result:
        InsertedObjects.append(dict(zip(columnNames, record)))
    
    cursor.close()
    return render_template('home.html', data=InsertedObjects)


#ruta para guardar usuarios en la bdd
@app.route('/user', methods=['POST'])
def AddUser():
    username = request.form('username')
    password = request.form('password')
   
    if username and password:
        cursor = db.cursor()
        SQL = "INSERT INTO user (username, password) VALUES (%s, %s)"
        data = (username, password)
        cursor.execute(SQL,data)
        db.commit()
    return redirect(url_for('home'))
    

@app.route('/protected') #hicimos una ruta donde te llevara a la pagina protegida solo si estas registrado
@login_required
def protected():
        return "<h1> esta es una vista protegida solo para usuarios </h1>"

def status_401(error): #se encuentra el error de que el usuario no esta logeado y te manda otravez al login
    return redirect(url_for('login'))

def status_404(error): #
    return "<h1>pagina no encontrada</h1>"


if (__name__)=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401) #cada vez que se encuentre el error te arrojara la funcion con ese errror
    app.register_error_handler(404, status_404)
    app.run()