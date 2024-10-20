@app.route ('/') #es la ruta raiz 
def index():
        #return redirect(url_for('login')) #nos va a redireccionar a la ruta login
    return redirect(url_for('Inicio_CS'))
    