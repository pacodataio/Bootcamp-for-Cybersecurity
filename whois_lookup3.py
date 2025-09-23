import whois
import sys

# Tomar el dominio desde la línea de comandos
domain = sys.argv[1]

# Hacer la consulta
w = whois.whois(domain)

# Mostrar solo el registrar name
print(w.registrar)
