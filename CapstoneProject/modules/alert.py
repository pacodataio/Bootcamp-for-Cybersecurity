# modules/alert.py
#module to show the alerts on the screen
import config
import datetime

COLORS=config.COLORS

def send_alert(event_type, filepath,malware_alert=None):
    # sShow on the screen an alert depending the kind of event
 
    if event_type == "created":
        level = "INFO"
        message = f'[+] New File created: {filepath}'
    elif event_type == "modified":
        level = "WARNING"
        message = f'[!] File Updated : {filepath}'
    elif event_type == "deleted":
        level = "CRITICAL"
        message = f'[-] File deleted: {filepath}'
    elif event_type == "moved":
        level = "SEVERE2"
        message = f'[-] File moved/rnamed to: {filepath}'
    elif event_type == "MALWARE":
        level = "SEVERE"
        message = f'[-] MALWARE: {malware_alert} : {filepath}'
        print(f'filepath:{filepath}')
    else:
        level = "DEBUG"
        message = f'[?] Evento desconocido: {filepath}'

    #print(f'[{level}] {message}')
    # Color y salida
    color = COLORS.get(level, COLORS["RESET"])
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{color}{timestamp} | {level:<8} | {message}{COLORS['RESET']}")