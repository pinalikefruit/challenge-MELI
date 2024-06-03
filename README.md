1. Levantar base de datos
`mongod --dbpath /data/db --logpath /var/log/mongodb/mongod.log`
2. Levantar servidor 
`ngrok http 5000`
3. Aplicacion
`source venv/bin/activate`
`python3 app.py`
4. Solicitudes

- Acceso
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password"}' https://d46c-190-221-146-98.ngrok-free.app/login

- Fectch data
curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNzQyNjEyMSwianRpIjoiOGI2MWFkZWItM2E3NC00MmQ5LTk2Y2MtMTc3NTI3MWNhY2Y2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzE3NDI2MTIxLCJjc3JmIjoiNWEwZGVjY2QtZTRhMy00ODRhLWJjYWMtNmRiYmIzZmYxMzI5IiwiZXhwIjoxNzE3NDI3MDIxfQ.VI7bwr26RQIX8cmhoomxTzYvmQXlKpJUvqbxzuq9FCA" https://d46c-190-221-146-98.ngrok-free.app/fetch-data

- Obtener la data encriptada
curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNzQyNjEyMSwianRpIjoiOGI2MWFkZWItM2E3NC00MmQ5LTk2Y2MtMTc3NTI3MWNhY2Y2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzE3NDI2MTIxLCJjc3JmIjoiNWEwZGVjY2QtZTRhMy00ODRhLWJjYWMtNmRiYmIzZmYxMzI5IiwiZXhwIjoxNzE3NDI3MDIxfQ.VI7bwr26RQIX8cmhoomxTzYvmQXlKpJUvqbxzuq9FCA" https://d46c-190-221-146-98.ngrok-free.app/usuarios/usuarios


- Obtener la data encriptada
curl -X GET -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNzQyNjEyMSwianRpIjoiOGI2MWFkZWItM2E3NC00MmQ5LTk2Y2MtMTc3NTI3MWNhY2Y2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzE3NDI2MTIxLCJjc3JmIjoiNWEwZGVjY2QtZTRhMy00ODRhLWJjYWMtNmRiYmIzZmYxMzI5IiwiZXhwIjoxNzE3NDI3MDIxfQ.VI7bwr26RQIX8cmhoomxTzYvmQXlKpJUvqbxzuq9FCA" https://d46c-190-221-146-98.ngrok-free.app/usuarios/1

5. Chequar BD
mongo
use security-challenge
db.usuarios.find().pretty() 


To Do

* Roles Disponibilidad de datos: establecer el tipo de control, la forma de obtener los datos y los posibles consumidores.
Proporciona API seguras para que otros equipos puedan consumir los datos.
Asegúrate de que solo los usuarios y aplicaciones autorizados puedan acceder a los datos.
al descencriptar, no mostrar las tarjetas de creditos.


* Instrucciones para la ejecución de la aplicación (incluida cualquier aplicación o librería a
instalar para el correcto funcionamiento del programa).
* Descripción de la aplicación realizada, supuestos, problemas y soluciones con los que se
encontró al realizar la misma con evidencias en png.
* Análisis de riesgo de la solución planteada.
* Dockerizar la aplicación.
* Documentación del proceso (Diagrama de clases, Arquitectura, etc)
* Update requirements
* Implementa controles como encriptación de datos en reposo y en tránsito, autenticación multifactor (MFA), y monitoreo continuo para detectar accesos no autorizados.
* Mantén registros detallados de acceso y actividades para auditorías.
* Frontend