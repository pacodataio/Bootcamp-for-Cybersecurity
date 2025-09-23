import sys #Nos permite acceder a los argumentos de la línea de comandos (sys.argv).
import socket #Para abrir conexiones TCP a los servidores WHOIS (puerto 43).
import re #Para usar expresiones regulares y extraer el Registrar: de la respuesta.
import time
from concurrent.futures import ThreadPoolExecutor, as_completed #parallel lookups.  more modern that the classic threading is upper layer over threading

# Diccionario de servidores WHOIS por TLD
WHOIS_SERVERS = {
    "com": "whois.verisign-grs.com",
    "net": "whois.verisign-grs.com",
    "org": "whois.pir.org",
    "io": "whois.nic.io",
    "es": "whois.nic.es",
    "app": "whois.nic.google"
}

def get_whois_server(domain):
    tld = domain.split(".")[-1].lower()
    return WHOIS_SERVERS.get(tld, "whois.iana.org")  # genérico si no está en el diccionario

def whois_query(domain, server, port=43):
    time.sleep(2)
    # Conecta al servidor WHOIS y devuelve la información completa
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    s.send((domain + "\r\n").encode("utf-8"))
    
    response = b""
    while True:
        data = s.recv(4096)
        if not data:
            break
        response += data
    s.close()
    return response.decode("utf-8", errors="ignore")

def extract_registrar(whois_data):
    match = re.search(r"Registrar:\s*(.*)", whois_data, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Registrar not found"

def  process_domain(domain):
    #print(f"Looking up {domain}...")
    server = get_whois_server(domain)
    try:
        data = whois_query(domain, server)
        registrar = extract_registrar(data)
    except socket.gaierror:
        registrar = "Servidor WHOIS no encontrado"
    
    print(f"{domain}: {registrar}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python whois_lookup.py domain1 [domain2 ...]")
        print("  python whois_lookup.py -f input.txt")
        sys.exit(1)
    
    if sys.argv[1] == "-f":
        filename = sys.argv[2]
        with open(filename, "r", encoding="utf-8") as f:
            domains = [line.strip() for line in f if line.strip()]
    else:
        domains = sys.argv[1:]

   # Usar ThreadPoolExecutor para paralelizar
    max_threads = 5  # Limitar número de hilos simultáneos
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(process_domain, domain) for domain in domains]

        # Procesar resultados a medida que terminan
        for future in as_completed(futures):
            future.result()  # Captura posibles excepciones
    

if __name__ == "__main__":
    main()
