import sys #Nos permite acceder a los argumentos de la línea de comandos (sys.argv).
import socket #Para abrir conexiones TCP a los servidores WHOIS (puerto 43).
import re #Para usar expresiones regulares y extraer el Registrar: de la respuesta.

def whois_query(domain, server="whois.verisign-grs.com", port=43):
    # Abrir conexión con el servidor WHOIS
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f'S: {s}')
    s.connect((server, port))
    s.send((domain + "\r\n").encode("utf-8"))
    print(f'S: {s}')

    # Recibir respuesta
    response = b""
    num=1
    while True:
        data = s.recv(4096)
        print(f'data{num}: {data} \n')
        if not data:
            break
        response += data
        num=num+1
    s.close()

    return response.decode("utf-8", errors="ignore")

def extract_registrar(whois_data):
    # Buscar "Registrar:" (puede variar según el TLD)
    match = re.search(r"Registrar:\s*(.*)", whois_data, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "Registrar not found"

def main():
    if len(sys.argv) < 2:
        print("Usage: python whois_lookup.py domain1 [domain2 ...]")
        sys.exit(1)

    domains = sys.argv[1:]
    for domain in domains:
        print(f"Looking up {domain}...")
        data = whois_query(domain)
        print('____________________')
        print(data)
       # registrar = extract_registrar(data)
        #print(f"{domain}: {registrar}\n")

if __name__ == "__main__":
    main()

