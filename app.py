from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from pymongo import MongoClient
import requests
import os
from dotenv import load_dotenv
from cerberus import Validator
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Cambia esto por una clave secreta segura
jwt = JWTManager(app)

client = MongoClient(os.getenv('MONGO_URI'))
db = client['security-challenge']
collection = db['usuarios']

# Esquema de validación para los datos de usuario
user_schema = {
    'fec_alta': {'type': 'datetime'},
    'user_name': {'type': 'string'},
    'codigo_zip': {'type': 'string'},
    'credit_card_num': {'type': 'string'},
    'credit_card_ccv': {'type': 'string'},
    'cuenta_numero': {'type': 'string'},
    'direccion': {'type': 'string'},
    'geo_latitud': {'type': 'float'},
    'geo_longitud': {'type': 'float'},
    'color_favorito': {'type': 'string'},
    'foto_dni': {'type': 'string'},
    'ip': {'type': 'string'},
    'auto': {'type': 'string'},
    'auto_modelo': {'type': 'string'},
    'auto_tipo': {'type': 'string'},
    'auto_color': {'type': 'string'},
    'cantidad_compras_realizadas': {'type': 'integer'},
    'avatar': {'type': 'string'},
    'fec_birthday': {'type': 'datetime'},
    'id': {'type': 'string'}
}

def is_valid_iso_date(date_string):
    """ Check if the date string is a valid ISO 8601 date """
    try:
        datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

# Ruta para autenticar usuarios y generar un token JWT
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'admin' or password != 'password':  # Implementar una autenticación real
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route('/')
def home():
    return "Welcome to the Security Challenge API!"

@app.route('/fetch-data', methods=['GET'])
@jwt_required()
def fetch_data():
    url = 'https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios'
    response = requests.get(url)
    users = response.json()
    
    print(users)  # Imprime los datos para depuración

    valid_users = []
    # Validar cada usuario
    validator = Validator(user_schema)
    for user in users:
        try:
            print(f"Converting user: {user}")  # Imprimir datos del usuario antes de la conversión
            if not is_valid_iso_date(user['fec_alta']) or not is_valid_iso_date(user['fec_birthday']):
                raise ValueError("Invalid date format")
            user['fec_alta'] = datetime.fromisoformat(user['fec_alta'].replace('Z', '+00:00'))
            user['fec_birthday'] = datetime.fromisoformat(user['fec_birthday'].replace('Z', '+00:00'))
            user['geo_latitud'] = float(user['geo_latitud'])
            user['geo_longitud'] = float(user['geo_longitud'])
            
            if validator.validate(user):
                valid_users.append(user)
            else:
                print(f"Validation errors for user {user['id']}: {validator.errors}")
        except (ValueError, KeyError) as e:
            print(f"Error al convertir datos para el usuario {user['id']}: {e}")

    if not valid_users:
        return jsonify({"msg": "No valid users found"}), 400

    collection.insert_many(valid_users)
    return 'Data fetched and stored successfully', 200

@app.route('/usuarios', methods=['GET'])
@jwt_required()
def get_usuarios():
    users = list(collection.find({}, {'_id': 0}))
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT')), debug=True)
