# Importamos librerías necesarias
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64

# Diccionario para guardar las API Keys en memoria
store = {}

# Pedimos contraseña maestra al inicio
master_password = input("Introduce tu contraseña maestra: ").encode()  # la usamos como bytes

# Función para derivar la clave a partir de la contraseña y salt
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password)  # devuelve bytes (clave segura)

# Función para guardar API Key
def store_api_key(service_name, api_key):
    salt = os.urandom(16)  # generamos un salt único
    key = derive_key(master_password, salt)  # derivamos clave de la contraseña
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # nonce aleatorio para AES-GCM
    ct = aesgcm.encrypt(nonce, api_key.encode(), None)  # ciframos la API Key
    # Guardamos en memoria
    store[service_name] = {
        "ciphertext": base64.b64encode(ct).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "salt": base64.b64encode(salt).decode()
    }
    print(f"API Key para '{service_name}' guardada correctamente.\n")

# Función para recuperar API Key
def retrieve_api_key(service_name):
    if service_name not in store:
        print(f"No se encontró ninguna API Key para '{service_name}'.\n")
        return
    entry = store[service_name]
    # Convertimos de base64 a bytes
    ct = base64.b64decode(entry["ciphertext"])
    nonce = base64.b64decode(entry["nonce"])
    salt = base64.b64decode(entry["salt"])
    key = derive_key(master_password, salt)  # derivamos la clave de nuevo
    aesgcm = AESGCM(key)
    try:
        api_key = aesgcm.decrypt(nonce, ct, None).decode()
        print(f"La API Key de '{service_name}' es: {api_key}\n")
    except:
        print("Error: contraseña maestra incorrecta o datos corruptos.\n")

# Menú principal
def menu():
    while True:
        print("Opciones:")
        print("1) Guardar API Key")
        print("2) Recuperar API Key")
        print("3) Salir")
        choice = input("Elige una opción: ").strip()
        if choice == "1":
            service_name = input("Nombre del servicio: ").strip()
            api_key = input("API Key: ").strip()
            store_api_key(service_name, api_key)
        elif choice == "2":
            service_name = input("Nombre del servicio: ").strip()
            retrieve_api_key(service_name)
        elif choice == "3":
            print("Saliendo...")
            break
        else:
            print("Opción inválida. Intenta de nuevo.\n")

# Ejecutamos el menú
if __name__ == "__main__":
    menu()
