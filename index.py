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



