# modules/analyzer.py
import hashlib
import os

class Analyzer:
    def __init__(self, logger, alert, malware_scanner):
        self.logger = logger
        self.alert = alert
        self.malware_scanner = malware_scanner
        self.hashes = {}  # dictionary  {file_path: latest_hash} to keep the latest hash for every file     

    def calcular_hash(self, filepath):
        try:
            with open(filepath, "rb") as f:
                hash = hashlib.sha256() #new instance
                while chunk := f.read(8192): #reading the file per blocks of 8kb
                    hash.update(chunk) # the hash is updated every block is reed
            return hash.hexdigest() #once the reading s finish it return the final hash
        except Exception as e:
            # if the file was eliminated or not exists
            return None

    def analyze_change(self, event_type, filepath):
        # event_type: created, modified, 'deleted'
        # filepath: absolute path of the file 

        #If deleted then  remove the hash and log and alert
        if event_type == "deleted":
            prev = self.hashes.pop(filepath, None)  # we remove the hash
            # write the log and send alert (no  hash)
            self.logger.log_event("deleted", filepath, None)
            self.alert.send_alert("deleted", filepath)
            return

        # compute the current hash
        current_hash = self.calcular_hash(filepath)
        if current_hash is None:
            # Awe cant acces the file or it was just deleted
            # we just ignore this
            return

        #  we get the previous hash (the latest calculated)
        previous_hash = self.hashes.get(filepath)

        # its new file or  just cretaed, so no previous hash
        if previous_hash is None:
            # save the hash
            self.hashes[filepath] = current_hash
            # Register (file created)
            self.logger.log_event(event_type, filepath, current_hash)
            self.alert.send_alert(event_type, filepath)

            #Call the malware scanner  to dismiss possible malware
            malware_alert = self.malware_scanner.scan_file(filepath, current_hash)
            if malware_alert:
                self.logger.log_event("Malware Detected", filepath, current_hash)
                self.alert.send_alert("MALWARE", filepath, malware_alert)
            return
        
        #the file was updated, different content
        #if has is different then: "file was changed": update new hash, log, alert and malware scanner.
        if current_hash != previous_hash:
            self.hashes[filepath] = current_hash #update the hash
            self.logger.log_event(event_type, filepath, current_hash)
            self.alert.send_alert(event_type, filepath)

            # scanning the file to dismiss malware
            malware_alert = self.malware_scanner.scan_file(filepath, current_hash)
            if malware_alert:
                self.logger.log_event("Malware Detected", filepath, current_hash)
                self.alert.send_alert("MALWARE",filepath, malware_alert)
            return

        # No change
        return None

    def handle_move(self, src_path, dest_path):
        #function to handel events when the file was renamed or moved to other directory
        #keep the same has and  register the change 
        src_path = os.path.abspath(src_path)
        dest_path = os.path.abspath(dest_path)

        # IF the original file is already registered  (hash already calculated)
        if src_path in self.hashes:
            file_hash = self.hashes.pop(src_path)  # we removed the element from the dictionary
            self.hashes[dest_path] = file_hash     # we save the same hash using the new path

            # we register the change in the log
            self.logger.log_event("moved", f'{src_path} to {dest_path}', file_hash)
            self.alert.send_alert("moved", dest_path)
              #Call the malware scanner  to dismiss possible malware
            malware_alert = self.malware_scanner.scan_file(dest_path, file_hash)
            if malware_alert:
                self.logger.log_event("Malware Detected", dest_path, file_hash)
                self.alert.send_alert("MALWARE", dest_path, malware_alert)
            return
        else:
            # if the file is not yet registered. we handle it as a new file
            self.logger.log_event("moved-unknown", f"{src_path} to {dest_path}", None)
            self.analyze_change("created", dest_path)
            
