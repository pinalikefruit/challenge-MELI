from cryptography.fernet import Fernet

# Generación de Claves: Asegúrate de que las claves de cifrado se generan de manera segura y son de suficiente longitud (al menos 256 bits para Fernet).
# Almacenamiento de Claves: Las claves deben almacenarse de manera segura, por ejemplo, en un hardware security module (HSM) o un sistema de gestión de claves seguro (KMS), como AWS KMS, Azure Key Vault, o Google Cloud KMS.

# Generar una nueva clave
encryption_key = Fernet.generate_key()
print(encryption_key.decode()) 