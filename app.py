from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from pymongo import MongoClient
from cryptography.fernet import Fernet
import requests
import os
from dotenv import load_dotenv
from cerberus import Validator
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Asegúrate de que esta línea carga la clave correctamente
jwt = JWTManager(app)

client = MongoClient(os.getenv('MONGO_URI'))
db = client['security-challenge']
collection = db['usuarios']

encryption_key = os.getenv('ENCRYPTION_KEY')
cipher_suite = Fernet(encryption_key.encode())

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
    try:
        datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return True
    except ValueError:
        return False

def encrypt_data(data):
    encrypted_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            encrypted_value = 'ENC:' + cipher_suite.encrypt(value.encode()).decode()
            encrypted_data[key] = encrypted_value
            logger.info(f"Encrypted {key}: {encrypted_value}")
        else:
            encrypted_data[key] = value
    return encrypted_data

def decrypt_data(data):
    decrypted_data = {}
    for key, value in data.items():
        if isinstance(value, str) and value.startswith('ENC:'):
            try:
                decrypted_value = cipher_suite.decrypt(value[4:].encode()).decode()
                decrypted_data[key] = decrypted_value
                logger.info(f"Decrypted {key}: {decrypted_value}")
            except (ValueError, TypeError, cryptography.fernet.InvalidToken) as e:
                decrypted_data[key] = value
                logger.error(f"Error decrypting {key}: {e}")
        else:
            decrypted_data[key] = value
    return decrypted_data

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'admin' or password != 'password':
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
    if response.status_code != 200:
        logger.error(f"Error fetching data: {response.status_code}")
        return jsonify({"msg": "Error fetching data"}), response.status_code
    
    users = response.json()
    logger.info("Fetched users from external API:")
    logger.info(users)

    valid_users = []
    validator = Validator(user_schema)
    for user in users:
        try:
            logger.info(f"Converting user: {user}")
            if not is_valid_iso_date(user['fec_alta']) or not is_valid_iso_date(user['fec_birthday']):
                raise ValueError("Invalid date format")
            user['fec_alta'] = datetime.fromisoformat(user['fec_alta'].replace('Z', '+00:00'))
            user['fec_birthday'] = datetime.fromisoformat(user['fec_birthday'].replace('Z', '+00:00'))
            user['geo_latitud'] = float(user['geo_latitud'])
            user['geo_longitud'] = float(user['geo_longitud'])

            if validator.validate(user):
                encrypted_user = encrypt_data(user)
                logger.info(f"Encrypted user: {encrypted_user}")
                valid_users.append(encrypted_user)
            else:
                logger.warning(f"Validation errors for user {user['id']}: {validator.errors}")
        except (ValueError, KeyError) as e:
            logger.error(f"Error al convertir datos para el usuario {user['id']}: {e}")

    if not valid_users:
        return jsonify({"msg": "No valid users found"}), 400

    logger.info("Inserting encrypted users into MongoDB:")
    for user in valid_users:
        logger.info(user)
    collection.insert_many(valid_users)
    logger.info("Data inserted into MongoDB successfully")
    return 'Data fetched and stored successfully', 200

@app.route('/usuarios', methods=['GET'])
@jwt_required()
def get_usuarios():
    encrypted_users = list(collection.find({}, {'_id': 0}))
    logger.info("Fetched encrypted users from MongoDB:")
    for user in encrypted_users:
        logger.info(user)
    users = [decrypt_data(user) for user in encrypted_users]
    logger.info("Decrypted users:")
    for user in users:
        logger.info(user)
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 5000)), debug=True)
