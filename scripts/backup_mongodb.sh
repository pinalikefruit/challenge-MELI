#!/bin/bash

# Variables de configuración
DB_NAME="security-challenge"
OUTPUT_DIR="/home/tu_usuario/backups"
DATE=$(date +%Y%m%d%H%M%S)
MONGO_HOST="localhost"
MONGO_PORT="5000"
MONGO_USERNAME="tu_usuario"    # Si tu base de datos requiere autenticación
MONGO_PASSWORD="tu_contraseña" # Si tu base de datos requiere autenticación

# Crear directorio de backup si no existe
mkdir -p $OUTPUT_DIR

# Ejecutar mongodump para crear el backup
mongodump --host $MONGO_HOST --port $MONGO_PORT --username $MONGO_USERNAME --password $MONGO_PASSWORD --db $DB_NAME --out $OUTPUT_DIR/backup_$DATE

# Eliminar backups antiguos (más de 7 días)
find $OUTPUT_DIR -type d -mtime +7 -exec rm -rf {} \;
