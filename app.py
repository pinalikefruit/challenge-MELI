from flask import Flask, jsonify
from pymongo import MongoClient
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = MongoClient(os.getenv('MONGO_URI'))
db = client['security-challenge']
collection = db['usuarios']

@app.route('/')
def home():
    return "Welcome to the Security Challenge API!"

@app.route('/fetch-data', methods=['GET'])
def fetch_data():
    url = 'https://62433a7fd126926d0c5d296b.mockapi.io/api/v1/usuarios'
    response = requests.get(url)
    users = response.json()
    collection.insert_many(users)
    return 'Data fetched and stored successfully', 200

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    users = list(collection.find({}, {'_id': 0}))
    return jsonify(users), 200

if __name__ == '__main__':
    app.run(port=int(os.getenv('PORT')), debug=True)
