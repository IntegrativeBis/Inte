from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_wtf.csrf import CSRFProtect 
import secrets
from DbModels import login, register_user, modify_user, delete_user, buscar_productos, modify_password
app = Flask('__name__', template_folder="SRC/templates", static_folder="SRC/static") # no es necesario pq la carpeta se llama asi y jinja busca esa por defecto


#INVENTAMOS UNA LLAVE SECRETA ALEATORIA
secret_key = secrets.token_hex(16)
#ASIGNAMOS LA LLAVE SECRETA A LA APP
app.secret_key = secret_key
#csrf=CSRFProtect()

@app.route('/')
def index():
    #return redirect(url_for('inicio_ss'))
    return render_template('inicio_ss.html')

@app.route ('/inicio_ss', methods = ['GET'])
def inicio_ss():
    termino = request.args.get('q', '')  # Toma el parámetro 'q' de la URL
    buscar_productos(termino)
    
    return render_template('inicio_ss.html')
 
#INICIARSESION RUTA
@app.route ('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    mensaje = "Introduce celular y contraseña"
    #data={} #quien ba a recopilar la info
    celular=request.form.get ("celular")
    contrasena=request.form.get ("contrasena")
    print(celular, contrasena)
    if celular and contrasena is not None:
        try:
            print("voy a usar la funcion LOGIN")
            usuario = login(celular, contrasena)
            session['cel'] = celular #hay que ver como guardar al usuario
            session['name'] = usuario[0]
            session['apellido'] = usuario[1]
            print(session, usuario[0], usuario[1])
            mensaje = "Correct"
            return redirect(url_for('inicio_cs'))
            return render_template('/inicio_cs.html', usuario = usuario)
        except Exception as e:
                print(f"Error de login (routes): {e}" )
                mensaje = "Celular o Contraseña incorrectas"
    return render_template('iniciar_sesion.html', mensaje = mensaje)
        
@app.errorhandler(404)
def err_handler(e):
    return render_template('error_404.html')
    
#ya estamos iniciados
@app.route('/inicio_cs') 
def inicio_cs(): 
    if 'cel' in session: 
        return render_template('inicio_cs.html', usuario=session)
    return render_template('error_404.html')
    

@app.route('/cuenta')
def cuenta():
    return render_template('cuenta.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio_ss'))

@app.route ('/registrar', methods=['GET', 'POST'])
def registrar():
    mensaje = None
    print ("voy a hacer el request POST")
    if request.method == 'POST':
        nombre=request.form.get ("nombre")
        apellido=request.form.get ("apellido")
        celular=request.form.get ("celular")
        contrasena=request.form.get ("contrasena")
        confirmar_contrasena=request.form.get("confirmar_contrasena")
        print(f"Nombre: {nombre} \nApellido: {apellido} \ncelular: {celular} \nPassword: {contrasena} \nConfirmed_Password: {confirmar_contrasena}")
        if contrasena != confirmar_contrasena:
            mensaje = "Las contraseñas no coinciden"
            return render_template('registrar.html', mensaje = mensaje)   
        try:
            register_user(nombre, apellido, celular, contrasena)
            mensaje = "REGISTRO EXITOSO"
            return render_template('iniciar_sesion.html', mensaje = mensaje)
        except Exception as e:
            print(e)
            mensaje = "ERROR AL REGISTRAR. POR FAVOR INTENTA DE NUEVO."
    return render_template('registrar.html', mensaje = mensaje)   

@app.route ('/listas')
def listas():
    return render_template("listas.html")

@app.route ('/busqueda_cs')
def busqueda_cs():
    return render_template('busqueda_cs.html')

@app.route ('/busqueda_ss')
def busqueda_ss():
    return render_template('busqueda_ss.html')

@app.route ('/producto_ss')
def producto_ss():
    return render_template('producto_ss.html')

@app.route ('/producto_cs')
def producto_cs():
    return render_template('producto_cs.html')

"""if "user" in session: """

if (__name__)=='__main__':
    #csrf.init_app(app)
    app.run(debug=True) #aqui podrias agregar el host y el puerto al que se quiere conectar y no se que threaded