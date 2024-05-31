1. Levantar base de datos
`mongod --dbpath /data/db --logpath /var/log/mongodb/mongod.log`
2. Levantar servidor 
`ngrok http 5000`
3. Aplicacion
`python3 app.py`
4. Solicitudes

- Acceso
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password"}' https://8f7c-190-221-146-98.ngrok-free.app/login

- Fectch data
curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNzE4NjEzNywianRpIjoiMDQwN2Q1YjEtMzBmMi00ODQxLWJlMGQtYzU0NTczNGZlZGYwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzE3MTg2MTM3LCJjc3JmIjoiNDk0NGFhMjItZWE0ZS00OWRhLTg0ZDctZTViZDM3ZTBjZjE0IiwiZXhwIjoxNzE3MTg3MDM3fQ.uderQH0_pB4Iw0hEkRWgp1iEobQPo5P-0mn11fw6zE8" https://8f7c-190-221-146-98.ngrok-free.app/fetch-data

- Obtener la data encriptada
curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNzE4NjEzNywianRpIjoiMDQwN2Q1YjEtMzBmMi00ODQxLWJlMGQtYzU0NTczNGZlZGYwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzE3MTg2MTM3LCJjc3JmIjoiNDk0NGFhMjItZWE0ZS00OWRhLTg0ZDctZTViZDM3ZTBjZjE0IiwiZXhwIjoxNzE3MTg3MDM3fQ.uderQH0_pB4Iw0hEkRWgp1iEobQPo5P-0mn11fw6zE8" https://8f7c-190-221-146-98.ngrok-free.app/usuarios

5. Chequar BD
mongo
use security-challenge
db.usuarios.find().pretty()