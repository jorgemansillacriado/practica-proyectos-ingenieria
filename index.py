from flask import Flask, request, render_template, session, redirect
import pymongo 
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import requests
from bs4 import BeautifulSoup

# Try connecting without SSL verification (use with caution in production!)

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def validar():
    if request.method == 'POST':
        usuario = request.form['login']
        password = request.form['password']
        
        client = MongoClient('mongodb+srv://jarabers:@#####@clusterjorge.uesqo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterJorge', tlsAllowInvalidCertificates=True) # Setting tlsAllowInvalidCertificates to True disables SSL certificate verification
        db = client['travel']
        collection = db['usuarios']
        x = collection.find_one({'login': usuario, 'password': password})
        print (x)
        if x:
            collection= db['destinos']
            x = collection.find({})
            return render_template('home.html', login = usuario, destinos = x)
        else:
            return render_template('login.html',error = True)
        
    return render_template('login.html')
    
@app.route('/chat', methods=['POST'])
def chat():
    mensaje = request.form['mensaje'].lower()

    # Lógica simple del bot
    if "hola" in mensaje:
        respuesta = "¡Hola! ¿En qué puedo ayudarte?"
    elif "viaje" in mensaje:
        respuesta = "Tenemos destinos increíbles. ¿A cuál quieres ir?"
    else:
        respuesta = "Lo siento, no entiendo. ¿Puedes repetirlo?"

    return render_template('home.html', respuesta=respuesta)

@app.route("/detalle",methods=['POST','GET'])
def detalle():
    if request.method == 'POST':
        usuario = request.form["login"]
        destino = request.form["destino"]
        client = MongoClient ('mongodb+srv://jarabers:vzlqOjNzmsBdASty@clusterjorge.uesqo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterJorge', tlsAllowInvalidCertificates=True) 
        db = client['travel']
        collection = db['destinos']
        x = collection.find_one({'nombre':destino})
        print(x)
        #obtengo el destino indicado por el usuario en la BD, por si no existe
        collection2 = db['valoracion']
        
        x2 = collection2.find_one({'usuario':usuario})
        print(x2)
        val = x2['valoraciones'].get(destino,0)
        print(destino)
        print(val)
        return render_template("detalle.html", login=usuario, destino=x, valoracion=val)

@app.route("/actualizar_like",methods=['POST','GET'])
def actualizar_like():
    if request.method == 'POST':
        valor = request.form["value"]
        usuario = request.form["usuario"]
        destino = request.form["destino"]
        client = MongoClient ('mongodb+srv://jarabers:vzlqOjNzmsBdASty@clusterjorge.uesqo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterJorge', tlsAllowInvalidCertificates=True) 
        db = client['travel']
        collection = db['valoracion']
        x = collection.find_one({'usuario':usuario})
        valoracion_nueva = x["valoraciones"]
        print(valoracion_nueva)
        valoracion_nueva[destino] = int(valor)
        print(valoracion_nueva)
        collection.update_one({'usuario':usuario},{"$set":{"valoraciones":valoracion_nueva}})
        return("ok")

"""
@app.route('/scrape')
def scrape():
    url = 'https://news.ycombinator.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titulos = [a.text for a in soup.select('.titleline a')]
    return render_template('scrape.html', titulos=titulos)

"""

if __name__ == '__main__':
    app.run(port=8000,debug=True)



