from flask import Flask, render_template, request, redirect, url_for, flash, Response, session, jsonify
#from db import dbconnection
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect 
import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from DbModels import login, user_register, get_by_id
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

#API_KEYMaps = 'AIzaSyBpT4O929acaKiKmxevg9hl8sjanWnnOW0' #App de gogke maps

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
                #session[''] hay que ver como guardar al usuario
                estado = "Correct"
                return render_template('/Inicio_CS.html')
            else:
                estado = "Incorrect"
        except Exception as e:
            print(e)
    #print ([0][1]) #se imprpimira el telefono
    return render_template('Inicio_CS.html', data = data, estado = estado)
        
            
    
#@login_manager.user_loader 
def load_user(id):
    return get_by_id(id)
        
#ya estamos iniciados
@app.route('/Inicio_CS') #hicimos una ruta donde te llevara a la pagina protegida solo si estas registrado
@login_required
def logged():
    return "<h1> esta es una vista protegida solo para usuarios </h1>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('IniciarSesion'))

@app.route ('/registrar', methods=['GET', 'POST'])
def registar():
    if request.method == 'POST':
    #estado = "Introduce data"
    #data={} #quien ba a recopilar la info
        nombre=request.args.get ("nombre")
        apellido=request.args.get ("apellido")
        telefono=request.args.get ("telefono")
        password=request.args.get ("password")
        try:
            user_register(nombre, apellido, telefono, password)
            mensaje = "REGISTRO EXITOSO"
            return render_template('Iniciar_sesion.html', mensaje = mensaje)
        except Exception as e:
            print(e)
            mensaje = "ERROR AL REGISTRAR. POR FAVOR INTENTA DE NUEVO."
            return render_template('Registrar.html', mensaje = mensaje)
        
"""
#este es el acceso para registrarnos
@app.route ('/Registrar', methods= ["GET", "POST"]) 
def registro(): 
    if request.method == 'POST':    
        nombre = request.form['txtNombre']
        celular = request.form['txtNumeroCel'] #obligatorio
        correo = request.form['txtCorreo'] #puede ser nulo
        password = generate_password_hash(request.form['txtPassword'])
        apellido = request.form['txtApellido']
        #Apm = request.form['txtApellidoM']
        #Ubi = request.form['txtUbicacion']

        # Verificar si el correo ya está registrado
        cursor = dbconnection.cursor()
        cursor.execute("SELECT * FROM usuario WHERE Celular = ?", (celular,))
        usuario_existente = cursor.fetchone()  # Si hay un resultado, significa que el correo ya está registrado

        if usuario_existente:
            # Si ya existe, devolver al formulario con un mensaje de error
            return render_template('Registrar.html', error="Este Celular ya está registrado.")
        
        # Si no existe, insertar el nuevo usuario
        #cursor.execute("INSERT INTO usuario (Nombre, correo, password, apm, app, ciudad) VALUES (?, ?, ?, ?, ?, ?)", (Nombre, Celular, Correo, Password, Apellido))
 
        
    return redirect(url_for('IniciarSesion', mensajito="usuario correctamente registrado"))
"""

if (__name__)=='__main__':
    #csrf.init_app(app)
    app.run(debug=True) #aqui podrias agregar el host y el puerto al que se quiere conectar y no se que threaded