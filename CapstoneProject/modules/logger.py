# modules/logger.py
#Tracking all changes in the directories
#write the change in a log file
import datetime
import config
import os
import sqlite3

#LOGFILE=config.LOG_FILE
#DB_PERSITENCE=config.ENABLE_DB_PERSISTENCE
#DB_PATH=config.DB_PATH

class  Logger:
    def __init__(self, logfile=config.LOG_FILE, db_path=config.DB_PATH, db_persistence=config.ENABLE_DB_PERSISTENCE):
            self.logfile = os.path.abspath(logfile)
            self.db_path = os.path.abspath(db_path)
            self.db_persistence=db_persistence
            self._init_db()

    def _init_db(self):
        if self.db_persistence:
            try:
                os.makedirs(os.path.dirname(self.db_path), exist_ok=True) #make sure the directoy exists if no it will be created
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        event_type TEXT,
                        filepath TEXT,
                        filehash TEXT
                    )
                """)
                conn.commit()
                conn.close()
            except Exception as e:
                print(f' Error logger._init_db:{e}.It couldnt connect to  DB : {self.db_path}.')

    def register_log_in_db(self,timestamp,event_type, filepath, file_hash):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO logs (timestamp, event_type, filepath, filehash) VALUES (?, ?, ?, ?)",
                (timestamp, event_type, filepath, file_hash)
            )
            conn.commit()
            conn.close()
        except Exception as e:
                print(f'Error Logger.log_in_DB :{e}. BB_PATH= {self.db_path}.')

    def log_event(self,event_type, filepath, file_hash=None):
        # it saves date, time, type of change nad file affected 
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if file_hash:
            log_line= f'{timestamp} - {event_type.upper()} - {filepath} - HASH: {file_hash}\n'
        else:
            log_line = f'{timestamp} - {event_type.upper()} - {filepath}\n'

        try:
            with open(self.logfile, "a", encoding="utf-8") as f:
                f.write(f'{log_line}')
        except FileNotFoundError:
            print(f'File  {self.logfile} not found')
        except Exception as e:
            print(f'!!!Error writing the log: {e}')

        if self.db_persistence:
            self.register_log_in_db(timestamp, event_type, filepath, file_hash)

