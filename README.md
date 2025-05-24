# practica-proyectos-ingenieria
pratica proyectos ingenieria 2 

## he añadido como seguridad variable en la cadena de conexion de mongdb para ello uso la siguiente libreria de python
from dotenv import load_dotenv
import os

meto en .env la cadena de conexion que no la subo a git ya que la meto en .gitignore y la uso en codigo como variable
 client = MongoClient(MONGODB_URI, tlsAllowInvalidCertificates=True) 

## meter los paquetes pip necesarios
pip install -r requirements.txt
## ejecutar el script
python index.py


## Podemos logar en la terminal de python con el siguiente comando
http://localhost:8000

