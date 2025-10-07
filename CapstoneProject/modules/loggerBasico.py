# modules/logger.py
#Tracking all changes in the directories
#write the change in a log file
import datetime
import config
import os
import sqlite3

LOGFILE=config.LOG_FILE
DB_PERSITENCE=config.ENABLE_DB_PERSISTENCE
DB_PATH=config.DB_PATH

def log_event(event_type, filepath, file_hash=None):
    # it saves date, time, type of change nad file affected 
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if file_hash:
        log_line= f'{timestamp} - {event_type.upper()} - {filepath} - HASH: {file_hash}\n'
    else:
        log_line = f'{timestamp} - {event_type.upper()} - {filepath}\n'
    try:
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write(f'{log_line}')
    except FileNotFoundError:
        print(f'File  {LOGFILE} not found')
    except Exception as e:
        print(f'!!!Error writing the log: {e}')


    if DB_PERSITENCE :
        print()

    try:
        print()
    except Error as e:
        print("No se pudo conectar a MySQL. Se usará almacenamiento en archivo.")