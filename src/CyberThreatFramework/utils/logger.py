import logging
import json
import csv
import os
from datetime import datetime

class ThreatLogger:
    def __init__(self, log_dir="src/CyberThreatFramework/logs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        self.json_log_file = os.path.join(log_dir, "simulation_log.json")
        self.csv_log_file = os.path.join(log_dir, "simulation_log.csv")
        
        # Initialize CSV header if file doesn't exist
        if not os.path.exists(self.csv_log_file):
            with open(self.csv_log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Module", "Event", "Details", "Status"])

    def log_event(self, module, event, details, status="INFO"):
        timestamp = datetime.now().isoformat()
        
        # Log to JSON
        log_entry = {
            "timestamp": timestamp,
            "module": module,
            "event": event,
            "details": details,
            "status": status
        }
        
        with open(self.json_log_file, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
            
        # Log to CSV
        with open(self.csv_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, module, event, str(details), status])
            
        print(f"[{timestamp}] [{module}] {event}: {status}")
