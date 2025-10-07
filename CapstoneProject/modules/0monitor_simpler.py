# This module define the finctions and scripts to monitor file on real time using watchdog library
from . import alert, loggerBasico
from watchdog.observers import Observer
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
import time,os
import platform


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
            loggerBasico.log_event("created", event.src_path,self.logfile)
            alert.send_alert("created", event.src_path)

    def on_modified(self, event):
        # to avoi infinite loop, so we ignore the change in the log file
        if os.path.abspath(event.src_path) == self.logfile:
            return 
             
        if not event.is_directory:
            loggerBasico.log_event("modified", event.src_path,self.logfile)
            alert.send_alert("modified", event.src_path)

    def on_deleted(self, event):
        # to avoi infinite loop, so we ignore the change in the log file
        if os.path.abspath(event.src_path) == self.logfile:
            return 
            
        if not event.is_directory:
            loggerBasico.log_event("deleted", event.src_path,self.logfile)
            alert.send_alert("deleted", event.src_path)
    
def start_watching(directories, logfile):
    # Function to start the monitoring the files indicated with
    # the directories parameter
   
    event_handler = FileChangeHandler(logfile)
     # --- Checking the OS ---
     #MAC is crashing using FSEvents
    if platform.system() == "Darwin":
        print("[INFO] macOS detected: using PollingObserver (more stable)")
        observer = PollingObserver(timeout=1.0)
    else:
        observer = Observer()

    for path in directories:
        try:
            abspath = os.path.abspath(path)
            if not os.path.exists(abspath):
                print(f"Warning: {abspath} does not exist, skipping")
                continue
            print(f"[*] Monitoreando: {abspath}")
            try:
                observer.schedule(event_handler, abspath, recursive=True) 
            except Exception as e:
                 print(f"Error scheduling {abspath}: {e}")
        except PermissionError:
            print(f"Permission denied: {path}, skipping")
        except Exception as e:
             print(f"Error scheduling {path}: {e}")
    try:
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
            observer.stop()
    finally:
            observer.join()