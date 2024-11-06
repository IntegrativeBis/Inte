from flask import Flask, render_template, request, redirect, url_for, session, jsonify
#from db import dbconnection
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect 
import secrets
from werkzeug.security import generate_password_hash
from DbModels import login, user_register
from User import User
app = Flask('__name__', template_folder="SRC/templates") # no es necesario pq la carpeta se llama asi y jinja busca esa por defecto
#login_manager = LoginManager()
#login_manager.init_app(app) #enlazamos con la app
#login_manager.login_view = 'IniciarSesion' #si el usuario intenta entrar a una vista protegida te redirige a esto
#login_manager.login_message = "Inicie sesion para acceder a este contenido"

#INVENTAMOS UNA LLAVE SECRETA ALEATORIA
secret_key = secrets.token_hex(16)
#ASIGNAMOS LA LLAVE SECRETA A LA APP
app.secret_key = secret_key
#csrf=CSRFProtect()

@app.route ('/')
def Inicio():
    return render_template("Inicio_SS.html")
    #return redirect(url_for('IniciarSesion'))
#INICIARSESION RUTA
@app.route ('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    estado = "Introduce data"
    data={} #quien ba a recopilar la info
    telefono=request.args.get ("telefono")
    password=request.args.get ("password")
    
    if telefono and password:
        try:
            user = login(telefono, password)
            if user:
                usuario = session['user'] #hay que ver como guardar al usuario
                estado = "Correct"
                return render_template('/Inicio_CS.html', usuario = usuario)
            else:
                estado = "Incorrect"
        except Exception as e:
            print(e)
    #print ([0][1]) #se imprpimira el telefono
    return render_template('Inicio_CS.html', data = data, estado = estado)
        
@app.errorhandler(404)
def err_handler(e):
    return render_template('error_404.html')
    
      
"""#@login_manager.user_loader 
def load_user(id):
    return get_by_id(id)
    """    

        
#ya estamos iniciados
@app.route('/Inicio_CS') #hicimos una ruta donde te llevara a la pagina protegida solo si estas registrado
def Inicio_CS():
    
    return "<h1> esta es una vista protegida solo para usuarios </h1>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('IniciarSesion'))

@app.route ('/Registrar', methods=['GET', 'POST'])
def registrar():
    user ={ #idk si esto debe estar dentro del IF
        'nombre': '',
        'apellido':'',
        'telefono':'',
        } #quien ba a recopilar la info
    mensaje = None
    
    if request.method == 'POST':
        user['nombre']=request.form.get ("nombre")
        user['apellido']=request.form.get ("apellido")
        user['telefono']=request.form.get ("telefono")
        password=request.form.get ("password")
        session['user'] = user
 
        hashed_password=generate_password_hash (password)
        try:
            user_register(user['nombre'], user['apellido'], user['telefono'], hashed_password)
            mensaje = "REGISTRO EXITOSO"
            return render_template('Iniciar_sesion.html', mensaje = mensaje)
        except Exception as e:
            print(e)
            mensaje = "ERROR AL REGISTRAR. POR FAVOR INTENTA DE NUEVO."
            return render_template('Registrar.html', mensaje = mensaje)
    return render_template('Registrar.html', mensaje = mensaje)   

"""if "user" in session: """

if (__name__)=='__main__':
    #csrf.init_app(app)
    app.run(debug=True) #aqui podrias agregar el host y el puerto al que se quiere conectar y no se que threaded