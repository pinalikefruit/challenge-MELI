# Security Challenge 2022

## Descripción de la Aplicación
Esta aplicación es una API diseñada para manejar de manera segura la recepción, almacenamiento y distribución de información sensible de los clientes obtenida a través de un endpoint externo. Utiliza Flask como framework de servidor, MongoDB para el almacenamiento de datos y cifrado de datos sensibles con Fernet para garantizar la seguridad durante el tránsito y el almacenamiento.

### Supuestos
- La API maneja datos sensibles y debe garantizar la seguridad en todos los estados.
- La información sensible debe estar cifrada en todo momento, excepto durante el procesamiento en memoria.

### Problemas y Soluciones
- **Problema**: Riesgo de exposición de datos sensibles durante el tránsito.
  - **Solución**: Cifrado de datos sensibles antes de su almacenamiento y aseguramiento de las comunicaciones con TLS.
- **Problema**: Necesidad de acceder a diferentes tipos de datos según el departamento de la empresa.
  - **Solución**: Implementación de roles en JWT que limitan el acceso a los datos según las necesidades del departamento.

### Evidencias
![](path_to_screenshot.png)
*Captura de pantalla del funcionamiento de la API.*

## Instrucciones de Ejecución

### Requisitos Previos
- Python 3.8 o superior
- MongoDB
- Dependencias de Python listadas en `requirements.txt`

### Instalación de Dependencias
Instalar las dependencias necesarias ejecutando:
```bash
pip install -r requirements.txt
```

### Configuración de Variables de Entorno
Configurar el archivo `.env.example` a archivo .env en el directorio raíz del proyecto y actualizar las siguientes variable:

* `JWT_SECRET_KEY`: Clave secreta para JWT.
* `MONGO_URI`: URI de conexión a MongoDB.
* `ENCRYPTION_KEY`: Clave para el cifrado Fernet.

### Ejecución de la Aplicación
Ejecutar la aplicación con:

```
python app.py
```


## Comunicación con la API
### Acceso
Para obtener un token de acceso:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username":"admin","password":"password"}' https://d46c-190-221-146-98.ngrok-free.app/login
```

### Fetch Data
Para obtener y almacenar datos desde el proveedor externo:

```bash
curl -X GET -H "Authorization: Bearer <your_token>" https://d46c-190-221-146-98.ngrok-free.app/fetch-data
```

### Obtener la Data Encriptada
Para obtener todos los datos de usuarios encriptados:

```bash
curl -X GET -H "Authorization: Bearer <your_token>" https://d46c-190-221-146-98.ngrok-free.app/usuarios/
```

Para obtener datos de un usuario específico por ID:
```bash
curl -X GET -H "Authorization: Bearer <your_token>" https://d46c-190-221-146-98.ngrok-free.app/usuarios/<ID>
```

### Uso en Postman
1. Acceso:

* Método: POST
* URL: https://d46c-190-221-146-98.ngrok-free.app/login
* Body:
```json
{
  "username": "admin",
  "password": "password"
}
```
* Enviar la solicitud para obtener el token.

2. Fetch Data:

* Método: GET
* URL: https://d46c-190-221-146-98.ngrok-free.app/fetch-data
* Headers:
Key: Authorization
Value: Bearer <your_token>

3. Obtener la Data Encriptada:

* Método: GET
* URL: https://d46c-190-221-146-98.ngrok-free.app/usuarios/
* Headers:
Key: Authorization
Value: Bearer <your_token>


4. Obtener Datos de Usuario Específico:

* Método: GET
* URL: https://d46c-190-221-146-98.ngrok-free.app/usuarios/1
* Headers:
Key: Authorization
Value: Bearer <your_token>


### Análisis de Riesgo de la Solución Planteada

* *Riesgo de filtración de datos*: Alto. Si las claves de cifrado son expuestas. Se recomienda rotar regularmente las claves y almacenarlas de manera segura.
* *Riesgo de acceso no autorizado*: Medio. Aunque se utiliza JWT para la autenticación, la configuración y manejo de los tokens debe ser rigurosa para evitar explotaciones.
* *Riesgo de ataques de inyección*: Bajo. Se utiliza validación de esquemas para evitar inyecciones no deseadas en la base de datos.

#### Arquitectura de la Aplicación

Diagrama de arquitectura mostrando cómo los componentes interactúan entre sí y con los servicios externos.

![Imagen](/image.png)

Explicación del Diagrama:

* Proveedor Externo: Fuente de datos externa que proporciona la información de los usuarios. 
* Aplicación de Consumo de Datos: Tu aplicación que consume los datos desde el proveedor externo.
* Base de Datos Segura: Almacena los datos cifrados y procesados de manera segura.
* Aplicaciones Internas: Aplicaciones dentro de la empresa que consumen los datos a través de la API REST


Este README proporciona una guía completa sobre cómo configurar y utilizar la aplicación, incluyendo ejemplos de cómo los diferentes departamentos pueden interactuar con la API utilizando `curl` y Postman.
