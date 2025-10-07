import mysql.connector
from mysql.connector import Error
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
import json

# Nombre de archivo de fallback
FILE_FALLBACK = "secrets.json"

# Intentar conectar a MySQL
use_mysql = False
try:
    db = mysql.connector.connect(
        host="localhost",
        user="tu_usuario",
        password="tu_contraseña",
        database="secrets_manager"
    )
    cursor = db.cursor()
    # Crear tabla si no existe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS api_keys (
        id INT AUTO_INCREMENT PRIMARY KEY,
        service_name VARCHAR(255) UNIQUE NOT NULL,
        salt VARCHAR(255) NOT NULL,
        nonce VARCHAR(255) NOT NULL,
        ciphertext TEXT NOT NULL
    )
    """)
    db.commit()
    use_mysql = True
    print("Conexión a MySQL establecida.\n")
except Error as e:
    print("No se pudo conectar a MySQL. Se usará almacenamiento en archivo.")
    store_file = {}
    # Cargar archivo si existe
    if os.path.exists(FILE_FALLBACK):
        with open(FILE_FALLBACK, "r", encoding="utf-8") as f:
            store_file = json.load(f)

# Pedimos contraseña maestra
master_password = input("Introduce tu contraseña maestra: ").encode()

# Función para derivar clave
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return kdf.derive(password)

# Guardar API Key
def store_api_key(service_name, api_key):
    salt = os.urandom(16)
    key = derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, api_key.encode(), None)
    salt_b64 = base64.b64encode(salt).decode()
    nonce_b64 = base64.b64encode(nonce).decode()
    ct_b64 = base64.b64encode(ct).decode()

    if use_mysql:
        cursor.execute("""
        INSERT INTO api_keys (service_name, salt, nonce, ciphertext)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            salt=%s, nonce=%s, ciphertext=%s
        """, (service_name, salt_b64, nonce_b64, ct_b64, salt_b64, nonce_b64, ct_b64))
        db.commit()
    else:
        store_file[service_name] = {
            "salt": salt_b64,
            "nonce": nonce_b64,
            "ciphertext": ct_b64
        }
        with open(FILE_FALLBACK, "w", encoding="utf-8") as f:
            json.dump(store_file, f, indent=4)
    print(f"API Key para '{service_name}' guardada correctamente.\n")

# Recuperar API Key
def retrieve_api_key(service_name):
    if use_mysql:
        cursor.execute("SELECT salt, nonce, ciphertext FROM api_keys WHERE service_name=%s", (service_name,))
        result = cursor.fetchone()
        if not result:
            print(f"No se encontró ninguna API Key para '{service_name}'.\n")
            return
        salt_b64, nonce_b64, ct_b64 = result
    else:
        if service_name not in store_file:
            print(f"No se encontró ninguna API Key para '{service_name}'.\n")
            return
        entry = store_file[service_name]
        salt_b64 = entry["salt"]
        nonce_b64 = entry["nonce"]
        ct_b64 = entry["ciphertext"]

    # Decodificar y descifrar
    salt = base64.b64decode(salt_b64)
    nonce = base64.b64decode(nonce_b64)
    ct = base64.b64decode(ct_b64)
    key = derive_key(master_password, salt)
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

# Ejecutar programa
if __name__ == "__main__":
    menu()
    if use_mysql:
        cursor.close()
        db.close()
