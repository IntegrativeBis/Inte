#AQUI ESTAN LOS IMPORTS QUE REQUERIMOS
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import secrets
from datetime import timedelta
from DbModels import login, register_user, modify_user, delete_user, busqueda_productos_AD, modify_password, busqueda_productos, busqueda_productos_by_id

#AQUI DEFINIMOS LA APP Y LE INSERTAMOS LOS VALORES CORRECPONDIENTES PARA QUE RECONOZCA LAS CARPETAS
app = Flask('__name__', template_folder="SRC/templates", static_folder="SRC/static") 

#ASIGNAMOS LA LLAVE SECRETA A LA APP E INVENTAMOS UNA LLAVE SECRETA ALEATORIA
app.secret_key = secrets.token_hex(16) 

#AQUI SE ENCONTRARAN LAS RUTAS PRINCIPALES-------------------------------------------------------------------------------------
"""
@app.route ('/') #, methods = ['GET']
def inicio_ss():
    termino = request.args.get('q', '').lower()  # Toma el parámetro 'q' de la URL
    print(termino)
    resultados = buscar_productos(termino)
    print (resultados)
    return render_template('inicio_ss.html')
"""
#ya estamos iniciados
@app.route('/') 
def inicio(): 
    if 'cel' in session :
        return render_template('inicio_cs.html', usuario=session)
    #return redirect(url_for('inicio_ss'))
    return render_template('inicio_ss.html')

#AQUI EN ADELANTE SOLO SE VERA LO QUE TENGA QUE VER CON EL USUARIOOOOOO----------------------------------------------------------------

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

#INICIARSESION RUTA
@app.route ('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    mensaje = "Introduce celular y contraseña"
    celular=request.form.get ("celular")
    contrasena=request.form.get ("contrasena")
    print(celular, contrasena)
    if celular and contrasena is not None:
        try:
            print("voy a usar la funcion LOGIN")
            usuario = login(celular, contrasena)
            session['cel'] = celular 
            session['nombre'] = usuario[0]
            session['apellido'] = usuario[1]
            print(session, usuario[0], usuario[1])
            mensaje = "Correct"
            return redirect(url_for('inicio', usuario=usuario))
        except Exception as e:
                print(f"Error de login (routes): {e}" )
                mensaje = "Celular o Contraseña incorrectas"
    return render_template('iniciar_sesion.html', mensaje = mensaje)
    
@app.route('/cuenta')
def cuenta():
    if 'cel' in session:
        return render_template('cuenta.html')
    return pagina_no_encontrada(404)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))

#DE AQUI EN ADELANTE SE ENCUENTRA TODO LO RELACIONADO CON PRODUCTOSSS Y BUSQUEDA-------------------------------------------------------------

@app.route('/buscar_productos') #esta ruta la usa el JS realtime durante se esta buscando producto en la barra buscadora
def buscar_productos():#aqui a medida que la barra se rellene se va a modificar todos los productos de abajo
    termino = request.args.get('q', '').lower()
    # Aquí debería buscar productos en la base de datos
    resultados = busqueda_productos(termino) # HAY QUE MODIFICAR ESTO A BUSQUEDA_PRODUCTOS NORMAL
    print(resultados)
    return jsonify(resultados) #se envian en formato Jaison

@app.route ('/busqueda', methods = ['GET']) #te redirecciona a alguna busqueda con el q que se le fue enviado desde el FORM inicio_ss.html
def busqueda(): 
    termino = request.args.get('q', '').lower() #agarra el argumento y lo hace minuscula
    print(termino)
    if 'cel' in session:
        return render_template('busqueda_cs.html')
    return render_template('busqueda_ss.html')

@app.route ('/producto/<int:id_producto>') #va a tomar el argumento buscado (aqui debe tomar el argumento del producto seleccionado en busqueda NO SE ACERLO) para que te aparezca el producto 
def producto(id_producto): #   DEBERIA DE TOMAR EL ID
    """termino = request.args.get('q', '').lower()
    print(termino)"""
    producto = busqueda_productos_by_id(id_producto)
    print(producto) 
    if 'cel' in session:
        return render_template('producto_cs.html', producto=producto)
    return render_template('producto_ss.html', producto=producto)

@app.route ('/listas')
def listas():
    return render_template("listas.html")



#A PARTIT DE AQUI SON ERRORES Y DEMAS COSAS --------------------------------------------------------------------------------------------------

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('error_404.html'), 404
    
if (__name__)=='__main__':
    #csrf.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes=30)
    app.run(debug=True) #aqui podrias agregar el host y el puerto al que se quiere conectar y no se que threaded