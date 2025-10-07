# This module define the finctions and scripts to monitor file on real time using watchdog library
import time,os
import platform
import config
#from . import alert, logger, malware_scanner
from . import alert
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from .analyzer import Analyzer
from modules.logger import  Logger
from modules.malware_scanner import MalwareScanner

#hetting parameters from config
logfile=config.LOG_FILE
db_path=config.DB_PATH
db_persistence=config.ENABLE_DB_PERSISTENCE
directories=config.DIRECTORIES_TO_WATCH

#creating Instances
malwarescanner=MalwareScanner()
logger=Logger(logfile,db_path,db_persistence)
analyzer = Analyzer(logger, alert,malwarescanner)  # creating and  Analyzer object which anlyze if  the changes are real
#if changes are real  different hash, then send logs and alerts

class FileChangeHandler(FileSystemEventHandler):
    # class to handle the events launched after file is created, modified or deleted"
    def __init__(self, logfile):
        super().__init__()  # coall the constructor of the FileSystemEventHandler
        self.logfile = os.path.abspath(logfile)  # saving  the absolute path of the  file log

    def on_created(self, event):
        # to avoi infinite loop, so we ignore the change in the log file
        if os.path.abspath(event.src_path) == self.logfile:
            return
        if not event.is_directory:
            analyzer.analyze_change("created", event.src_path)

    def on_modified(self, event):
        # to avoi infinite loop, so we ignore the change in the log file
        if os.path.abspath(event.src_path) == self.logfile:
            return 
        if not event.is_directory:
            analyzer.analyze_change("modified", event.src_path)

    def on_deleted(self, event):
        # to avoi infinite loop, so we ignore the change in the log file
        if os.path.abspath(event.src_path) == self.logfile:
            return 
        if not event.is_directory:
            analyzer.analyze_change("deleted", event.src_path)
    
    def on_moved(self, event):
        # function to handle events when the file was moved or renamed
        #if self.should_ignore(event.dest_path) or self.should_throttle(event.dest_path):
           #  return
        if os.path.abspath(event.dest_path) == self.logfile:
            return 
       
        try:
            #print(f'[WARNING] file was moved/renamed: {event.src_path} to {event.dest_path}')      
            analyzer.handle_move(event.src_path, event.dest_path)
        except Exception as e:
            print(f'[ERROR] Moving file {event.src_path} to {event.dest_path}: {e}')
        
def start_watching():
    # Function to start the monitoring the files indicated with
    # the directories parameter
   
    event_handler = FileChangeHandler(logfile)
     # --- Checking the OS ---
     #MAC is crashing using FSEvents
    if platform.system() == "Darwin":
        print('[INFO] macOS detected: using PollingObserver (more stable)')
        observer = PollingObserver(timeout=1.0)
    else:
        observer = Observer()

    for path in directories:
        try:
            abspath = os.path.abspath(path)
            if not os.path.exists(abspath):
                print(f'Warning: {abspath} does not exist, skipping')
                continue
            print(f'(*) Monitoreando: {abspath}')
            try:
                observer.schedule(event_handler, abspath, recursive=True) 
            except Exception as e:
                 print(f'Error scheduling {abspath}: {e}')
        except PermissionError:
            print(f'Permission denied: {path}, skipping')
        except Exception as e:
             print(f'Error scheduling {path}: {e}')
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
            observer.stop()
    finally:
            observer.join()