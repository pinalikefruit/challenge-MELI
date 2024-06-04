from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from pymongo import MongoClient
from cryptography.fernet import Fernet
import requests
import os
from dotenv import load_dotenv
from cerberus import Validator
from datetime import datetime
import logging
from functools import wraps

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

admin_key = os.getenv('ADMIN_SECRET_KEY')
user_key = os.getenv('USER_SECRET_KEY')
bi_key = os.getenv('BI_SECRET_KEY')
marketing_key = os.getenv('MARKETING_SECRET_KEY')
atencion_key = os.getenv('ATENCION_SECRET_KEY')
finanzas_key = os.getenv('FINANZAS_SECRET_KEY')
seguridad_key = os.getenv('SEGURIDAD_SECRET_KEY')

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

users = {
    'admin': {'password': admin_key , 'role': 'admin'},
    'user': {'password': user_key, 'role': 'user'},
    'bi_user': {'password': bi_key, 'role': 'business_intelligence'},
    'marketing_user': {'password': marketing_key, 'role': 'marketing'},
    'atencion_user': {'password': atencion_key, 'role': 'atencion_al_cliente'},
    'finanzas_user': {'password': finanzas_key, 'role': 'finanzas'},
    'seguridad_user': {'password': seguridad_key, 'role': 'seguridad_y_fraude'}
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
        if key in ['credit_card_num', 'credit_card_ccv', 'cuenta_numero', 'direccion', 'foto_dni', 'ip']:
            if isinstance(value, str):
                encrypted_value = 'ENC:' + cipher_suite.encrypt(value.encode()).decode()
                encrypted_data[key] = encrypted_value
                logger.info(f"Encrypted {key}: {encrypted_value}")
            else:
                encrypted_data[key] = value
        else:
            encrypted_data[key] = value
    return encrypted_data

def decrypt_data(data):
    decrypted_data = {}
    for key, value in data.items():
        if key in ['credit_card_num', 'credit_card_ccv', 'cuenta_numero', 'direccion', 'foto_dni', 'ip']:
            # No desencriptar datos sensibles
            decrypted_data[key] = value
        elif isinstance(value, str) and value.startswith('ENC:'):
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

def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims['role'] != role:
                return jsonify({"msg": "Access forbidden: insufficient privileges"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # role = request.json.get('role', None)

    user = users.get(username)
    if not user or user['password'] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    role = user['role']
    access_token = create_access_token(identity=username, additional_claims={"role": role})
    
    return jsonify(access_token=access_token)

@app.route('/')
def home():
    return "Welcome to the Security Challenge API!"

@app.route('/fetch-data', methods=['GET'])
@jwt_required()
@role_required('admin')
def fetch_data():
    url = 'https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios'
    response = requests.get(url, verify=True)
    try:
        response.raise_for_status()
    except requests.exceptions.SSLError as e:
        logger.error(f"Error de SSL: {e}")
        return jsonify({"msg": "SSL Error"}), 500
    except requests.exceptions.HTTPError as e:
        logger.error(f"Error HTTP: {e}")
        return jsonify({"msg": f"HTTP Error: {e}"}), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Error en la solicitud: {e}")
        return jsonify({"msg": "Request Error"}), 500

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
    claims = get_jwt()
    role = claims['role']

    encrypted_users = list(collection.find({}, {'_id': 0}))
    logger.info("Fetched encrypted users from MongoDB:")
    for user in encrypted_users:
        logger.info(user)
    
    decrypted_users = [decrypt_data(user) for user in encrypted_users]
    filtered_users = []
    for user in decrypted_users:
        if role == 'business_intelligence':
            filtered_user = {key: value for key, value in user.items() if key not in ['credit_card_num', 'credit_card_ccv', 'cuenta_numero', 'foto_dni', 'ip']}
        elif role == 'marketing':
            filtered_user = {key: value for key, value in user.items() if key in ['user_name', 'codigo_zip', 'color_favorito', 'cantidad_compras_realizadas', 'geo_latitud', 'geo_longitud']}
        elif role == 'atencion_al_cliente':
            filtered_user = {key: value for key, value in user.items() if key in ['user_name', 'direccion', 'ip', 'cantidad_compras_realizadas', 'auto', 'auto_modelo', 'auto_tipo', 'auto_color']}
        elif role == 'finanzas':
            filtered_user = {key: value for key, value in user.items() if key in ['user_name', 'credit_card_num', 'credit_card_ccv', 'cuenta_numero']}
        elif role == 'seguridad_y_fraude':
            filtered_user = {key: value for key, value in user.items() if key in ['user_name', 'direccion', 'ip', 'foto_dni', 'geo_latitud', 'geo_longitud', 'credit_card_num', 'credit_card_ccv']}
        elif role == 'admin':
            filtered_user = user  # Admin role has access to all data
        else:
            logger.warning(f"Role {role} not authorized to access user data")
            return jsonify({"msg": "Access forbidden: insufficient privileges"}), 403
        filtered_users.append(filtered_user)

    logger.info(f"Filtered user data for role {role}:")
    for user in filtered_users:
        logger.info(user)

    return jsonify(filtered_users), 200

@app.route('/usuarios/<user_id>', methods=['GET'])
@jwt_required()
def get_usuario_by_id(user_id):
    logger.info(f"Fetching user with ID: {user_id}")
    encrypted_user = collection.find_one({'id': user_id}, {'_id': 0})
    if not encrypted_user:
        logger.warning(f"User with ID {user_id} not found")
        return jsonify({"msg": "User not found"}), 404
    decrypted_user = decrypt_data(encrypted_user)
    claims = get_jwt()
    role = claims['role']

    # Filtrar datos según el rol
    if role == 'business_intelligence':
        filtered_user = {key: value for key, value in decrypted_user.items() if key not in ['credit_card_num', 'credit_card_ccv', 'cuenta_numero', 'foto_dni', 'ip']}
    elif role == 'marketing':
        filtered_user = {key: value for key, value in decrypted_user.items() if key in ['user_name', 'codigo_zip', 'color_favorito', 'cantidad_compras_realizadas', 'geo_latitud', 'geo_longitud']}
    elif role == 'atencion_al_cliente':
        filtered_user = {key: value for key, value in decrypted_user.items() if key in ['user_name', 'direccion', 'ip', 'cantidad_compras_realizadas', 'auto', 'auto_modelo', 'auto_tipo', 'auto_color']}
    elif role == 'finanzas':
        filtered_user = {key: value for key, value in decrypted_user.items() if key in ['user_name', 'credit_card_num', 'credit_card_ccv', 'cuenta_numero']}
    elif role == 'seguridad_y_fraude':
        filtered_user = {key: value for key, value in decrypted_user.items() if key in ['user_name', 'direccion', 'ip', 'foto_dni', 'geo_latitud', 'geo_longitud', 'credit_card_num', 'credit_card_ccv']}
    elif role == 'admin':
        filtered_user = decrypted_user  # Admin tiene acceso a todos los datos
    else:
        logger.warning(f"Role {role} not authorized to access this data")
        return jsonify({"msg": "Access forbidden: insufficient privileges"}), 403

    logger.info(f"Filtered user data for role {role}: {filtered_user}")
    return jsonify(filtered_user), 200

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT', 5000)), debug=True)
