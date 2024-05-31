from cryptography.fernet import Fernet

# Generar una nueva clave
encryption_key = Fernet.generate_key()
print(encryption_key.decode()) 