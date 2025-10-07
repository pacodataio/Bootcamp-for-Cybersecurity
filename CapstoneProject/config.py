
import platform
import os

#Directories to monitor
DIRECTORIES_TO_WATCH = [
    ".",
    "/etc",  
    "/Users/franciscocr/Documents"   ]

LOG_FILE = "file_monitor.log"

#set the value to true to enable  database peristence
ENABLE_DB_PERSISTENCE=True
#Db out od the directories to watch to avoid loops
if platform.system() == "Windows":
    DB_PATH = "C:\\Temp\\secure_log.db"
else:
    DB_PATH = "/tmp/secure_log.db"

# set the value to True to enable  malware SCAN 
ENABLE_MALWARE_SCAN = True

# ANSI color codes to print alerts
COLORS = {
    "INFO": "\033[94m",      # azul
    "WARNING": "\033[93m",   # amarillo
    "CRITICAL": "\033[91m",  # rojo
    "SEVERE": "\033[95m",   # magenta
    "SEVERE2": "\033[92m",   # magenta
    "RESET": "\033[0m"
}