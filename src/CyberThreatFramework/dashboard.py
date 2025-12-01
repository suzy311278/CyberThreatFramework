from flask import Flask, render_template, send_from_directory, jsonify, request
import pandas as pd
import os
import subprocess
import threading
import time
from datetime import datetime
import sys
# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# Also add the current directory to path for direct imports if needed
sys.path.append(os.path.dirname(__file__))

try:
    from src.CyberThreatFramework.data import ATTACK_CATALOG, THREAT_ACTORS
except ImportError:
    from data import ATTACK_CATALOG, THREAT_ACTORS

app = Flask(__name__)

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
PYTHON_EXEC = sys.executable
MAIN_SCRIPT = os.path.join(BASE_DIR, 'main.py')

# Global state for running simulations
running_process = None
simulation_output = []

@app.route('/')
def index():
    return render_template('dashboard.html', 
                           catalog=ATTACK_CATALOG, 
                           actors=THREAT_ACTORS)

@app.route('/api/stats')
def get_stats():
    log_file = os.path.join(LOG_DIR, 'simulation_log.csv')
    total_events = 0
    modules_count = {}
    recent_events = []
    
    if os.path.exists(log_file):
        try:
            df = pd.read_csv(log_file)
            total_events = len(df)
            modules_count = df['Module'].value_counts().to_dict()
            recent_events = df.tail(5).to_dict('records')
        except:
            pass
            
    return jsonify({
        "total_events": total_events,
        "modules_count": modules_count,
        "recent_events": recent_events,
        "attack_types": len(ATTACK_CATALOG)
    })

@app.route('/api/logs')
def get_logs():
    log_file = os.path.join(LOG_DIR, 'simulation_log.csv')
    logs = []
    if os.path.exists(log_file):
        try:
            df = pd.read_csv(log_file)
            df = df.sort_values(by='Timestamp', ascending=False)
            logs = df.to_dict('records')
        except:
            pass
    return jsonify(logs)

@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    global running_process, simulation_output
    data = request.json
    tool = data.get('tool')
    target = data.get('target', '127.0.0.1')
    
    if running_process and running_process.poll() is None:
        return jsonify({"status": "error", "message": "A simulation is already running"}), 400
        
    simulation_output = []
    
    cmd = []
    if tool == 'scan':
        cmd = [PYTHON_EXEC, MAIN_SCRIPT, 'scan', target, '--ports', '22', '80', '443']
    elif tool == 'bruteforce':
        cmd = [PYTHON_EXEC, MAIN_SCRIPT, 'bruteforce', target, '--simulate']
    elif tool == 'ransomware':
        # Create a dummy dir for safety
        dummy_dir = os.path.join(BASE_DIR, 'simulation_target')
        if not os.path.exists(dummy_dir):
            os.makedirs(dummy_dir)
            with open(os.path.join(dummy_dir, 'data.txt'), 'w') as f: f.write("dummy data")
        cmd = [PYTHON_EXEC, MAIN_SCRIPT, 'ransomware', dummy_dir]
    elif tool == 'plc':
        cmd = [PYTHON_EXEC, MAIN_SCRIPT, 'plc', target]
    else:
        # Fallback for unimplemented tools
        simulation_output.append(f"Simulation for {tool} is a placeholder.")
        return jsonify({"status": "success", "message": "Placeholder simulation started"})

    def run_proc():
        global running_process, simulation_output
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        running_process = process
        
        for line in process.stdout:
            simulation_output.append(line.strip())
        for line in process.stderr:
            simulation_output.append(f"ERROR: {line.strip()}")
            
        process.wait()
        
        # Auto-generate visualizations
        simulation_output.append("--- Generating Visualizations & Maps ---")
        viz_cmd = [PYTHON_EXEC, MAIN_SCRIPT, 'visualize']
        subprocess.run(viz_cmd)
        
        simulation_output.append("--- Simulation Complete ---")

    thread = threading.Thread(target=run_proc)
    thread.start()
    
    return jsonify({"status": "success", "message": f"Started {tool} simulation"})

@app.route('/api/monitor')
def monitor_simulation():
    global simulation_output
    return jsonify({"output": simulation_output})

@app.route('/logs/<path:filename>')
def custom_static(filename):
    return send_from_directory(LOG_DIR, filename)

if __name__ == '__main__':
    print(f"Starting Enhanced Dashboard on port 5002")
    app.run(host='0.0.0.0', port=5002, debug=True)
